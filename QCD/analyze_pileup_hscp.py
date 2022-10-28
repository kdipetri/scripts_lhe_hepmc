import json
import time
import numpy as np
import ROOT
import random
from pyjet import cluster
from pyjet.testdata import get_event
import mathutils

#https://www.quora.com/What-is-matplotlib-use-and-why-do-we-use-them
import matplotlib 
matplotlib.use('pdf') # for speed? 
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
from util.plot_helper import *
from util.get_timing import *
from util.passTrackTrigger import *

prompt_configs = []
#prompt_configs.append("pt0.5")
prompt_configs.append("pt1.0")
prompt_configs.append("pt1.5")
prompt_configs.append("pt2.0")


doTest = False    
#doTest = True    

def get_iso(hscp,tracks,dR_cut=0.4):
    # This function computes the isolation of "particle" 
    # Isolation = scalar sum of status 1 particles in a cone of dR_cut=0.3 around "partcle"
    # Divided by the "particle" momentum

    v1 = ROOT.TLorentzVector()
    v1.SetPtEtaPhiM(hscp["pt"], hscp["eta"], hscp["phi"], 0.139)
    v2 = ROOT.TLorentzVector()

    # Loop over all particles
    sum_pt = 0
    for trk in tracks:
       
        if hscp==trk: continue
        v2.SetPtEtaPhiM(trk["pt"], trk["eta"], trk["phi"], 0.139)
        
        dR = v1.DeltaR(v2) 
        if dR > dR_cut : continue # only keep in dR cone
    
        sum_pt += trk["pt"] 

    iso = sum_pt / hscp["pt"] 
    return iso 

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
    f = open('output/{}_pileup{}.json'.format(sample,pileup)) 
    data = json.load(f)
    event_tracks = data['event_tracks']
    weight_array = data['weights']
    event_array  = data['events']


    # we need to loop over pileup events
    for i,trks in enumerate(event_tracks): 

        if doTest and i > 100 : break

        if i%1000==0 : print("event number ",i)  

        #evt_dvs = {} 
        z0 = event_array[i]["z0"]
    
        # Different displaced configs
        for config in prompt_configs:

            #print(config)
            ptcut  = float(config.strip("pt"))

            # Process tracks to form DVs for each config
            tracks = []
            hscp_tracks = []
            sum_trk_pt = 0
            for j,trk in enumerate(trks):

                if passPrompt(trk, z0, cutOpt=config) == 0 : continue

                #print(trk["pt"], trk["eta"], trk["phi"], trk["d0"])

                sum_trk_pt += trk["pt"]
                tracks.append(trk)

                if trk["pt"] > 10. : hscp_tracks.append(trk)  
        
            # compute hscp track isolation
            
            n_hscp_10=0
            n_hscp_25=0
            n_hscp_50=0
            n_hscp_100=0
            n_hscp_highBeta_10=0
            n_hscp_highBeta_25=0
            n_hscp_highBeta_50=0
            n_hscp_highBeta_100=0
            n_hscp_highM_10=0
            n_hscp_highM_25=0
            n_hscp_highM_50=0
            n_hscp_highM_100=0
            for hscp in hscp_tracks:
                iso = get_iso(hscp,tracks) 
                hscp = getHit(hscp)
                if iso > 0.05 : continue
                if hscp["pt"] > 10. : n_hscp_10+=1
                if hscp["pt"] > 25. : n_hscp_25+=1
                if hscp["pt"] > 50. : n_hscp_50+=1
                if hscp["pt"] > 100.: n_hscp_100+=1
                if hscp["hit_beta"] < 0.98 : 
                    if hscp["pt"] > 10. : n_hscp_highBeta_10+=1
                    if hscp["pt"] > 25. : n_hscp_highBeta_25+=1
                    if hscp["pt"] > 50. : n_hscp_highBeta_50+=1
                    if hscp["pt"] > 100.: n_hscp_highBeta_100+=1
                if hscp["hit_mass"] > 20. : 
                    if hscp["pt"] > 10. : n_hscp_highM_10+=1
                    if hscp["pt"] > 25. : n_hscp_highM_25+=1
                    if hscp["pt"] > 50. : n_hscp_highM_50+=1
                    if hscp["pt"] > 100.: n_hscp_highM_100+=1
                
                         
            event_array[i]["nHSCP_10_" +config] = n_hscp_10 
            event_array[i]["nHSCP_25_" +config] = n_hscp_25 
            event_array[i]["nHSCP_50_" +config] = n_hscp_50 
            event_array[i]["nHSCP_100_" +config] = n_hscp_100 
            event_array[i]["nHSCP_highM_10_" +config] = n_hscp_highM_10 
            event_array[i]["nHSCP_highM_25_" +config] = n_hscp_highM_25 
            event_array[i]["nHSCP_highM_50_" +config] = n_hscp_highM_50 
            event_array[i]["nHSCP_highM_100_"+config] = n_hscp_highM_100 
            event_array[i]["nHSCP_highBeta_10_" +config] = n_hscp_highBeta_10 
            event_array[i]["nHSCP_highBeta_25_" +config] = n_hscp_highBeta_25 
            event_array[i]["nHSCP_highBeta_50_" +config] = n_hscp_highBeta_50 
            event_array[i]["nHSCP_highBeta_100_"+config] = n_hscp_highBeta_100 

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
    

    if "qcd" in sample: sample += "_hscp"
    with open('output/analyzed_{}_pileup{}.json'.format(sample,pileup), 'w') as fp:
        json.dump(outdata, fp)

    print( "output saved" )
    return



samples = []
samples.append("qcd_2TeV") 
#samples.append("stau_300_stable") 
#samples.append("stau_100_stable") 
pileups = [200]

for pileup in pileups:
    for sample in samples:
        analyzePUevents(pileup,sample)

