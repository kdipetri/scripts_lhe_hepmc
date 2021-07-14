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
    elif "_eta" in dist: return "$\eta$" 
    elif "_phi" in dist: return "$\phi$" 
    elif "_lxy" in dist: return "$r_{xy}$ [mm]" 
    elif "_betagamma" in dist: return "$\\beta\gamma$" 
    elif "_isolation" in dist: return "isolation" 
    elif "_decaytime" in dist: return "decay time [ns]" 
    elif "_hit_t"     in dist: return "$t_{hit}$ [ns]" 
    elif "_hit_delay" in dist: return "$t_{hit}-t_{0}$ [ns]" 
    elif "_hit_betaRes" in dist: return "$\\beta$ meas.-$\\beta$ true." 
    elif "_hit_massRes" in dist: return "$m_{ToF}$ -$m_{True}$ [GeV]" 
    elif "_hit_beta" in dist: return "$\\beta$ meas." 
    elif "_hit_mass" in dist: return "$m_{ToF}$ [GeV]" 
    elif "_m" in dist: return "mass [GeV]"
    return "" 

def yscale(dist):
    if "_lxy" in dist: return "log" 
    if "_decaytime" in dist: return "log" 
    if "_hit_betaRes" in dist: return "log" 
    if "_hit_massRes" in dist: return "log" 
    else : return "linear" 

def get_bins(dist):
    if "_pt" in dist: return np.linspace(0,1000,20)
    elif "_eta" in dist: return np.linspace(-4,4,20)
    elif "_phi" in dist: return np.linspace(-4,4,20)
    elif "_Lxy" in dist: return np.linspace(0,1000,100)
    elif "_betagamma" in dist: return np.linspace(0,10,20)
    elif "_isolation" in dist: return np.linspace(0,1,20)
    elif "_decaytime" in dist: return np.linspace(0,1,20)
    elif "_hit_t"     in dist: return np.linspace(0,20,50) 
    elif "_hit_delay" in dist: return np.linspace(0,10,50) 
    elif "_hit_betaRes" in dist: return np.linspace(-0.2,0.2,50) 
    elif "_hit_massRes" in dist: return np.linspace(-400,400,50) 
    elif "_hit_beta" in dist: return np.linspace(0,1.5,50) 
    elif "_hit_mass" in dist: return np.linspace(0,1000,50) 
    return np.linspace(0,1000,20)

def get_array(mass,lifetime,dist):
    f = open('output/stau_{}_{}.json'.format(mass,lifetime)) 
    data = json.load(f)
    dist_array = [ stau[dist] for stau in data["staus"] ]
    f.close()
    return dist_array

def compare1D(arrays,labels,outfile):
    bins = get_bins(outfile)
    plt.style.use('seaborn-colorblind')

    for i in range(0,len(arrays)):
        plt.hist(arrays[i], bins, histtype='step', label=labels[i])

    plt.legend(loc='upper right')
    plt.yscale(yscale(outfile))
    plt.xlabel(xtitle(outfile))
    plt.ylabel(ytitle(outfile))
    plt.savefig(outfile)
    plt.clf()
    print(outfile)
    return

def compareMass(dist,lifetime="1ns"):
    masses = ["200","400","600"]
    #masses = ["100","200","300","400","500","600"]

    arrays = []
    labels = []
    for mass in masses:
        arrays.append(get_array(mass,lifetime,dist))
        labels.append("M={} GeV".format(mass))
        #labels.append("M={} GeV, {}".format(mass,lifetime))

    outfile="plots/compareMass_{}_{}.pdf".format(lifetime,dist)
    compare1D(arrays,labels,outfile)
    return


def compareLifetime(dist,mass="500"):
    lifetimes = ["0p01ns","0p1ns","1ns","10ns"]

    arrays = []
    labels = []
    for lifetime in lifetimes:
        arrays.append(get_array(mass,lifetime,dist))
        labels.append("M={} GeV, {}".format(mass,lifetime))
        print(lifetime)

    outfile="plots/compareLifetime_{}_{}.pdf".format(lifetime,dist)
    compare1D(arrays,labels,outfile)
    return

def compareTimeRes(dist,mass="600",lifetime = "1ns"):
    methods = []
    methods.append("_tHit0;tBS0;zBS0") # truth  
    methods.append("_tHit50;tBS0;zBS0") # hit res only 
    methods.append("_tHit0;tBS200;zBS0") # beamspot only  
    methods.append("_tHit0;tBS0;zBS50") # z0 only  
    methods.append("_tHit50;tBS200;zBS0") # hit + beamspot res  
    methods.append("") # all

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

# Compare stau properties for different masses and lifetimes
compareLifetime("lxy")
#compareLifetime("decaytime")

#compareTimeRes("hit_time")
#compareTimeRes("hit_delay")
#compareTimeRes("hit_beta")
#compareTimeRes("hit_betaRes")
#compareTimeRes("hit_mass")
#compareTimeRes("hit_massRes")
#
#compareMass("eta") 
#compareMass("phi") 
#compareMass("pt" ) 
#compareMass("m"  ) 
#compareMass("lxy") 
#compareMass("betagamma") 
#compareMass("decaytime") 
#compareMass("isolation")
#compareMass("hit_time")
compareMass("hit_delay")
#compareMass("hit_beta")
#compareMass("hit_betaRes")
#compareMass("hit_mass")
#compareMass("hit_massRes")
