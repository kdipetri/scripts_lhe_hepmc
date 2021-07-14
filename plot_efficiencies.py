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
    elif "_lxy" in dist: return "min $L_{xy}$ [mm]" 
    elif "_z" in dist: return "$z$ [mm]" 
    elif "_m" in dist: return "mass [GeV]"
    return "" 

def yscale(dist):
    return "linear" 

def get_bins(dist):
    #if "_pt" in dist: return np.linspace(0,1000,20)
    #elif "_eta" in dist: return np.linspace(-4,4,20)
    #return np.linspace(0,1000,20)
    return 

def get_efficiency(sample,selection):
    f = open('output/stau_{}.json'.format(sample)) 
    data = json.load(f)
    event_array = [ event[selection] for event in data["events"] ]
    npass = sum(event_array)
    nevents = len(event_array)
    eff = float(npass)/nevents
    f.close()
    return eff 

def compare_effs(arrays,xvariable,labels,outfile):
    bins = get_bins(outfile)
    plt.style.use('seaborn-colorblind')

    for i in range(0,len(arrays)):
        plt.plot(xvariable, arrays[i],  label=labels[i])
        #plt.hist(arrays[i], bins, histtype='step', label=labels[i])

    plt.legend(loc='upper right')
    plt.yscale(yscale(outfile))
    plt.xlabel(xtitle(outfile))
    plt.ylabel(ytitle(outfile))
    plt.savefig(outfile)
    plt.clf()
    print(outfile)
    return


def eff_array_Lxy(sample="500_1ns",lxys=[600, 800, 1000, 1200], eta=2.5, z=3000):

    # returns an array of efficiency versus different lxy cuts
    eff_array = []
    for lxy in lxys:
        selOpt = "pass_StageOne_lxy{};z{};eta{}".format(lxy,z,eta)
        eff_array.append( get_efficiency(sample, selOpt) )
    
    return eff_array

def compare_eff_lxy(samples=["500_0p01ns","500_0p1ns","500_1ns","500_10ns"]):
    # compares efficiencies for different masses or lifetimes
    lxys=[600, 800, 1000, 1200]
    eff_arrays = []
    for sample in samples:
        eff_arrays.append( eff_array_Lxy(sample,lxys) ) 

    compare_effs(eff_arrays, lxys, samples,"plots/effs/eff_lxy_test.pdf")

    

    #arrays = []
    #labels = []
    #for lifetime in lifetimes:
    #    arrays.append(get_array(mass,lifetime,dist))
    #    labels.append("M={} GeV, {}".format(mass,lifetime))
    #    print(lifetime)

    #outfile="plots/compareLifetime_{}_{}.pdf".format(lifetime,dist)
    #compare1D(arrays,labels,outfile)
    #return

# Compare efficiencies  
#graphEffLxy()
compare_eff_lxy()
