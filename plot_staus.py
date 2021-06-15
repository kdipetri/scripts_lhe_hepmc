import json
import numpy as np
import matplotlib.pyplot as plt

def get_bins(dist):
    if "_pt" in dist: return np.linspace(0,1000,20)
    if "_eta" in dist: return np.linspace(-4,4,20)
    if "_phi" in dist: return np.linspace(-4,4,20)
    if "_Lxy" in dist: return np.linspace(0,1000,100)
    if "_betagamma" in dist: return np.linspace(0,10,20)
    return np.linspace(0,1000,20)

def get_array(mass,lifetime,dist):
    f = open('output/stau_{}_{}.json'.format(mass,lifetime)) 
    data = json.load(f)
    dist_array = data[dist]
    f.close()
    return dist_array

def compare1D(arrays,labels, bins, outfile):
    fig, ax = plt.subplots(figsize =(8, 6))

    for i,array in enumerate(arrays):
        ax.hist(array, bins, alpha=0.5, label=labels[i])

    ax.legend(loc='upper right')
    #ax.set_ylabel("charged particles")
    #ax.set_xlabel("$p_{T}^{charged} [GeV]$")
    plt.savefig(outfile)
    return

def compareMass(dist,lifetime="1ns"):
    masses = ["100","200","300","400","500","600"]

    arrays = []
    labels = []
    for mass in masses:
        arrays.append(get_array(mass,lifetime,dist))
        labels.append("M={} GeV, {}".format(mass,lifetime))

    bins=get_bins(dist)
    outfile="plots/compareMass_{}_{}.png".format(lifetime,dist)
    compare1D(arrays,labels,bins,outfile)

    return

def compareLifetime(dist,mass="600"):
    lifetimes = ["0p001ns","0p01ns","0p1ns","1ns"]

    arrays = []
    labels = []
    for lifetime in lifetimes:
        arrays.append(get_array(mass,lifetime,dist))
        labels.append("M={} GeV, {}".format(mass,lifetime))

    bins=get_bins(dist)
    outfile="plots/compareLifetime_{}_{}.png".format(lifetime,dist)
    compare1D(arrays,labels,bins,outfile)

    return

compareLifetime("stau_lxy")
compareLifetime("stau_decaytime")

#compareMass("stau_eta") 
#compareMass("stau_phi") 
#compareMass("stau_pt" ) 
#compareMass("stau_m"  ) 
#compareMass("stau_lxy") 
#compareMass("stau_betagamma") 
#compareMass("stau_decaytime") 

