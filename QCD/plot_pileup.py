import json
import time
import numpy as np
import ROOT

#https://www.quora.com/What-is-matplotlib-use-and-why-do-we-use-them
import matplotlib 
matplotlib.use('pdf') # for speed? 
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
from util.plot_helper import *

# Displaced Vertex Samples
samples = []
samples.append("hscp_qcd")
samples.append("qcd_nTrack")
samples.append("qcd")
samples.append("suep_mMed-200_mDark-1.0_temp-1.0_nTrack")
samples.append("suep_mMed-600_mDark-1.0_temp-1.0_nTrack")
samples.append("higgsportal_125_40_0p1ns")
samples.append("higgsportal_125_55_1ns")
samples.append("stau_100_stable")
samples.append("stau_300_stable")
samples.append("stau_300_0p1ns")
samples.append("stau_300_1ns")

# Displaced Vertex Samples
samples_dv = ["qcd","higgsportal_125_40_0p1ns","higgsportal_125_55_1ns"]
samples_dv_labels = ["QCD", "$m_{S}=40$ GeV, $\\tau_{S}=0.1$ ns", "$m_{S}=55$ GeV, $\\tau_{S}=1$ ns" ]

# Displaced Track Samples
samples_trk = ["qcd","stau_300_0p1ns","stau_300_1ns" ]
samples_trk_labels = ["QCD", "$m_{\\tilde{\\tau}}=300$ GeV, $\\tau_{\\tilde{\\tau}}=0.1$ ns", "$m_{\\tilde{\\tau}}=300$ GeV, $\\tau_{\\tilde{\\tau}}=1$ ns" ]

# SUEP Samples
samples_suep = ["qcd_nTrack","suep_mMed-200_mDark-1.0_temp-1.0_nTrack","suep_mMed-600_mDark-1.0_temp-1.0_nTrack" ]
samples_suep_labels = ["QCD", "$m_{S}=200$ GeV", "$m_{S}=600$ GeV" ]

# HSCP Samples
samples_HSCP = ["hscp_qcd","stau_100_stable","stau_300_stable" ]
samples_HSCP_labels = ["QCD", "$m_{\\tilde{\\tau}}=100$ GeV, stable","$m_{\\tilde{\\tau}}=300$ GeV, stable" ]

# Prompt track selections
prompt_configs = []
prompt_configs.append("pt1.0")
prompt_configs.append("pt1.5")
prompt_configs.append("pt2.0")

# Displaced track selections
displaced_configs=[]
displaced_configs.append("pt1.0;d050")
displaced_configs.append("pt2.0;d050")
displaced_configs.append("pt10.0;d050")
displaced_configs.append("pt1.0;d0100")
displaced_configs.append("pt2.0;d0100")
displaced_configs.append("pt10.0;d0100")

pileups = [200] 

# pre-process input data to speedup??
input_data = {} 
for sample in samples: 
    for pileup in pileups:
        print(sample+"_"+str(pileup))
        f = open('output/analyzed_{}_pileup{}.json'.format(sample, pileup),"r") 
        input_data[sample+"_"+str(pileup)] = json.load(f)
        f.close()   

def configString(cuts):
    pt_str = "$p_{\mathsf{T}} > $"
    d0_str = "$d_{0} < $"
    
    if "HSCP" in cuts: 
        pt_str += cuts.split("_")[-2] 
        d0_str += "1"
    elif "prompt" in cuts: 
        d0_str += "1"
        pt_str += cuts.split("_")[-1].strip("pt")
    else : # displaced
        cut = cuts.split("_")[-1]
        for c in cut.split(";"):
            if "pt" in c : pt_str += c[2:]  
            if "d0" in c : d0_str += c[2:]


    outstring = pt_str + " GeV, "+ d0_str + " mm"
    return outstring

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
    
