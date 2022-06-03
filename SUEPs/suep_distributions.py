#!/usr/bin/env python

import json
import numpy as np
import matplotlib 
matplotlib.use('pdf') # for speed? 
import matplotlib.pyplot as plt

f = open('SUEP_effieciencies.json',)
data = json.load(f)
f.close()

masses  = [125, 200, 400, 600, 800, 1000]
ntracks = [100, 150, 200]
pts     = [0.5, 1, 2]
pTs     = ["05", "1", "2"]

def get_bins(dist):
    # start, stop, stepsize
    if "compare_ht"     in dist: return np.arange(0, 2000, 50)
    if "compare_nTrack" in dist: 
        xmax=800
        nbins=50
        if   "mass200" in dist : xmax= 250
        elif "mass800" in dist : xmax= 500
        elif "pt05"    in dist : xmax= 500
        elif "pt1"     in dist : xmax= 300
        elif "pt2"     in dist : xmax= 100 
        return np.arange(0, xmax, float(xmax)/nbins)
    if "compare_pt" in dist: return np.arange(0,6,0.1)
    else : return np.arange(0, 3000, 100)

def leg_loc(dist):
    return "upper right"

def xlabel(dist):
    if "compare_ht" in dist: return "$H_{\\mathsf{T}}$ (GeV)"
    elif "compare_nTrack" in dist: return "$n_{\\mathsf{Track}}$"
    elif "compare_pt" in dist: return "$p_{\mathsf{T}}$ (GeV)"
    else : return ""

def ylabel(dist):
    if "compare_pt" in dist: return "Tracks (AU)"
    else : return "Events (AU)"

def yscale(dist):
    #if "compare_pt" in dist: return "log"
    #else : return "linear"
    return "linear"

def ymax(dist):
    if "compare_pt" in dist: return 0.12
    elif "compare_nTrack_for_diffmass" in dist: return 0.23
    #elif "compare_ht" in dist: return 0.5
    else : return -1

def compare1D(arrays,labels,title,outfile,norm=0):

    print(outfile)

    bins = get_bins(outfile)
    plt.style.use('seaborn-colorblind')
    plt.figure(figsize=(6,5.5))

    for i in range(0,len(arrays)):
        (counts, bins) = np.histogram(arrays[i], bins=bins)
        factor = len(arrays[i])
        plt.hist(bins[:-1], bins, histtype='step', label=labels[i], weights=counts/factor)

    plt.subplots_adjust(left=0.18, right=0.95, top=0.9, bottom=0.18)
    plt.grid(visible=True, which='major', axis='both', color='gainsboro')

    plt.yscale(yscale(outfile))
    if ymax(outfile) != -1: plt.ylim(0,ymax(outfile))
    #plt.ylim(-0.05,1.05)

    ax = plt.axes()
    ax.xaxis.set_major_locator(plt.MaxNLocator(6))
    ax.yaxis.set_major_locator(plt.MaxNLocator(6))
   
    size=20 
    
    plt.xlabel(xlabel(outfile), fontsize=size, labelpad=size/2)
    plt.ylabel(ylabel(outfile), fontsize=size, labelpad=size/2)
    plt.xticks(fontsize=size-4)
    plt.yticks(fontsize=size-4)
    plt.title(title,fontsize=size-4)

    if len(arrays) > 4 and "compare_nT" in outfile : 
        plt.legend(loc=leg_loc(outfile),prop={'size':size-4,}, ncol=2, borderpad=0.2, handlelength=1, handletextpad=0.5, columnspacing=0.8)
    else : plt.legend(loc=leg_loc(outfile),prop={'size':size-4,}, handlelength=1)

    plt.savefig(outfile)
    plt.clf()
    return

#
#HT plots for different pT thresholds, for fixed mass
#
def comparePt(dist):

    for i,mass in enumerate(masses):
        title = "$m_{\\Phi}}$"+" = {} GeV".format(mass)
        arrays = []
        labels = []

        for j,pt in enumerate(pTs):
            array = data[dist][i][dist+"_"+pt]
            arrays.append(array)
            labels.append("$p_{\\mathsf{T}}$ > "+"{} GeV".format(pts[j]) )


        outfile="plots/dists/compare_{}_for_diffpt_mass{}.pdf".format(dist,mass)
        compare1D(arrays,labels,title,outfile)

    return

comparePt("ht")
comparePt("nTrack")

def compareMasses(dist,ptbin=-1):

    labels = []
    arrays = []
    for i,mass in enumerate(masses):

        if ptbin==-1: #comparing pT for mediator mass 
            array = data["trackPt"][i][dist]
            title = ""

        else : 
            array = data[dist][i][dist+"_"+pTs[ptbin]]
            title = "$p_{\\mathsf{T}}$ >"+" {} GeV".format(pts[ptbin])

        arrays.append(array)
        labels.append("$m_{\\Phi}$ = "+"{} GeV".format(mass) )


    outfile="plots/dists/compare_{}_for_diffmass{}.pdf".format(dist,"" if ptbin==-1 else "_pt"+pTs[ptbin])
    compare1D(arrays,labels,title,outfile)

    return

compareMasses("pt")
compareMasses("ht",0)
compareMasses("ht",1)
compareMasses("ht",2)
compareMasses("nTrack",0)
compareMasses("nTrack",1)
compareMasses("nTrack",2)
