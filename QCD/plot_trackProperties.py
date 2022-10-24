import json
import time
import numpy as np

#https://www.quora.com/What-is-matplotlib-use-and-why-do-we-use-them
import matplotlib 
matplotlib.use('pdf') # for speed? 
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator

from util.plot_helper import *

f = open('output/qcd.json') 
data = json.load(f)

def get_track_array(dist):
    dist_array   = [ track[dist]     for track in data["tracks"] ]
    weight_array = [ track["weight"] for track in data["tracks"] ]
    #dist_array = np.array(dist_array)
    #weight_array = np.array(weight_array)
    #print(dist_array.shape, weight_array.shape)
    f.close()
    return dist_array, weight_array

def get_event_array(dist,pileup=0):
    dist_array   = [ event[dist]     for event in data["events"] ]
    weight_array = [ event["weight"] for event in data["events"] ]
    f.close()
    
    if pileup<2:
        return dist_array, weight_array
    else : 
        # convert weights to rough probabilities
        # inv_weights = [ 1.0/x for x in weight_array ] 
        sumweights = sum(weight_array)
        prob_array = [ x/sumweights for x in weight_array ]
        #print("inverse weights")
        #for i in range(0,10):
        #    print(weight_array[i], prob_array[i])

        # add ntracks from pile-up events
        pileup_array = dist_array 
        size = len(dist_array)
        for x in range(1,pileup):
            new_array = np.random.choice(dist_array,size,p=prob_array) 
            #print('pu evt', x, new_array[0:10])
            pileup_array = [ sum(evt) for evt in zip(pileup_array,new_array) ]  
        
        #print("pileup events, ",dist)
        #for i in range(10000,10010):
        #    print(dist_array[i], new_array[i], pileup_array[i]) 

        # plot weights to double check
        plt.figure(figsize=(6,5.5))
        plt.hist(prob_array, histtype='step')
        size=20 
        plt.xlabel('weight',fontsize=size, labelpad=size/2)
        plt.ylabel('events',fontsize=size, labelpad=size/2)
        plt.xticks(fontsize=size-4)
        plt.yticks(fontsize=size-4)
        plt.subplots_adjust(left=0.18, right=0.95, top=0.9, bottom=0.18)
        plt.grid(visible=True, which='major', axis='both', color='gainsboro')
        plt.yscale('log')
        plt.savefig('plots/normalizedweights.pdf')
        plt.clf()
        plt.close()

        # plot pileup-event array to double check
        plt.figure(figsize=(6,5.5))
        plt.hist(new_array, histtype='step')
        size=20 
        plt.xlabel('ntracks',fontsize=size, labelpad=size/2)
        plt.ylabel('events' ,fontsize=size, labelpad=size/2)
        plt.xticks(fontsize=size-4)
        plt.yticks(fontsize=size-4)
        plt.subplots_adjust(left=0.18, right=0.95, top=0.9, bottom=0.18)
        plt.grid(visible=True, which='major', axis='both', color='gainsboro')
        plt.yscale('log')
        plt.savefig('plots/new_array_{}.pdf'.format(dist))
        plt.clf()
        plt.close()

        return pileup_array, weight_array

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

def plotTracks(dist):

    arrays = []
    labels = []
    weights = []

    # Just plot QCD for now 
    dist_array,weight_array = get_track_array(dist)

    arrays .append(dist_array)
    weights.append(weight_array)
    labels .append("SM particles")
     
    outfile="plots/track_{}.pdf".format(dist)
    compare1D(arrays,labels,weights,outfile)

    return


def comparePrompt(dist,pileup=0):
    pts = []
    pts.append("pt0.5")
    pts.append("pt1.0")
    pts.append("pt1.5")
    pts.append("pt2.0")
    
    labels = []
    arrays = []
    weights = []
    
    for pt in pts:
        dist = "nTrack_pass_prompt_"+pt
        label = "$p_{T}$ > "+pt.strip("pt")+" GeV"

        dist_array,weight_array = get_event_array(dist,pileup)

        arrays .append(dist_array)
        weights.append(weight_array)
        labels .append(label)

    outfile="plots/comparePrompt_nTrack.pdf"
    if pileup>0: outfile = "plots/comparePrompt_nTrack_pileup{}.pdf".format(pileup)
    compare1D(arrays,labels,weights,outfile)
    
def compareDisplaced(dist,pileup=0):
    pts = []
    pts.append("pt0.5;d050")
    pts.append("pt1.0;d050")
    pts.append("pt2.0;d050")
    pts.append("pt5.0;d050")
    pts.append("pt10.0;d050")
    
    labels = []
    arrays = []
    weights = []
    
    for pt in pts:
        dist = "nTrack_pass_displaced_"+pt
        label = "$p_{T}$ > "+pt.split(";")[0].strip("pt")+" GeV"

        dist_array,weight_array = get_event_array(dist,pileup)

        arrays .append(dist_array)
        weights.append(weight_array)
        labels .append(label)

    outfile="plots/compareDisplaced_nTrack_scanpt.pdf"
    if pileup>0: outfile = "plots/compareDisplaced_nTrack_pileup{}.pdf".format(pileup)
    compare1D(arrays,labels,weights,outfile)

# Compare stau displacement properties for lifetimes
#plotTracks("pt")
#plotTracks("eta")
#plotTracks("phi")
#plotTracks("d0")
#plotTracks("prod_rxy")
#plotTracks("decay_rxy")

comparePrompt("ntrack")
comparePrompt("ntrack",pileup=2)
comparePrompt("ntrack",pileup=3)
comparePrompt("ntrack",pileup=4)
comparePrompt("ntrack",pileup=5)

compareDisplaced("ntrack")
compareDisplaced("ntrack",pileup=100)
compareDisplaced("ntrack",pileup=200)
