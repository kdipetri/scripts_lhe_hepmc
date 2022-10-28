import json
import time
import numpy as np
import ROOT
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

#https://www.quora.com/What-is-matplotlib-use-and-why-do-we-use-them
import matplotlib 
matplotlib.use('pdf') # for speed? 
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
from util.plot_helper import *

matplotlib.rcParams['hatch.linewidth'] = 0.2
matplotlib.rcParams['hatch.color'] = "tab:gray"

# Displaced Vertex Samples
samples = []
samples.append("qcd_2TeV")
samples.append("higgsportal_125_40_0p1ns")
samples.append("higgsportal_125_55_1ns")

# Displaced Vertex Samples
samples_dv = ["qcd_2TeV","higgsportal_125_40_0p1ns","higgsportal_125_55_1ns"]
samples_dv_labels = ["QCD", "$m_{S}=40$ GeV, $\\tau_{S}=0.1$ ns", "$m_{S}=55$ GeV, $\\tau_{S}=1$ ns" ]


pileups = [200] 

# pre-process input data to speedup??
input_data = {} 
for sample in samples: 
    for pileup in pileups:
        print(sample+"_"+str(pileup))
        f = open('output/analyzed_{}_pileup{}.json'.format(sample, pileup),"r") 
        input_data[sample+"_"+str(pileup)] = json.load(f)
        f.close()   


def distArray(sample,pileup=0,dist="nDVs_3trks_pt1.0;d050"):

    data = input_data[sample+"_"+str(pileup)]
    weight_array = data['weights']
    dist_array   = [ event[dist]  for event in data["events"] ]
    
    return dist_array,weight_array

def jetArray(sample,pileup=0,dist="nDVs_3trks_pt1.0;d050"):

    data = input_data[sample+"_"+str(pileup)]
    weight_array = [] 
    dist_array = []
    for i,evt in enumerate(data["event_jets"]):
        for jet in evt: 
            dist_array   .append( jet[dist] ) 
            weight_array .append( data["weights"][i] ) 
    
    return dist_array,weight_array

def histErrors( values, weights, bin_edges ):
    
    errors = []
    bin_centers = []
    for bin_index in range(len(bin_edges)-1):

        # find which data points are inside the bin
        bin_left = bin_edges[bin_index]
        bin_right = bin_edges[bin_index + 1]
        in_bin = np.logical_and(bin_left < values, values <= bin_right)        
        
        # filter the weights to only those inside the bin
        weights_in_bin = np.array(weights)[in_bin]
        
        # compute the error however you want
        error = np.sqrt(np.sum(weights_in_bin ** 2))
        errors.append(error)
    
        # save the center of the bins to plot the errorbar in the right place
        bin_center = (bin_right + bin_left) / 2
        bin_centers.append(bin_center)

    errors = np.array(errors)
    bin_centers = np.array(bin_centers)
        
    return errors,bin_centers
    

def compare1D(arrays,labels,weights,outfile,title,norm=1):
    plt.style.use('seaborn-v0_8-colorblind')
    plt.figure(figsize=(6,5.5))

    xmax = 0
    for array in arrays: 
        tmpmax = max(array)
        tmpmin = min(array)
        if tmpmax > xmax: xmax=tmpmax
    
    if "ptsum" in outfile: xmax = 1000
    xmax = int(xmax)
    
    if xmax <= 5 : bins = np.linspace(-0.5,5.5,7)
    elif xmax <= 150: bins = np.linspace(-0.5,xmax+1.5,xmax+3)
    else : bins = np.linspace(0,xmax,50) 

    if "eta" in outfile  : bins = np.linspace(-2.5,2.5,20)
    if "frac" in outfile : bins = np.linspace(0,1,20)
    
    if "DVProp" in outfile: 
        if "sumpt" in outfile  :  bins = np.linspace(0,20,20)
        if "sumpt2" in outfile :  bins = np.linspace(0,50,100)
        if "mass" in outfile :  bins = np.linspace(0,20,40)
        if "rxy" in outfile :  bins = np.linspace(0,300,300)

    for i in range(0,len(arrays)):
        (counts, bins) = np.histogram(arrays[i], bins=bins, weights=weights[i])
        factor = sum(weights[i])
        hist_weights = counts/float(factor) if  norm==1 else counts

        errors, bin_centers = histErrors(arrays[i],weights[i], bins)
        hist_errors = errors/float(factor) if  norm==1 else errors

        if norm==1 and "QCD" in labels[i]: 
            plt.hist(bins[:-1], bins, histtype='stepfilled', color="tab:gray", alpha=0.7, label=labels[i], weights=hist_weights)
            plt.fill_between(bins[1:], hist_weights-hist_errors, hist_weights+hist_errors, step='pre',  hatch='////////', linewidth='0', fc='none')
        else : 
            plt.hist(bins[:-1], bins, histtype='step', label=labels[i], weights=hist_weights)

    if "hit_t" in outfile:
        ax = plt.axes()
        ax.xaxis.set_major_locator(plt.MaxNLocator(5))
        ax.yaxis.set_major_locator(plt.MaxNLocator(5))

    plt.subplots_adjust(left=0.18, right=0.95, top=0.9, bottom=0.18)
    plt.grid(visible=True, which='major', axis='both', color='gainsboro')

    plt.yscale('log')
    plt.ylim(0.00001,100.)
   
    size=20 
    plt.xlabel(xtitle(outfile),fontsize=size, labelpad=size/2)
    plt.ylabel(ytitle(outfile) + " (AU)",fontsize=size, labelpad=size/2)
    plt.xticks(fontsize=size-4)
    plt.yticks(fontsize=size-4)
    plt.title(title,fontsize=size-4)
    plt.legend(prop={'size':size-5,})

    plt.savefig(outfile)
    plt.clf()
    plt.close()
    print(outfile)
    return



