#!/usr/bin/env python
import argparse
import json
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import uproot4 as uproot
import scipy.interpolate
import math
from scipy.interpolate import griddata
from scipy.interpolate import interpn
from matplotlib.ticker import (MultipleLocator, FormatStrFormatter,
                               AutoMinorLocator)

from matplotlib import colors as mcolors
import colorsys
from matplotlib.colors import ListedColormap, LinearSegmentedColormap

plt.ioff()

def argsort(seq):
    return sorted(range(len(seq)), key=seq.__getitem__)

event_count = 10000

# arg parsing
parser = argparse.ArgumentParser(description='process model')
parser.add_argument('model'  , type=str , default='higgs', help='benchmark model: higgs or staus')

args = parser.parse_args()
model   = args.model


#creates empty lists of lifetimes, pts, d0s, and masses
print(model)
lifes  = ['0p01ns','0p1ns','1ns']
if model=='higgs':
    masses = [5,8,15,25,40,55]
    part = "\\mathsf{S}"
elif model=='staus' : 
    masses = [100,300,500]
    #masses = [100,200,300,400,500,600]
    part = "\\tilde{\\tau}"
else :
    print('model must be higgs or staus')
    exit()


def life_to_float(life):
    fl = float(life.strip("ns").replace("p","."))
    return fl

def get_array(model,mass,life,dist):
    f = open('output/%s_%d_%s_distributions.json'%(model,mass,life))
    data = json.load(f)
    if dist=="track_d0sm" : dist = "track_d0"
    array = data[dist]
    f.close()
    return array

def yscale(dist):
    if 'track_pt' in dist: return 'log'
    if 'track_d0' in dist: return 'log'
    if 'vtx' in dist: return 'log'
    if model=='higgs' and 'ntr' in dist: return 'log'
    return 'linear'

def xtitle(dist):
    if "track_pt" in dist: return "$p_{\\mathsf{T}}$ (GeV)"
    if "track_d0" in dist: return "$d_{0}$ (mm)"
    if "track_eta" in dist: return "$\\eta$"
    if "track_phi" in dist: return "$\\phi$"
    if "vtx_lxy" in dist: return "$L_{\\mathsf{xy}}$ (mm)"
    if "vtx_r" in dist: return "$R$ (mm)"
    if "vtx_z" in dist: return "$Z$ (mm)"
    if "ntracks_acc" in dist: return "$n_{\\mathsf{Track}}^{\\mathsf{Accepted}}$"
    if "ntracks_d0" in dist: return "$n_{\\mathsf{Track}}^{\\mathsf{Displaced}}$"
    if "ntracks" in dist: return "$n_{\\mathsf{Charged}}$"
    return ""

def ytitle(dist):
    if "ntracks" in dist: return "Events (AU)"
    if "track_" in dist: return "Charged Particles (AU)"
    if "vtx" in dist: return "Vertex (AU)" 
    return ""

def get_bins(dist):
    if model=='higgs':
        if "ntracks" in dist: return np.linspace(-0.5,305.5,52) #np.linspace(-0.5,103.5,27)
        if "track_pt" in dist: return np.linspace(0,70,35)
    if model=='staus':
        if "ntracks"  in dist: return np.linspace(-0.5,6.5,8)
        if "track_pt" in dist: return np.linspace(0,600,30)
    if "track_d0sm" in dist: return np.linspace(0,10,100)
    if "track_d0" in dist: return np.linspace(0,500,100)
    if "_eta"  in dist: return np.linspace(-5,5,50)
    if "_phi"  in dist: return np.linspace(-4,4,30)
    if "vtx_z" in dist: return np.linspace(-1000,1000,50)
    if "vtx"   in dist: return np.linspace(0,1000,50)
    return np.linspace(0,100,30) 

def title(dist):
    t = model 
    # get important number
    n = dist.split("_")[2]
    if "compareLife" in dist :
        if model=='higgs' : t += ", $m_{"+part+"}$ = "+ str(n) +" GeV" 
        if model=='staus' : t += ", $m_{"+part+"}$ = "+ str(n) +" GeV"
    else : 
        if model=='higgs' : t += ", $\\tau_{"+part+"}$ = "+ str(life_to_float(n)) +" ns" 
        if model=='staus' : t += ", $\\tau_{"+part+"}$ = "+ str(life_to_float(n)) +" ns" 
    return t 

def compare1D(arrays,labels,outfile,norm=0):
    plt.style.use('seaborn-colorblind')

    bins = get_bins(outfile)
    fig, ax = plt.subplots(figsize=(6,5.5))

    for i in range(0,len(arrays)):
        (counts, bins) = np.histogram(arrays[i], bins=bins)
        factor = len(arrays[i])
        plt.hist(bins[:-1], bins, histtype='step', label=labels[i], weights=counts/factor)

    ax.xaxis.set_major_locator(plt.MaxNLocator(5))
    ax.yaxis.set_major_locator(plt.MaxNLocator(5))

    plt.subplots_adjust(left=0.18, right=0.95, top=0.9, bottom=0.18)
    plt.grid(visible=True, which='major', axis='both', color='gainsboro')

   
    size=20 
    plt.yscale(yscale(outfile))
    if yscale(outfile)=='log': plt.ylim(0.0005,2.)
    plt.xlabel(xtitle(outfile),fontsize=size, labelpad=size/2)
    plt.ylabel(ytitle(outfile),fontsize=size, labelpad=size/2)
    plt.xticks(fontsize=size-4)
    plt.yticks(fontsize=size-4)
    plt.title(title(outfile),fontsize=size-4)
    plt.legend(prop={'size':size-4,})
    #plt.legend(loc=leg_loc(outfile),prop={'size':size-4,})

    plt.savefig(outfile)
    plt.clf()
    plt.close(fig)
    print(outfile)
    return

def compareMass(dist,lifetime="0p1ns"):

    arrays = []
    labels = []
    for mass in masses:
        arrays.append(get_array(model,mass,lifetime,dist))
        labels.append("$m_{"+part+"}$"+" = {} GeV".format(mass))

    # no bkg
    outfile="plots/distributions/compareMass_{}_{}_{}.pdf".format(model,lifetime,dist)
    compare1D(arrays,labels,outfile)

    return

def compareLife(dist,mass=40):

    arrays = []
    labels = []
    for life in lifes:
        arrays.append(get_array(model,mass,life,dist))
        labels.append("$\\tau_{"+part+"}$"+" = {} ns".format(life_to_float(life)))

    # no bkg
    outfile="plots/distributions/compareLife_{}_{}_{}.pdf".format(model,mass,dist)
    compare1D(arrays,labels,outfile)

    return

#Structure: [lifetime, mass, value]
dists=[]
dists.append("track_pt") 
dists.append("track_d0")
dists.append("track_d0sm")
dists.append("track_eta")
dists.append("vtx_lxy")
dists.append("vtx_r")
dists.append("vtx_z")
dists.append("ntracks")
dists.append("ntracks_d0")
dists.append("ntracks_acc")

for dist in dists:
    compareMass(dist,"0p1ns")
    compareMass(dist,"1ns")
    if model=='higgs':
        compareLife(dist,8)
        compareLife(dist,15)
        compareLife(dist,40)
        compareLife(dist,55)
    else : 
        compareLife(dist,300)
        compareLife(dist,500)

