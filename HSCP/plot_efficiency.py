import json
import time
import math
import numpy as np
#https://www.quora.com/What-is-matplotlib-use-and-why-do-we-use-them
import matplotlib 
matplotlib.use('pdf') # for speed? 
import matplotlib.pyplot as plt
from plot_helper import *


def get_efficiency(sample,selection):
    f = open('output/stau_{}.json'.format(sample)) 
    data = json.load(f)

    # Stage 2 pass
    event_array = [ event[selection] for event in data["events"] ]
    npass = float(sum(event_array))

    # Stage 1 acceptance for nominal selection
    stageOne = "pass_StageOne_lxy1200;z3000;eta2.5"
    # for now just compute total efficiency (since we focus on stable)
    # later can add option for efficiency with respect to acceptance
    
    seen_array = [ event[stageOne] for event in data["events"] ]
    nevents = float(sum(seen_array))

    eff = npass/nevents
    err = (math.sqrt(( npass / nevents ) * (1.0 - ( npass / nevents )) / nevents))
    f.close()
    return eff,err 

def compare_effs(yvals,yerrs,xvariable,labels,outfile):
    bins = get_bins(outfile,xvariable)
    plt.style.use('seaborn-colorblind')
    plt.figure(figsize=(6,5.5))

    for i in range(0,len(yvals)):
        plt.errorbar( bins, yvals[i], yerrs[i], label=labels[i], marker = "o", alpha=0.5)

    plt.subplots_adjust(left=0.18, right=0.95, top=0.9, bottom=0.18)
    plt.grid(visible=True, which='major', axis='both', color='gainsboro')

    plt.yscale(yscale(outfile))
    plt.ylim(-0.05,1.05)
   
    size=20 
    plt.xlabel(xtitle(outfile),fontsize=size, labelpad=size/2)
    plt.ylabel(ytitle(outfile),fontsize=size, labelpad=size/2)
    plt.xticks(fontsize=size-4)
    plt.yticks(fontsize=size-4)
    plt.title(title(outfile),fontsize=size-4)
    plt.legend(loc=leg_loc(outfile),prop={'size':size-4,})
    plt.yscale(yscale(outfile))
    plt.savefig(outfile)
    plt.clf()

    print(outfile)

    return

def eff_array_samples(samples=["500_0p01ns","500_1ns","500_10ns"],pt=10,timeCut="None",tHit=50,tBS=200,zBS=50):

    # returns an array of efficiency versus different masses or lifetimes 


    # Stage 2 more refined track selection 
    eff_array = []
    err_array = []
    for sample in samples:
        sel2 = "pass_StageTwo_pt{};{}_tHit{};tBS{};zBS{}".format(pt,timeCut,tHit,tBS,zBS)

        eff,err = get_efficiency(sample, sel2)
        eff_array.append( eff )
        err_array.append( err )
    
    return eff_array,err_array

def compare_eff_pt(lifetime="stable"):

    # compares efficiencies for different masses or lifetimes
    samples_mass = ["100_"+lifetime,"300_"+lifetime,"500_"+lifetime,"700_"+lifetime,"1000_"+lifetime]

    pts=[10,20,50,100]
    labels_pt  = ["$p_{T}$"+" > {} GeV".format(x) for x in pts]
    timeCut="None"

    # stau mass x-axis
    effs_mass = []
    errs_mass = []
    for pt in pts : 
        effs,errs = eff_array_samples(samples_mass,pt=pt,timeCut=timeCut)
        effs_mass.append( effs )
        errs_mass.append( errs )

    compare_effs(effs_mass, errs_mass, samples_mass, labels_pt,"plots/effs/eff_v_mass_for_pt_l{}.pdf".format(lifetime))

def compare_eff_delay(lifetime="stable"):

    # compares efficiencies for different masses or lifetimes
    samples_mass = ["100_"+lifetime,"300_"+lifetime,"500_"+lifetime,"700_"+lifetime,"1000_"+lifetime]

#track_sels.append("pt10;mass15")
#track_sels.append("pt10;mass30")
#track_sels.append("pt10;mass60")
#track_sels.append("pt10;beta0.96")
#track_sels.append("pt10;beta0.95")
#track_sels.append("pt10;beta0.90")
#track_sels.append("pt10;delay0.25")
#track_sels.append("pt10;delay0.33")
#track_sels.append("pt10;delay0.50")

    delays=["delay0.25","delay0.33","delay0.50"]
    betas =["beta0.96","beta0.95","beta0.90"]
    mtofs =["mass15","mass30","mass60"]
    labels_delay = ["delay > {} ns".format(x.strip("delay")) for x in delays]
    labels_beta  = ["$\\beta_{TOF}$"+" < {} ".format(x.strip("beta")) for x in betas]
    labels_mtof  = ["$m_{TOF}$"+" > {} GeV".format(x.strip("mass")) for x in mtofs]
    pt=10 

    # stau mass x-axis
    effs_mass = []
    errs_mass = []
    for delay in delays : 
        effs,errs = eff_array_samples(samples_mass,pt=pt,timeCut=delay)
        effs_mass.append( effs )
        errs_mass.append( errs )

    compare_effs(effs_mass, errs_mass, samples_mass, labels_delay,"plots/effs/eff_v_mass_for_delay_l{}.pdf".format(lifetime))

    effs_mass = []
    errs_mass = []
    for beta in betas : 
        effs,errs = eff_array_samples(samples_mass,pt=pt,timeCut=beta)
        effs_mass.append( effs )
        errs_mass.append( errs )

    compare_effs(effs_mass, errs_mass, samples_mass, labels_beta,"plots/effs/eff_v_mass_for_beta_l{}.pdf".format(lifetime))

    effs_mass = []
    errs_mass = []
    for mtof in mtofs : 
        effs,errs = eff_array_samples(samples_mass,pt=pt,timeCut=mtof)
        effs_mass.append( effs )
        errs_mass.append( errs )

    compare_effs(effs_mass, errs_mass, samples_mass, labels_mtof,"plots/effs/eff_v_mass_for_mTOF_l{}.pdf".format(lifetime))


# Stage 2 efficiency versus different pT cuts 
compare_eff_pt("stable") 

# Stage 2 efficiency for different delays
compare_eff_delay("stable")

# Stage 2 delay for different methods?
