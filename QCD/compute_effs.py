import json
import time
import numpy as np

#https://www.quora.com/What-is-matplotlib-use-and-why-do-we-use-them
import matplotlib 
matplotlib.use('pdf') # for speed? 
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator

from plot_helper import *


def get_array(mass,lifetime,dist):
    f = open('output/signal_{}_{}.json'.format(mass,lifetime)) 
    data = json.load(f)
    dist_array = [ track[dist] for track in data["tracks"] ]
    f.close()
    return dist_array

def get_bkg_array(dist):
    f = open('output/qcd.json') 
    data = json.load(f)
    dist_array = [ track[dist] for track in data["tracks"] ]
    f.close()
    return dist_array

def compare1D(arrays,labels,outfile,norm=0):
    if "withbkg" in outfile : norm=1
    bins = get_bins(outfile)
    plt.style.use('seaborn-colorblind')
    plt.figure(figsize=(6,5.5))

    for i in range(0,len(arrays)):
        (counts, bins) = np.histogram(arrays[i], bins=bins)
        factor = len(arrays[i])
        if norm==1: 
            if "SM" in labels[i]: 
                plt.hist(bins[:-1], bins, histtype='stepfilled', color="tab:gray", alpha=0.7, label=labels[i], weights=counts/factor)
            else : 
                plt.hist(bins[:-1], bins, histtype='step', label=labels[i], weights=counts/factor)
        else : 
            if "SM" in labels[i]: 
                plt.hist(bins[:-1], bins, histtype='stepfilled', color="tab:gray", alpha=0.7, label=labels[i], weights=counts)
            else : 
                plt.hist(bins[:-1], bins, histtype='step', label=labels[i], weights=counts)

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
    print(outfile)
    return

def plotTracks(dist):

    arrays = []
    labels = []

    # Just plot QCD for now 
    arrays.append(get_bkg_array(dist))
    labels.append("SM particles")
     
    outfile="plots/track_{}.pdf".format(dist)
    compare1D(arrays,labels,outfile)

    return


# Compare stau displacement properties for lifetimes
plotTracks("pt")
plotTracks("eta")
plotTracks("phi")
plotTracks("d0")
plotTracks("prod_rxy")
plotTracks("decay_rxy")
