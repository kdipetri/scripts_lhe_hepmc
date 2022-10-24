import json
import time
import numpy as np
import ROOT
import random
from pyjet import cluster
from pyjet.testdata import get_event
import mathutils
from util.passTrackTrigger import *

#https://www.quora.com/What-is-matplotlib-use-and-why-do-we-use-them
import matplotlib 
matplotlib.use('pdf') # for speed? 
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
from util.plot_helper import *

prompt_configs = []
prompt_configs.append("pt0.5")
prompt_configs.append("pt1.0")
prompt_configs.append("pt1.5")
prompt_configs.append("pt2.0")

doTest = False    
#doTest = True    


def clusterJets(tracks):

    vectors = np.zeros( len(tracks), dtype=np.dtype([('pT', 'f8'), ('eta', 'f8'), ('phi', 'f8'), ('mass', 'f8'), ('d0', 'f8')]) )

    for i,trk in enumerate(tracks): 
        vectors[i] = (trk["pt"], trk["eta"], trk["phi"], 0.139 , trk["d0"])

    sequence = cluster(vectors, R=0.4, p=-1)
    jets = sequence.inclusive_jets()  # list of PseudoJets

    return jets

def compare1D(arrays,labels,weights,outfile,norm=0):
    if "withbkg" in outfile : norm=1
    bins = get_bins(outfile)
    plt.style.use('seaborn-v0_8-colorblind')
    plt.figure(figsize=(6,5.5))

    for i in range(0,len(arrays)):
        (counts, bins) = np.histogram(arrays[i], bins=bins, weights=weights[i])
        factor = len(arrays[i])
        hist_weights = counts/factor if  norm==1 else counts
        if "SM" in labels[i]: 
            plt.hist(bins[:-1], bins, histtype='stepfilled', color="tab:gray", alpha=0.7, label=labels[i], weights=hist_weights)
        else : 
            plt.hist(bins[:-1], bins, histtype='step', label=labels[i], weights=hist_weights)

    if "hit_t" in outfile:
        ax = plt.axes()
        ax.xaxis.set_major_locator(plt.MaxNLocator(5))
        ax.yaxis.set_major_locator(plt.MaxNLocator(5))

    plt.subplots_adjust(left=0.18, right=0.95, top=0.9, bottom=0.18)
    plt.grid(visible=True, which='major', axis='both', color='gainsboro')

    plt.yscale(yscale(outfile))
    #plt.ylim(-0.05,1.05)
   
    size=20 
    plt.xlabel(xtitle(outfile),fontsize=size, labelpad=size/2)
    plt.ylabel(ytitle(outfile),fontsize=size, labelpad=size/2)
    plt.xticks(fontsize=size-4)
    plt.yticks(fontsize=size-4)
    plt.title(title(outfile),fontsize=size-4)
    plt.legend(prop={'size':size-4,})
    #plt.legend(loc=leg_loc(outfile),prop={'size':size-4,})

    plt.savefig(outfile)
    plt.clf()
    plt.close()
    print(outfile)
    return

def analyzePUevents(pileup=2,sample='qcd'):

    # Get events with correct pileup
    f = open('output/{}_pileup{}_nTrackPV.json'.format(sample,pileup)) 
    data = json.load(f)
    event_tracks = data['event_tracks']
    weight_array = data['weights']
    event_array  = data['events']


    # we need to loop over pileup events
    for i,trks in enumerate(event_tracks): 

        if doTest and i > 100 : break

        if i%1000==0 : print("event number ",i)  

        #evt_dvs = {} 
        z0 = event_array[i]['z0']
    
        # Different displaced configs
        for config in prompt_configs:

            #print(config)

            # Process tracks to form DVs for each config
            tracks = []
            sum_trk_pt = 0
            for trk in trks:

                #print(i,type(trk))

                if passPrompt(trk, z0, cutOpt=config) == 0 : continue

                #print(trk["pt"], trk["eta"], trk["phi"], trk["d0"])

                sum_trk_pt += trk["pt"]
                tracks.append(trk)
        
            # Reconstruct Jets
            jets = clusterJets(tracks) 

            nJets = 0
            ht = 0
            for jet in jets: 
                if jet.pt < 25: continue 
                ntrk = len(jet.constituents_array())
                if ntrk < 1 : continue
                
                ht += jet.pt
                nJets += 1
                #print(jet, len(jet.constituents_array()))

            ## save computed info to event arrays
            event_array[i]["prompt_nJets_" +config] = nJets 
            event_array[i]["prompt_jetht_" +config] = ht 
            event_array[i]["prompt_sumtrkpt_" +config] = sum_trk_pt 



    if doTest: return 

    outdata = {
        "weights"   : weight_array,
        "events"    : event_array,
    }
    

    with open('output/analyzed_{}_nTrack_pileup{}.json'.format(sample,pileup), 'w') as fp:
        json.dump(outdata, fp)

    return



samples = []
samples.append("suep_mMed-600_mDark-1.0_temp-1.0") 
samples.append("suep_mMed-200_mDark-1.0_temp-1.0") 
samples.append("qcd") 
pileups = [200]

for pileup in pileups:
    for sample in samples:
        analyzePUevents(pileup,sample)

