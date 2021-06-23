import json
import time
import numpy as np
#https://www.quora.com/What-is-matplotlib-use-and-why-do-we-use-them
import matplotlib 
matplotlib.use('pdf') # for speed? 
import matplotlib.pyplot as plt

def ytitle(dist):
    return "staus"

def xtitle(dist):
    if "_pt" in dist: return "$p_{T}$ [GeV]" 
    elif "_m" in dist: return "mass [GeV]"
    elif "_eta" in dist: return "$\eta$" 
    elif "_phi" in dist: return "$\phi$" 
    elif "_lxy" in dist: return "$r_{xy}$ [mm]" 
    elif "_betagamma" in dist: return "$\\beta\gamma$" 
    elif "_isolation" in dist: return "isolation" 
    elif "_decaytime" in dist: return "decay time [ns]" 
    return "" 

def yscale(dist):
    if "_decaytime" in dist: return "log" 
    else : return "linear" 

def get_bins(dist):
    if "_pt" in dist: return np.linspace(0,1000,20)
    elif "_eta" in dist: return np.linspace(-4,4,20)
    elif "_phi" in dist: return np.linspace(-4,4,20)
    elif "_Lxy" in dist: return np.linspace(0,1000,100)
    elif "_betagamma" in dist: return np.linspace(0,10,20)
    elif "_isolation" in dist: return np.linspace(0,1,20)
    elif "_decaytime" in dist: return np.linspace(0,1,20)
    return np.linspace(0,1000,20)

def get_array(mass,lifetime,dist):
    f = open('output/stau_{}_{}.json'.format(mass,lifetime)) 
    data = json.load(f)
    dist_array = data[dist]
    f.close()
    return dist_array

def compare1D(arrays,labels,outfile):
    bins = get_bins(outfile)
    plt.style.use('seaborn-colorblind')

    for i in range(0,len(arrays)):
        plt.hist(arrays[i], bins, alpha=0.5, label=labels[i])

    plt.legend(loc='upper right')
    plt.yscale(yscale(outfile))
    plt.xlabel(xtitle(outfile))
    plt.ylabel(ytitle(outfile))
    plt.savefig(outfile)
    plt.clf()
    print(outfile)
    return

def compareMass(dist,lifetime="1ns"):
    masses = ["100","400","600"]
    #masses = ["100","200","300","400","500","600"]

    arrays = []
    labels = []
    for mass in masses:
        arrays.append(get_array(mass,lifetime,dist))
        labels.append("M={} GeV, {}".format(mass,lifetime))

    outfile="plots/compareMass_{}_{}.pdf".format(lifetime,dist)
    compare1D(arrays,labels,outfile)
    return


def compareLifetime(dist,mass="600"):
    lifetimes = ["0p001ns","0p01ns","0p1ns","1ns"]

    arrays = []
    labels = []
    for lifetime in lifetimes:
        arrays.append(get_array(mass,lifetime,dist))
        labels.append("M={} GeV, {}".format(mass,lifetime))
        print(lifetime)

    outfile="plots/compareLifetime_{}_{}.pdf".format(lifetime,dist)
    compare1D(arrays,labels,outfile)
    return


compareLifetime("stau_lxy")
compareLifetime("stau_decaytime")

compareMass("stau_eta") 
compareMass("stau_phi") 
compareMass("stau_pt" ) 
compareMass("stau_m"  ) 
compareMass("stau_lxy") 
compareMass("stau_betagamma") 
compareMass("stau_decaytime") 
compareMass("stau_isolation")
