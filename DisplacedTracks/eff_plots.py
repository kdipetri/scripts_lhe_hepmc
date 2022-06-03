#!/usr/bin/env python
import argparse
import json
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import uproot4 as uproot
import scipy.interpolate
import math
from scipy.interpolate import griddata
from scipy.interpolate import interpn
from matplotlib.ticker import (MultipleLocator, FormatStrFormatter,
                               AutoMinorLocator)

from matplotlib import colors as mcolors
import colorsys
from matplotlib.colors import ListedColormap, LinearSegmentedColormap

plt.ioff()

def argsort(seq):
    return sorted(range(len(seq)), key=seq.__getitem__)

event_count = 10000
check = 1

# arg parsing
parser = argparse.ArgumentParser(description='process model')
parser.add_argument('model'  , type=str , default='staus', help='benchmark model: higgs or staus')
parser.add_argument('ntracks', type=int , default=2      , help='ntracks required per event')
parser.add_argument('slope'  , type=bool, default=True   , help='True for lin slope, false for binary')
#parser.add_argument('doTest' , type=bool, default=False )

args = parser.parse_args()
model   = args.model
track_low_cut = args.ntracks
use_slope_eff = args.slope
doTest  = False 

#change to true if you want to run a certain section of the plotting code
# 1D efficiencies
do_eff = True 
# 2D eff and acceptance
do_2D = False #True  

#track efficiency defined in stau_eff.py
track_eff = 1

#Format naming conventions
pre = ""
if doTest:
    pre = "test_"

append = "_NOslope"
if use_slope_eff:
    append = "_slope"

#creates empty lists of lifetimes, pts, d0s, and masses
lt_list  = []
clt_list = []
pt_list  = []
d0_list  = []
mass_list = []

cf_masses = []
cf_lifetimes = []
cf_values_pt = []
cf_values_d0 = []
cf_values_both = []
cf_cats_pt   = ["events", "seen"]
cf_cats_d0   = ["events", "seen"]
cf_cats_both = ["events", "seen"]

#getfile
f = open('output/%s%s_%dtrack_%.1feffs%s.json'%(pre,model,track_low_cut,track_eff,append))
data = json.load(f)

trk_str = "$n_{\\mathsf{Track}} \\geq$ "+str(track_low_cut)

def life_to_float(life):
    fl = float(life.strip("ns").replace("p","."))
    return fl

#fills the lists from the values in the .json data file
print("Preparing lists")
for i in data["lifetimes"]:
    lt_list.append(i)
for i in lt_list:
    clt_list.append( life_to_float(i) )
for i in data["pts"]:
    pt_list.append(i)
for i in data["d0s"]:
    d0_list.append(i)
for i in data["data"]:
    if i["cmass"] not in mass_list:
        mass_list.append(i["cmass"])
mass_list.sort()


# Structure: [lifetime][pt][d0][mass]
cmasses       = np.zeros((len(lt_list), len(pt_list), len(d0_list), len(mass_list))) * np.nan
efficiencies  = np.zeros((len(lt_list), len(pt_list), len(d0_list), len(mass_list))) * np.nan
errors        = np.zeros((len(lt_list), len(pt_list), len(d0_list), len(mass_list))) * np.nan

# Structure: [mass][pt][d0][clifetime]
clifetimes    = np.zeros((len(mass_list), len(pt_list), len(d0_list), len(clt_list))) * np.nan
cefficiencies = np.zeros((len(mass_list), len(pt_list), len(d0_list), len(clt_list))) * np.nan
cerrors       = np.zeros((len(mass_list), len(pt_list), len(d0_list), len(clt_list))) * np.nan

# Structure: [lifetime][mass] 
seen_event_list = np.zeros((len(mass_list), len(clt_list)))*np.nan
event_list      = np.zeros((len(mass_list), len(clt_list)))*np.nan


# Collect efficiency data in array
print("Collecting efficiency data")
for i in data["data"]:
    #print(i)
    L = lt_list.index(i["lifetime"])
    C = clt_list.index(life_to_float(i["lifetime"]))
    P = pt_list.index(i["pt"])
    D = d0_list.index(i["d0"])
    M = mass_list.index(i["cmass"])

    cmasses[L][P][D][M] = i["cmass"]
    efficiencies[L][P][D][M] = i["efficiency"]
    errors[L][P][D][M] = i["error"]

    clifetimes[M][P][D][C] = i["clifetime"]
    cefficiencies[M][P][D][C] = i["efficiency"]
    cerrors[M][P][D][C] = i["error"]
    twodeffs = np.swapaxes(cefficiencies,0,2)