def dvArray(sample,pileup=0,dist="ndvs3",ntracks=3):

    data = input_data[sample+"_"+str(pileup)]
    weight_array = [] 
    dist_array = []

    ndvs2_array = []
    ndvs3_array = []
    ndvs4_array = []
    ndvs5_array = []
    ndv_weight_array = [] 
    for i,evt in enumerate(data["event_dvs"]):
        ndvs2 = 0
        ndvs3 = 0
        ndvs4 = 0
        ndvs5 = 0
        #print(i,evt)
        for dv in evt: 
            #print(dv)
            if dv["mass"] < 3: continue
            if dv["rxy"] < 4 : continue
            if dv["rxy"] > 300 : continue
            if abs(dv["z"]) > 300 : continue
            #if dv["sumpt"] < 6 : continue
            if dv["sumpt2"] < 10 : continue

            if dv["ntracks"] >= 2 : ndvs2+=1
            if dv["ntracks"] >= 3 : ndvs3+=1
            if dv["ntracks"] >= 4 : ndvs4+=1
            if dv["ntracks"] >= 5 : ndvs5+=1

            if "ndvs" not in dist: 
                if dv["ntracks"] < ntracks : continue 
                dist_array   .append( dv[dist] ) 
                weight_array .append( data["weights"][i] ) 

        ndvs2_array.append(ndvs2)
        ndvs3_array.append(ndvs3)
        ndvs4_array.append(ndvs4)
        ndvs5_array.append(ndvs5)

    if "ndvs2" in dist: return ndvs2_array, data["weights"]
    if "ndvs3" in dist: return ndvs3_array, data["weights"]
    if "ndvs4" in dist: return ndvs4_array, data["weights"]
    if "ndvs5" in dist: return ndvs5_array, data["weights"]
    
    return dist_array,weight_array
def compareSampleDVs(dist="ndvs3",pileup=200):
    
    title = "$p_{\\mathrm{T}}>1.0$ GeV, $|d_{0}|<100$ mm" 
    if "ndvs" in dist: 
        dist_arrays = []
        weight_arrays = []
        labels = samples_dv_labels 
        for sample in samples_dv:
            dist_array,weight_array = dvArray(sample, pileup, dist)
            dist_arrays.append(dist_array)
            weight_arrays.append(weight_array)
        
        outfile = "plots/pileup/compareDVProperties_pileup{}_{}.pdf".format(pileup,dist)
        compare1D(dist_arrays,labels,weight_arrays,outfile,title)
    else : 
        ntracks = [2,3,4,5]
        for ntrack in ntracks: 
            dist_arrays = []
            weight_arrays = []
            labels = samples_dv_labels 
            for sample in samples_dv:
                dist_array,weight_array = dvArray(sample, pileup, dist, ntrack)
                dist_arrays.append(dist_array)
                weight_arrays.append(weight_array)
            
            outfile = "plots/pileup/compareDVProperties_pileup{}_{}_ntrk{}.pdf".format(pileup,dist,ntrack)
            compare1D(dist_arrays,labels,weight_arrays,outfile,title)

    return 


# DV Dependent Dists

dists = []
dists.append("mass")
dists.append("sumpt") 
dists.append("sumpt2")
dists.append("ntracks") 
dists.append("tracks_pt")  
dists.append("rxy") 
dists.append("ndvs2") 
dists.append("ndvs3") 
dists.append("ndvs4") 
dists.append("ndvs5") 

for dist in dists:
    compareSampleDVs(dist)

