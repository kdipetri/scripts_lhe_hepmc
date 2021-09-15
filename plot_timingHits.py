import json
import time
import numpy as np
#https://www.quora.com/What-is-matplotlib-use-and-why-do-we-use-them
import matplotlib 
matplotlib.use('pdf') # for speed? 
import matplotlib.pyplot as plt

c = 299792458 #m/s

def title(dist):
    if "hitR" in dist: return "hit $r_{xy}$ [mm]" 
    elif "hitZ" in dist: return "hit z [mm]"
    elif "hitT" in dist: return "hit t [ns]"
    elif "hitDist" in dist: return "hit $r_{xyz}$ [mm]"
    elif "hitBeta" in dist: return "$\\beta$ meas."
    elif "hitMass" in dist: return "$m_{ToF}$ [GeV]"
    elif "betagamma" in dist: return "$\\beta\gamma$"
    return "" 

def yscale(dist):
    if "_decaytime" in dist: return "log" 
    else : return "linear" 

def get_bins(dist):
    if   "hitR" in dist: return np.linspace(0,1500,50) 
    elif "hitZ" in dist: return np.linspace(0,3500,50)
    elif "hitT" in dist: return np.linspace(0,20,50) 
    elif "hitDist" in dist: return np.linspace(0,5000,50) 
    elif "hitBeta" in dist: return np.linspace(0,1.5,30) 
    elif "betagamma" in dist: return np.linspace(0,10,50)
    elif "Pt" in dist: return np.linspace(0,500,50)
    elif "Eta" in dist: return np.linspace(-5,5,50)
    return np.linspace(0,1000,50)

def get_array(mass,lifetime,dist):
    f = open('output/stau_{}_{}.json'.format(mass,lifetime)) 
    data = json.load(f)
    dist_array = [ stau[dist] for stau in data["staus"] ]
    #dist_array = data[dist]
    f.close()
    return dist_array

def plot2D(xarray,yarray,outfile):
    xdist = outfile.split("_v_")[1]
    ydist = outfile.split("_v_")[0]
    binx = get_bins(xdist)
    biny = get_bins(ydist)
    plt.style.use('seaborn-colorblind')
    plt.hist2d(xarray,yarray,bins=[binx,biny])
    #plt.legend(loc='upper right')
    #plt.yscale(yscale(outfile))
    plt.xlabel(title(xdist))
    plt.ylabel(title(ydist))
    plt.savefig(outfile)
    plt.clf()
    print(outfile)
    return

def plot1D(array,outfile):
    bins = get_bins(outfile)
    plt.style.use('seaborn-colorblind')
    plt.hist(array, bins, alpha=0.5)

    #plt.legend(loc='upper right')
    #plt.yscale(yscale(outfile))
    plt.xlabel(title(outfile))
    plt.ylabel("staus")
    plt.savefig(outfile)
    plt.clf()
    print(outfile)
    return

def compare1D(arrays,labels,outfile):
    bins = get_bins(outfile)
    plt.style.use('seaborn-colorblind')

    for i in range(0,len(arrays)):
        plt.hist(arrays[i], bins, alpha=0.5, label=labels[i])

    plt.legend(loc='upper right')
    plt.yscale(yscale(outfile))
    plt.xlabel(title(outfile))
    plt.ylabel("staus")
    plt.savefig(outfile)
    plt.clf()
    print(outfile)
    return

def plots2D(mass,lifetime):

    # get hit arrays
    #hit_r = get_array(mass,lifetime,"hit_r")
    #hit_z = get_array(mass,lifetime,"hit_z")
    #hit_t = get_array(mass,lifetime,"hit_t")
    #stau_betagamma = get_array(mass,lifetime,"betagamma")
    #stau_p  = get_array(mass,lifetime,"p")
    stau_pt   = get_array(mass,lifetime,"pt")
    stau_eta  = get_array(mass,lifetime,"eta")

    pre="plots/2Dhits/mass_{}_{}".format(mass,lifetime)

    #misc
    plot2D(stau_eta,stau_pt,"{}_stauPt_v_stauEta.pdf".format(pre))

    ## plot 2D
    #plot2D(hit_z,hit_r,"{}_hitR_v_hitZ.pdf".format(pre) )

    ## plot 1D

    #hit_dist = []
    #hit_beta = [] # v/c
    #hit_mass = []
    #for i in range(0,len(hit_r)):

    #    dist = (hit_r[i]**2 + hit_z[i]**2)**0.5
    #    beta = ( dist / 1e3) / (hit_t[i] / 1e9) / c # v / c 
    #    gamma = 1.0/(1-beta**2)**0.5 
    #    mass = stau_p[i]/(beta*gamma)
    #    #print(dist,beta,hit_t[i])

    #    hit_dist.append(dist) 
    #    hit_beta.append(beta)
    #    hit_mass.append(mass)

    #plot2D(hit_dist,hit_t   ,"{}_hitT_v_hitDist.pdf".format(pre) )
    #plot2D(hit_dist,hit_beta,"{}_hitBeta_v_hitDist.pdf".format(pre) )
    #plot2D(stau_betagamma,hit_beta,"{}_hitBeta_v_betagamma.pdf".format(pre) )
    #plot1D(hit_t   ,"{}_hitT.pdf"   .format(pre))
    #plot1D(hit_dist,"{}_hitDist.pdf".format(pre))
    #plot1D(hit_beta,"{}_hitBeta.pdf".format(pre))
    #plot1D(hit_mass,"{}_hitMass.pdf".format(pre))
    #plot1D(stau_betagamma,"{}_betagamma.pdf".format(pre))

    return (hit_t,hit_dist,hit_beta,hit_mass)

plots2D(100,"stable")

#(time200, dist200, beta200, mass200) = plots2D(200,"1ns")
#(time400, dist400, beta400, mass400) = plots2D(400,"1ns")
#(time600, dist600, beta600, mass600) = plots2D(600,"1ns")
#
#pre="plots/2Dhits/compareMass"
#labels=["$m_{\\tilde{\\tau}}$=200 GeV","$m_{\\tilde{\\tau}}$=400 GeV","$m_{\\tilde{\\tau}}$=600 GeV"]
#compare1D( [beta200,beta400,beta600],labels,"{}_hitBeta.pdf".format(pre) )
#compare1D( [mass200,mass400,mass600],labels,"{}_hitMass.pdf".format(pre) )
#compare1D( [time200,time400,time600],labels,"{}_hitTime.pdf".format(pre) )
