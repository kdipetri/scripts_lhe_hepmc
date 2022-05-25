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
    f = open('output/stau_{}_{}.json'.format(mass,lifetime)) 
    data = json.load(f)
    dist_array = [ stau[dist] for stau in data["staus"] ]
    f.close()
    return dist_array

def get_bkg_array(dist,mass=100,lifetime="stable"):
    f = open('output/bkg_{}_{}.json'.format(mass,lifetime)) 
    data = json.load(f)
    dist_array = [ stau[dist] for stau in data["staus"] ]
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
        if "SM" in labels[i]: 
            plt.hist(bins[:-1], bins, histtype='stepfilled', color="tab:gray", alpha=0.7, label=labels[i], weights=counts/factor)
        else : 
            plt.hist(bins[:-1], bins, histtype='step', label=labels[i], weights=counts/factor)

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
    plt.legend(loc=leg_loc(outfile),prop={'size':size-4,})

    plt.savefig(outfile)
    plt.clf()
    print(outfile)
    return

def compareMass(dist,lifetime="stable"):
    masses = ["100","500","1000"]

    arrays = []
    labels = []
    for mass in masses:
        arrays.append(get_array(mass,lifetime,dist))
        labels.append("$m_{\\tilde{\\tau}}$"+" = {} GeV".format(mass))

    # no bkg
    outfile="plots/compareMass_{}_{}.pdf".format(lifetime,dist)
    compare1D(arrays,labels,outfile)

    # add bkg
    arrays.append(get_bkg_array(dist))
    labels.append("SM particles")
    outfile="plots/compareMass_{}_{}_withbkg.pdf".format(lifetime,dist)
    compare1D(arrays,labels,outfile)

    return


def compareLifetime(dist,mass="500"):
    lifetimes = ["0p01ns","0p1ns","1ns","10ns","stable"]

    arrays = []
    labels = []
    for lifetime in lifetimes:
        arrays.append(get_array(mass,lifetime,dist))
        labels.append("$m_{\\tilde{\\tau}}$"+" = {} GeV, {}".format(mass,lifetime))
        print(lifetime)

    outfile="plots/compareLifetime_{}_{}.pdf".format(mass,dist)
    compare1D(arrays,labels,outfile)
    return

def compareTimeRes(dist,mass="600",lifetime = "1ns"):
    methods = []
    methods.append("_tHit0;tBS0;zBS0") # truth  
    methods.append("_tHit50;tBS0;zBS0") # hit res only 
    methods.append("_tHit0;tBS200;zBS0") # beamspot only  
    methods.append("_tHit0;tBS0;zBS50") # z0 only  
    methods.append("_tHit50;tBS200;zBS0") # hit + beamspot res  
    methods.append("_tHit50;tBS200;zBS50") # all

    labels = []
    labels.append("truth")
    labels.append("50ps hit")
    labels.append("200ps beamspot")
    labels.append("z0 unknown")
    labels.append("50ps hit, 200ps beamspot")
    labels.append("all effects")
    
    arrays = []
    for method in methods:
        arrays.append(get_array(mass,lifetime,dist+method))

    outfile="plots/compareMethod_{}_{}_{}.pdf".format(mass,lifetime,dist)
    compare1D(arrays,labels,outfile)
    return

# Compare stau displacement properties for lifetimes
compareLifetime("lxy",500)
compareLifetime("lxy",100)
compareLifetime("z",500)
compareLifetime("z",100)
compareLifetime("decaytime",500)
compareLifetime("decaytime",100)

# Compare stau kinematics for different masses, with and without bkg
compareMass("eta","1ns") 
compareMass("phi","1ns") 
compareMass("pt" ,"1ns") 
compareMass("m"  ,"1ns") 
compareMass("lxy","1ns") 
compareMass("betagamma","1ns") 
compareMass("decaytime","1ns") 
compareMass("isolation","1ns")

#
s="_tHit50;tBS200;zBS0" 
compareMass("hit_time"+s)
compareMass("hit_delay"+s)
compareMass("hit_beta"+s)
compareMass("hit_betaRes"+s)
compareMass("hit_invBeta"+s)
compareMass("hit_invBetaRes"+s)
compareMass("hit_mass"+s)
compareMass("hit_massRes"+s)

s="_tHit50;tBS0;zBS0" 
compareMass("hit_time"+s)
compareMass("hit_delay"+s)
compareMass("hit_beta"+s)
compareMass("hit_betaRes"+s)
compareMass("hit_invBeta"+s)
compareMass("hit_invBetaRes"+s)
compareMass("hit_mass"+s)
compareMass("hit_massRes"+s)

# compare timing resolution methods
#compareTimeRes("hit_time")
#compareTimeRes("hit_delay")
#compareTimeRes("hit_beta")
#compareTimeRes("hit_betaRes")
#compareTimeRes("hit_mass")
#compareTimeRes("hit_massRes")