def dvArray(sample,pileup=0,dist="nDVs_3trks_pt1.0;d050"):

    data = input_data[sample+"_"+str(pileup)]
    weight_array = [] 
    dist_array = []

    ndvs3_array = []
    ndvs4_array = []
    ndv_weight_array = [] 
    for i,evt in enumerate(data["event_dvs"]):
        ndvs3 = 0
        ndvs4 = 0
        #print(i,evt)
        for dv in evt: 
            #print(dv)
            if dv["mass"] < 3: continue
            if dv["rxy"] < 4 : continue
            if dv["rxy"] > 300 : continue
            if abs(dv["z"]) > 300 : continue
            if dv["sumpt"] < 6 : continue
            #if dv["sumpt2"] < 8 : continue

            if dv["ntracks"] >= 3 : ndvs3+=1
            if dv["ntracks"] >= 4 : ndvs4+=1

            if "ndvs" not in dist: 
                if dv["ntracks"] <= 2 : continue 
                dist_array   .append( dv[dist] ) 
                weight_array .append( data["weights"][i] ) 

        ndvs3_array.append(ndvs3)
        ndvs4_array.append(ndvs4)

    if "ndvs3" in dist: return ndvs3_array, data["weights"]
    if "ndvs4" in dist: return ndvs4_array, data["weights"]
    
    return dist_array,weight_array

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
        if "mass" in outfile :  bins = np.linspace(0,20,200)
        if "rxy" in outfile :  bins = np.linspace(0,300,300)

    for i in range(0,len(arrays)):
        (counts, bins) = np.histogram(arrays[i], bins=bins, weights=weights[i])
        factor = sum(weights[i])
        hist_weights = counts/float(factor) if  norm==1 else counts
        if norm==1 and "QCD" in labels[i]: 
            plt.hist(bins[:-1], bins, histtype='stepfilled', color="tab:gray", alpha=0.7, label=labels[i], weights=hist_weights)
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
    plt.ylabel(ytitle(outfile) + " AU",fontsize=size, labelpad=size/2)
    plt.xticks(fontsize=size-4)
    plt.yticks(fontsize=size-4)
    plt.title(title,fontsize=size-4)
    plt.legend(prop={'size':size-5,})

    plt.savefig(outfile)
    plt.clf()
    plt.close()
    print(outfile)
    return


def compareSampleJets(dist="nDVs_3trks_pt1.0;d050",pileup=200):
    
    dist_arrays = []
    weight_arrays = []
    labels = samples_dv_labels 
    for sample in samples_dv:
        dist_array,weight_array = jetArray(sample, pileup, dist)
        dist_arrays.append(dist_array)
        weight_arrays.append(weight_array)
        
    outfile = "plots/pileup/compareDisJets_pileup{}_{}.pdf".format(pileup,dist)
    title = configString(dist)
    compare1D(dist_arrays,labels,weight_arrays,outfile,title)
    return 

dists = []
dists.append("mass")
dists.append("pt") 
dists.append("eta")
dists.append("ntrk") 
dists.append("nPVConstit")  
dists.append("nPromptConstit") 
dists.append("nDisplacedConstit") 
dists.append("fracPV")
dists.append("fracDisplaced")

#for dist in dists:
#    compareSampleJets(dist)


def compareSampleDVs(dist="nDVs_3trks_pt1.0;d050",pileup=200):
    
    print("DV ", dist)
    dist_arrays = []
    weight_arrays = []
    labels = samples_dv_labels 
    for sample in samples_dv:
        dist_array,weight_array = dvArray(sample, pileup, dist)
        dist_arrays.append(dist_array)
        weight_arrays.append(weight_array)
        
    outfile = "plots/pileup/compareDVProperties_pileup{}_{}.pdf".format(pileup,dist)
    title = configString(dist)
    compare1D(dist_arrays,labels,weight_arrays,outfile,title)
    return 


