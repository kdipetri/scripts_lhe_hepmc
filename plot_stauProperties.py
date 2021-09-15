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
    if "_pt" in dist: return np.linspace(0,1000,50)
    elif "_eta" in dist: return np.linspace(-5,5,50)
    elif "_phi" in dist: return np.linspace(-4,4,40)
    elif "_Lxy" in dist: return np.linspace(0,1500,60)
    elif "_betagamma" in dist: return np.linspace(0,30,30)
    elif "_isolation" in dist: return np.linspace(0,3,60)
    elif "_decaytime" in dist: return np.linspace(0,6,60)
    elif "_hit_t"     in dist: return np.linspace(0,20,50) 
    elif "_hit_delay" in dist: return np.linspace(-2,10,60) 
    elif "_hit_betaRes" in dist: return np.linspace(-0.2,0.2,50) 
    elif "_hit_massRes" in dist: return np.linspace(-400,400,50) 
    elif "_hit_beta" in dist: return np.linspace(0,1.5,50) 
    elif "_hit_invBeta" in dist: return np.linspace(0,10,50) 
    elif "_hit_invBetaRes" in dist: return np.linspace(-10,10,50) 
    elif "_hit_mass" in dist: return np.linspace(0,1200,60) 
    return np.linspace(0,1000,20)

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

    for i in range(0,len(arrays)):
        (counts, bins) = np.histogram(arrays[i], bins=bins)
        factor = len(arrays[i])
        if "bkg" in labels[i]: 
            plt.hist(bins[:-1], bins, histtype='step', color="tab:gray", label=labels[i], weights=counts/factor)
        else : 
            plt.hist(bins[:-1], bins, histtype='step', label=labels[i], weights=counts/factor)
            #plt.hist(arrays[i], bins, histtype='step', label=labels[i], density=norm)

    plt.legend(loc='upper right')
    plt.yscale(yscale(outfile))
    plt.xlabel(xtitle(outfile))
    plt.ylabel(ytitle(outfile))
    plt.savefig(outfile)
    plt.clf()
    print(outfile)
    return

def compareMass(dist,lifetime="stable"):
    masses = ["100","500","1000"]
    #masses = ["100","300","500","700","1000"]

    arrays = []
    labels = []
    for mass in masses:
        arrays.append(get_array(mass,lifetime,dist))
        labels.append("M={} GeV".format(mass))
        #labels.append("M={} GeV, {}".format(mass,lifetime))

    # no bkg
    outfile="plots/compareMass_{}_{}.pdf".format(lifetime,dist)
    compare1D(arrays,labels,outfile)

    # add bkg
    arrays.append(get_bkg_array(dist))
    labels.append("Bkg")
    outfile="plots/compareMass_{}_{}_withbkg.pdf".format(lifetime,dist)
    compare1D(arrays,labels,outfile)

    return


def compareLifetime(dist,mass="500"):
    lifetimes = ["0p01ns","0p1ns","1ns","10ns","stable"]

    arrays = []
    labels = []
    for lifetime in lifetimes:
        arrays.append(get_array(mass,lifetime,dist))
        labels.append("M={} GeV, {}".format(mass,lifetime))
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