for i in data["cutflow"]:
    #print(i)
    L = lt_list.index(i["lifetime"])
    C = clt_list.index( life_to_float(i["lifetime"]) )
    M = mass_list.index(i["cmass"])

    seen_event_list[M][C] = i["seen"]
    event_list[M][C] = i["events"]

acc = np.divide(seen_event_list,event_list)


f.close()

def manual_cmap(cmap, value=1.):
    colors = cmap(np.arange(cmap.N))
    hls = np.array([colorsys.rgb_to_hls(*c) for c in colors[:,:3]])
    hls[:,1] *= value
    rgb = np.clip(np.array([colorsys.hls_to_rgb(*c) for c in hls]), 0,1)
    return mcolors.LinearSegmentedColormap.from_list("", rgb)

#EFFICIENCY PLOTS
#-----------------

plt.style.use('seaborn-colorblind')



if do_eff:
    
    # outfile format
    # model_Ntrack_%eff_vlifetime_varyd0_fixpt_X_fixmass_Y"

    part_tex = "\\mathsf{S}" if model=='higgs' else "\\tilde{\\tau}"
    part_str = "Scalar" if model=='higgs' else "Stau"
    part_mass = "$m_{"+part_tex+"}$"
    part_life = "$\\tau_{"+part_tex+"}$"

    def xlabel(outfile):

        if "vlifetime" in outfile : 
            if model=='higgs' : return "Scalar Lifetime (ns)" 
            if model=='staus' : return "Stau Lifetime (ns)" 
        if "vmass" in outfile : 
            if model=='higgs' : return "Scalar Mass (GeV)"
            if model=='staus' : return "Scalar Mass (GeV)" 
        return "" 

    def xscale(outfile):
        if 'vlifetime' in outfile : return 'log'
        return 'linear'

    def make_1D_eff( xarrays, yarrays, yerrs, labels, title, outfile ):

        fig,axs = plt.subplots(figsize=(6,5.5))
        size=20 
        
        axs.set_title(title,fontsize=size-4)
        axs.set_xlabel(xlabel(outfile) ,fontsize=size, labelpad=size/2)
        axs.set_ylabel("Efficiency"    ,fontsize=size, labelpad=size/2)
        plt.xticks(fontsize=size-4)
        plt.yticks(fontsize=size-4)
        
        for k in range(len(xarrays)):
            axs.errorbar(xarrays[k], yarrays[k], yerr = yerrs[k], label = labels[k], marker = "o", alpha = 0.5)
        
        plt.subplots_adjust(left=0.18, right=0.95, top=0.9, bottom=0.18)
        plt.ylim(-0.05,1.05)
        axs.set_xscale(xscale(outfile))
        
        plt.grid(visible=True, which='major', axis='both', color='gainsboro')
        
        axs.legend(prop={'size':size-5,},borderpad=0.2, handlelength=1, handletextpad=0.5)
        
        fig.savefig(outfile)
        
        plt.clf()
    
        return

    # Make plots....

    # X axis lifetime, fixed mass, fixed transverse momentum, vary d0 efficiency plots
    for i in range(len(mass_list)):
        for j in range(len(pt_list)):

            labels = []
            title = trk_str+", "+part_mass+" = "+str(mass_list[i])+ " GeV, $p_{\mathsf{T}}$ > " +str(pt_list[j]) + " GeV"
            outfile = "plots/1D/%s%s_%dtrack_%.1feff%s_vlifetime_varyd0_fixmass_%s_fixpt_%s.pdf"%(pre,model,track_low_cut,track_eff,append,str(mass_list[i]),str(pt_list[j]))
            for k in range(len(d0_list)):
                labels.append("$|d_0| <$ " + str(d0_list[k]) + " mm")
        
            make_1D_eff( clifetimes[i][j], cefficiencies[i][j], cerrors[i][j], labels, title, outfile)


            if doTest: break
        if doTest: break

    # X axis mass, fixed lifetime, fixed transverse momentum, vary d0 efficiency plots
    for i in range(len(lt_list)):
        for j in range(len(pt_list)):

            labels=[]
            title = trk_str+", "+part_life+" = "+str(clt_list[i])+ " ns, $p_{\mathsf{T}}$ > " +str(pt_list[j]) + " GeV"
            outfile = "plots/1D/%s%s_%dtrack_%.1feff%s_vmass_varyd0_fixlifetime_%s_fixpt_%s.pdf"%(pre,model,track_low_cut,track_eff,append,str(lt_list[i]),str(pt_list[j]))

            for k in range(len(d0_list)):
                labels.append("$|d_0| <$ " + str(d0_list[k]) + " mm")

            make_1D_eff( cmasses[i][j], efficiencies[i][j], errors[i][j], labels, title, outfile)

            if doTest: break
        if doTest: break

    # X axis lifetime, fixed mass, fixed d0, vary pt efficiency plots
    for i in range(len(mass_list)):
        for j in range(len(d0_list)):

            labels = []
            title = trk_str+", "+part_mass+" = "+str(mass_list[i])+ " GeV, $|d_0|$ < " +str(d0_list[j]) + " mm"
            outfile = "plots/1D/%s%s_%dtrack_%.1feff%s_vlifetime_varypt_fixmass_%s_fixd0_%s.pdf"%(pre,model,track_low_cut,track_eff,append,str(mass_list[i]),str(d0_list[j]))

            xarrays = []
            yarrays = []
            yerrs = []
            for k in range(len(pt_list)):
                labels.append("$p_{\\mathsf{T}} >$ " + str(pt_list[k]) + " GeV")
                xarrays.append(clifetimes[i][k][j])
                yarrays.append(cefficiencies[i][k][j])
                yerrs.append(cerrors[i][k][j])

            make_1D_eff( xarrays, yarrays, yerrs, labels, title, outfile)

            if doTest: break
        if doTest: break

    # X axis mass, fixed lifetime, fixed d0, vary pt efficiency plots
    for i in range(len(lt_list)):
        for j in range(len(d0_list)):

            labels = []
            title = trk_str+", "+part_life+" = "+str(clt_list[i])+ " ns, $|d_0|$ < " +str(d0_list[j]) + " mm"
            outfile = "plots/1D/%s%s_%dtrack_%.1feff%s_vmass_varypt_fixlifetime_%s_fixd0_%s.pdf"%(pre,model,track_low_cut,track_eff,append,str(lt_list[i]),str(d0_list[j]))

            xarrays = []
            yarrays = []
            yerrs = []
            for k in range(len(pt_list)):
                labels.append("$p_{\\mathsf{T}} >$ " + str(pt_list[k]) + " GeV")
                xarrays.append(cmasses[i][k][j])
                yarrays.append(efficiencies[i][k][j])
                yerrs.append(errors[i][k][j])

            make_1D_eff( xarrays, yarrays, yerrs, labels, title, outfile)

            if doTest: break
        if doTest: break