def compareSamplePerDist(pileup=200,dist="nDVs_3trks_pt1.0;d050"):
    
    dist_arrays = []
    weight_arrays = []
    labels = []
    if "prompt" in dist: 
        for sample in samples_suep:
            dist_array,weight_array = distArray(sample, pileup, dist)
            dist_arrays.append(dist_array)
            weight_arrays.append(weight_array)
            
        outfile = "plots/pileup/compareSUEP_for_pileup{}_{}.pdf".format(pileup,dist)
        title = configString(dist)
        compare1D(dist_arrays,samples_suep_labels,weight_arrays,outfile,title)

    elif "HSCP" in dist: 
        for sample in samples_HSCP:
            dist_array,weight_array = distArray(sample, pileup, dist)
            dist_arrays.append(dist_array)
            weight_arrays.append(weight_array)
            
        outfile = "plots/pileup/compareHSCP_for_pileup{}_{}.pdf".format(pileup,dist)
        title = configString(dist)
        compare1D(dist_arrays,samples_HSCP_labels,weight_arrays,outfile,title)

    elif "nDVs" in dist or "nJets" in dist or "ptsum" in dist: 
        for sample in samples_dv:
            dist_array,weight_array = distArray(sample, pileup, dist)
            dist_arrays.append(dist_array)
            weight_arrays.append(weight_array)
            
        outfile = "plots/pileup/compareDVs_for_pileup{}_{}.pdf".format(pileup,dist)
        title = configString(dist)
        compare1D(dist_arrays,samples_dv_labels,weight_arrays,outfile,title)

    elif "nTrack_pass_displaced" in dist: 
        tmp_samples = samples_trk
        tmp_labels  = samples_trk_labels
        if "pt1.0" in dist or "pt2.0" in dist: 
            print("using higgs!")
            tmp_samples = samples_dv
            tmp_labels  = samples_dv_labels
        for sample in tmp_samples:
            dist_array,weight_array = distArray(sample, pileup, dist)
            dist_arrays.append(dist_array)
            weight_arrays.append(weight_array)
            
        outfile = "plots/pileup/compareDTs_for_pileup{}_{}.pdf".format(pileup,dist)
        title = configString(dist)
        compare1D(dist_arrays,tmp_labels,weight_arrays,outfile,title)

    return 


# DV Dependent Dists
dists = []
dists.append("mass")
dists.append("sumpt") 
dists.append("sumpt2")
dists.append("ntracks") 
dists.append("tracks_pt")  
dists.append("rxy") 
dists.append("ndvs3") 
dists.append("ndvs4") 

for dist in dists:
    compareSampleDVs(dist)


# Premade distributions
#pu=200
#dists = []
#dists.append("nDVs_2trks")
#dists.append("nDVs_3trks")
#dists.append("nDVs_4trks")
#dists.append("nDVs_5trks")

#for cfg in displaced_configs:
#    compareSamplePerDist(pu,"nTrack_pass_displaced_"+cfg)
#    compareSamplePerDist(pu,"displacedTrack_ptsum_"+cfg)
#    compareSamplePerDist(pu,"displacedTrack_ptsum2_"+cfg)
#    for dist in dists:
#        compareSamplePerDist(pu,dist+"_"+cfg)
#
#
## SUEP
#for cfg in prompt_configs:
#    compareSamplePerDist(pu,"nTrack_pass_prompt_"+cfg)
#    compareSamplePerDist(pu,"prompt_nJets_"+cfg)   
#    compareSamplePerDist(pu,"prompt_jetht_" +cfg)  
#    compareSamplePerDist(pu,"prompt_sumtrkpt_" +cfg)  
#compareSamplePerDist(pu,"nTrack_pass_prompt_pt0.5")
#
## HSCP
#for cfg in prompt_configs:
#    compareSamplePerDist(pu,"nHSCP_10_"+cfg)
#    compareSamplePerDist(pu,"nHSCP_25_"+cfg)
#    compareSamplePerDist(pu,"nHSCP_50_"+cfg)
#    compareSamplePerDist(pu,"nHSCP_100_"+cfg)
#    compareSamplePerDist(pu,"nHSCP_highBeta_10_"+cfg)
#    compareSamplePerDist(pu,"nHSCP_highBeta_25_"+cfg)
#    compareSamplePerDist(pu,"nHSCP_highBeta_50_"+cfg)
#    compareSamplePerDist(pu,"nHSCP_highBeta_100_"+cfg)
#    compareSamplePerDist(pu,"nHSCP_highM_10_"+cfg)
#    compareSamplePerDist(pu,"nHSCP_highM_25_"+cfg)
#    compareSamplePerDist(pu,"nHSCP_highM_50_"+cfg)
#    compareSamplePerDist(pu,"nHSCP_highM_100_"+cfg)
