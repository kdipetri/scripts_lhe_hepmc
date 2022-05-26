import json
import time
import numpy as np
#https://www.quora.com/What-is-matplotlib-use-and-why-do-we-use-them
import matplotlib 
matplotlib.use('pdf') # for speed? 
import matplotlib.pyplot as plt


def get_bins(dist):
    if "_pt" in dist: return np.linspace(0,1000,50)
    elif "_eta" in dist: return np.linspace(-5,5,50)
    elif "_phi" in dist: return np.linspace(-4,4,40)
    elif "_Lxy" in dist: return np.linspace(0,1500,60)
    elif "_betagamma" in dist: return np.linspace(0,30,30)
    elif "_isolation" in dist: return np.linspace(0,3,60)
    elif "_decaytime" in dist: return np.linspace(0,6,60)
    elif "hit_t"     in dist: return np.linspace(0,20,50) 
    elif "hit_delay" in dist: return np.linspace(-2,10,200) 
    elif "hit_betaRes" in dist: return np.linspace(-0.2,0.2,200) 
    elif "hit_massRes" in dist: return np.linspace(-400,400,200) 
    elif "hit_beta" in dist: return np.linspace(0,1.5,200) 
    elif "hit_invBeta" in dist: return np.linspace(0,10,200) 
    elif "hit_invBetaRes" in dist: return np.linspace(-10,10,200) 
    elif "hit_mass" in dist: return np.linspace(0,1200,200) 
    return np.linspace(0,1000,200)

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
    #plt.yscale(yscale(outfile))
    #plt.xlabel(xtitle(outfile))
    #plt.ylabel(ytitle(outfile))
    plt.savefig(outfile)
    plt.clf()
    print(outfile)
    return

def get_bkg_array(dist,mass=100,lifetime="stable"):
    f = open('output/bkg_{}_{}.json'.format(mass,lifetime)) 
    data = json.load(f)
    dist_array = [ stau[dist] for stau in data["staus"] ]
    f.close()
    return dist_array


def plot_bkg(dist,cuts):
    arrays=[]
    labels=[]
    bkg_array = get_bkg_array(dist)
    for cut in cuts:    
        num = len([x for x in bkg_array if x > cut])
        den = len(bkg_array)
        eff = float(num)/den
        print(cut, num, den, eff)
    arrays.append( bkg_array )
    labels.append( "bkg")
    compare1D( arrays, labels, "plots/bkg/"+dist+".png")

s="_tHit50;tBS200;zBS0" 
#plot_bkg("hit_delay"+s,np.linspace(0,2,200))
#plot_bkg("hit_beta"+s,np.linspace(0.5,1,200))
plot_bkg("hit_mass"+s,np.linspace(50,150,200))
