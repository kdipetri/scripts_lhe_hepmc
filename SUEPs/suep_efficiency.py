#!/usr/bin/env python

import json
import numpy
import matplotlib 
matplotlib.use('pdf') # for speed? 
import matplotlib.pyplot as plt

f = open('SUEP_effieciencies.json',)
data = json.load(f)

masses = [125, 200, 400, 600, 800, 1000]
ntracks = [100, 150, 200]
pts = [0.5, 1, 2]


def get_bins(dist):
    # start, stop, stepsize
    if "compare_mass"   in dist: return masses 
    if "compare_ntrack" in dist: return ntracks
    if "compare_pt"     in dist: return pts
    else : return np.arange(0, 3000, 100)

def leg_loc(dist):
    if "pt1" in dist: return "upper left"
    if "pt2" in dist: return "upper left"
    if "pt05" in dist: return "lower right"
    return "upper right"

def xlabel(dist):
    if   "compare_mass"   in dist: return "Mediator Mass $m_{\\Phi}$ (GeV)"
    elif "compare_ntrack" in dist: return "$n_{\\mathsf{Track}}$"
    elif "compare_pt"     in dist: return "$p_{\mathsf{T}}$ (GeV)"
    else : return ""

def ylabel(dist):
    return "Efficiency"

def compare_effs(yvals,yerrs,labels,title,outfile):
    print(outfile)

    bins = get_bins(outfile)
    plt.style.use('seaborn-colorblind')
    plt.figure(figsize=(6,5.5))

    for i in range(0,len(yvals)):
        plt.errorbar( bins, yvals[i], yerrs[i], label=labels[i], marker = "o", alpha=0.5)

    plt.subplots_adjust(left=0.18, right=0.95, top=0.9, bottom=0.18)
    plt.grid(visible=True, which='major', axis='both', color='gainsboro')

    #plt.yscale(yscale(outfile))
    plt.ylim(-0.05,1.05)

    ax = plt.axes()
    ax.xaxis.set_major_locator(plt.MaxNLocator(5))
    ax.yaxis.set_major_locator(plt.MaxNLocator(5))
   
    size=20 
    
    plt.xlabel(xlabel(outfile), fontsize=size, labelpad=size/2)
    plt.ylabel(ylabel(outfile), fontsize=size, labelpad=size/2)
    plt.xticks(fontsize=size-4)
    plt.yticks(fontsize=size-4)
    plt.title(title,fontsize=size-4)
    plt.legend(loc=leg_loc(outfile),prop={'size':size-4,})

    plt.savefig(outfile)
    plt.clf()
    return

# efficiencies are of the format
#    "data": [
#        {"cut": "125_pt05_n100", "efficiency": efficiencies[0][0], "error" : errors[0][0]},
# err_n100_125 = [data["data"][0]["error"], data["data"][3]["error"], data["data"][6]["error"]]


def get_cut_index(mass=125,n=100,pt=0.5):
    i = masses.index(mass)
    j = pts.index(pt)
    k = ntracks.index(n)
    cut = i*9 + j*3 + k
    return cut

def get_efficiency(mass=125,n=100,pt=0.5):

    i = get_cut_index(mass,n,pt)
    cut = data["data"][i]["cut"]
    eff = data["data"][i]["efficiency"]
    err = data["data"][i]["error"]
    print(cut,eff,err)
    return eff,err 

def get_eff_array(masses=[],ntracks=[],pts=[]):

    # returns an array of efficiency 
    # v. mass , ntracks, or pt
    eff_array = []
    err_array = []
    if len(masses)>1:
        for mass in masses:
            eff,err = get_efficiency(mass,ntracks[0],pts[0])
            eff_array.append( eff )
            err_array.append( err )
    if len(ntracks)>1:
        for ntrack in ntracks:
            eff,err = get_efficiency(mass[0],ntrack,pts[0])
            eff_array.append( eff )
            err_array.append( err )
    if len(pts)>1:
        for pt in pts:
            eff,err = get_efficiency(mass[0],ntracks[0],pt)
            eff_array.append( eff )
            err_array.append( err )
    
    return eff_array,err_array

# compare efficiency: x-axis mass, legend nTracks, fixed pT 
def compare_mass_ntracks_pt(pt=0.5):
    
    eff_arrays=[]
    err_arrays=[]
    labels=[]
    title="$p_{\\mathsf{T}}$ >"+" {} GeV".format(pt)
    outfile = "plots/effs/compare_mass_ntracks_pt{}.pdf".format( "05" if pt==0.5 else pt )
    
    for ntrack in ntracks:
        eff_array,err_array = get_eff_array(masses,[ntrack],[pt])
        eff_arrays.append(eff_array)
        err_arrays.append(err_array)
        labels.append("$n_{\\mathsf{Track}}$"+" > {}".format(ntrack))

    compare_effs(eff_arrays,err_arrays,labels,title,outfile)
    return 

# compare fficiency: x-axis mass, legend pt, fixed ntracks
def compare_mass_pt_ntracks(ntrack=150):
    

    eff_arrays=[]
    err_arrays=[]
    labels=[]
    title="$n_{\\mathsf{Track}}$ >"+" {}".format(ntrack)
    outfile = "plots/effs/compare_mass_pt_ntracks{}.pdf".format( ntrack )
    
    for pt in pts:
        eff_array,err_array = get_eff_array(masses,[ntrack],[pt])
        eff_arrays.append(eff_array)
        err_arrays.append(err_array)
        labels.append("$p_{\\mathsf{T}}$"+" > {} GeV".format(pt))

    compare_effs(eff_arrays,err_arrays,labels,title,outfile)
    return 

compare_mass_ntracks_pt(0.5)
compare_mass_ntracks_pt(1)
compare_mass_ntracks_pt(2)

compare_mass_pt_ntracks(100)
compare_mass_pt_ntracks(150)
compare_mass_pt_ntracks(200)