# 2D ACCEPTANCE AND EFFICIENCY HISTOGRAMS
#--------------------
size=16
if do_2D:
    myjet = manual_cmap(plt.cm.get_cmap("rainbow"), 1.2)

    def get_levels(model,zlabel):
        levels = [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0]
        if model == 'higgs' : 
            if zlabel == 'Acceptance' : levels = [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,0.92,0.94,0.96,0.98,1.0]
            elif zlabel == 'AxE'      : levels = [0.02,0.04,0.06,0.08,0.1,0.12,0.14,0.16,0.18,0.2,0.22,0.24]
            else : levels=[0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,0.92,0.94,0.96,0.98,1.0]
        #else : # staus 
        #    if zlabel == 'Acceptance' : levels = 
        return levels
    
    def xaxis(model):
        if model == 'higgs': return "$m_{\\mathsf{S}}$ (GeV)"
        else :               return "$m_{\\tilde{\\tau}}$ (GeV)"

    def yaxis(model):
        if model == 'higgs': return "$\\tau_{\\mathsf{S}}$ (GeV)"
        else :               return "$\\tau_{\\tilde{\\tau}}$ (GeV)"

    def make_2D_plot(x,y,z,model,zlabel,d0="",pt=""):

        if model == 'higgs':
            xlinspace = np.linspace(5,55,500)
        elif model == 'staus':
            xlinspace = np.linspace(100,600,500)
        ylinspace = np.linspace(-3,0,500) #in log space
        xymeshgrid = np.meshgrid(xlinspace,ylinspace)

        ZI = scipy.interpolate.griddata((x,y), z, (xymeshgrid[0],xymeshgrid[1]), method="cubic")
        fig, ax = plt.subplots(figsize=(6, 4) )
        plt.pcolor(xymeshgrid[0], xymeshgrid[1], ZI, vmax=1, vmin=0, rasterized=True,cmap=myjet,alpha=1)

        cbar = plt.colorbar()
        cbar.set_label(zlabel, rotation=270, labelpad=1.5*size, fontsize=size)
        cbar.ax.tick_params(labelsize=size-4)

        CS = plt.contour(xymeshgrid[0], xymeshgrid[1], ZI, levels=get_levels(model,zlabel), colors="k")
        plt.clabel(CS, inline=1, fontsize=size/2, fmt='%1.2f')
        plt.clim(0,1)
        
        # axes 
        plt.xlabel(xaxis(model),fontsize=size, labelpad=size/2-2)
        plt.ylabel(xaxis(model),fontsize=size, labelpad=size/2-2)

        # title
        plt.title("",fontsize=size-4)

        plt.xticks(fontsize=size-4)
        plt.yticks(fontsize=size-4)
        plt.grid(alpha=0.2, which="major")
        plt.grid(alpha=0.1, which="minor")
        plt.subplots_adjust(left=0.2, right=0.88, top=0.9, bottom=0.18)

        ax.set_yticklabels(['0.001','','0.01','','0.1','','1'])
        ax.set_ylim(-3,0)

        label = "{}".format(trk_str) 
        if len(d0)>0 : label = label + "\n$|d_0|$ < " + "{:} mm".format(d0_list[i]) 
        if len(pt)>0 : label = label + "\n$p_{\mathsf{T}} > $ " + "{:} GeV".format(pt_list[j])
        props = dict(boxstyle='round', facecolor="white", alpha = 0.5)
        plt.text(0.85, 0.97, label, verticalalignment='top', horizontalalignment='center', fontsize=size/2., bbox= props, transform=ax.transAxes)

        # outfile
        outfile = 'plots/2D/%s%dtrack_%.1feff_%s_2Dmvslt_%s%s'%(pre,track_low_cut,track_eff,model,zlabel,append)
        if len(d0)>0 : outfile = outfile + "_%s_%s"%(d0,pt)
        outfile = outfile + ".pdf"
        fig.savefig(outfile)
        plt.clf()

    print("2D Histograms of mass vs lifetime")

    # Acceptance
    xArray = []
    yArray = []
    zArray = []

    for k in range(len(mass_list)):
        for l in range(len(clt_list)):
            if np.isnan(acc[k][l]) : continue
            xArray.append(mass_list[k])
            yArray.append(math.log(clt_list[l]))
            zArray.append(acc[k][l])

    xArray = np.array(xArray)
    yArray = np.array(yArray)
    zArray = np.array(zArray)

    make_2D_plot(xArray,yArray,zArray,model,'Acceptance')


    # AxE and Efficiency
    for i in range(len(d0_list)):
        for j in range(len(pt_list)):
            xArray = []
            yArray = []
            zArray1 = []
            zArray2 = []

            twodeffsel = twodeffs[i][j]
            acceff = np.multiply(acc,twodeffsel)
            #print('AxE is: ',acceff)

            for k in range(len(mass_list)):
                for l in range(len(clt_list)):
                    if np.isnan(acceff[k][l]) : continue
                    xArray.append(mass_list[k])
                    yArray.append(math.log(clt_list[l]))
                    zArray1.append(acceff[k][l])
                    zArray2.append(twodeffsel[k][l])

            xArray = np.array(xArray)
            yArray = np.array(yArray)
            zArray1 = np.array(zArray1)
            zArray2 = np.array(zArray2)
        
            d0 = str(d0_list[i])
            pt = str(pt_list[j])

            make_2D_plot(xArray,yArray,zArray1,model,"AxE",d0,pt)
            make_2D_plot(xArray,yArray,zArray2,model,"Efficiency",d0,pt)



