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
    event_array = [ event[selection] for event in data["events"] ]
    npass = float(sum(event_array))
    nevents = float(len(event_array))
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

    plt.savefig(outfile)
    plt.clf()

    print(outfile)
    return


def eff_array_lxy(sample="500_1ns",lxys=[600, 800, 1000, 1200],z=3000,eta=2.5):

    # returns an array of efficiency versus different lxy cuts
    eff_array = []
    err_array = []
    for lxy in lxys:
        selOpt = "pass_StageOne_lxy{};z{};eta{}".format(lxy,z,eta)
        eff,err = get_efficiency(sample, selOpt)
        eff_array.append( eff )
        err_array.append( err )
    
    return eff_array,err_array

def eff_array_eta(sample="500_1ns",lxy= 1200,z=3000,etas=[1.0,2.5,4.0]):

    # returns an array of efficiency versus different lxy cuts
    eff_array = []
    err_array = []
    for eta in etas:
        selOpt = "pass_StageOne_lxy{};z{};eta{}".format(lxy,z,eta)
        eff,err = get_efficiency(sample, selOpt)
        eff_array.append( eff )
        err_array.append( err )
    
    return eff_array,err_array

def eff_array_samples(samples=["500_0p01ns","500_1ns","500_10ns"],lxy=1200,z=3000,eta=2.5):

    # returns an array of efficiency versus different masses or lifetimes 
    eff_array = []
    err_array = []
    for sample in samples:
        selOpt = "pass_StageOne_lxy{};z{};eta{}".format(lxy,z,eta)
        eff,err = get_efficiency(sample, selOpt)
        eff_array.append( eff )
        err_array.append( err )
    
    return eff_array,err_array

def compare_eff_lxy(lifetime="10ns",mass="500"):

    # compares efficiencies for different masses or lifetimes
    lxys = [600, 800, 1000, 1200]
    samples_life = [mass+"_0p01ns",mass+"_0p1ns",mass+"_1ns",mass+"_10ns",mass+"_stable"]
    samples_mass = ["100_"+lifetime,"300_"+lifetime,"500_"+lifetime,"700_"+lifetime,"1000_"+lifetime]
    z=3000
    eta=2.5
    labels_lxy  = ["$L_{xy}$ = " + "{} mm".format(x) for x in lxys]
    labels_life = [sampleLabel(s) for s in samples_life]
    labels_mass = [sampleLabel(s) for s in samples_mass]

    # lxy x-axis
    effs_life = []
    errs_life = []
    for sample in samples_life:
        effs,errs = eff_array_lxy(sample,lxys,z,eta) 
        effs_life.append( effs ) 
        errs_life.append( errs ) 

    effs_mass = []
    errs_mass = []
    for sample in samples_mass:
        effs,errs = eff_array_lxy(sample,lxys,z,eta) 
        effs_mass.append( effs ) 
        errs_mass.append( errs ) 

    compare_effs(effs_life, errs_life, lxys, labels_life,"plots/effs/acc_v_lxy_for_life_m{}.pdf".format(mass))
    compare_effs(effs_mass, errs_mass, lxys, labels_mass,"plots/effs/acc_v_lxy_for_mass_l{}.pdf".format(lifetime))

    # sample lifetime or mass x-axis
    effs_life = []
    effs_mass = []
    errs_life = []
    errs_mass = []
    for lxy in lxys : 
        effs,errs = eff_array_samples(samples_life,lxy,z,eta) 
        effs_life.append( effs )
        errs_life.append( errs )
        effs,errs = eff_array_samples(samples_mass,lxy,z,eta)
        effs_mass.append( effs )
        errs_mass.append( errs )

    compare_effs(effs_life, errs_life, samples_life, labels_lxy,"plots/effs/acc_v_life_for_lxy_m{}.pdf".format(mass))
    compare_effs(effs_mass, errs_mass, samples_mass, labels_lxy,"plots/effs/acc_v_mass_for_lxy_l{}.pdf".format(lifetime))

def compare_eff_eta(lifetime="1ns",mass="500"):

    # compares efficiencies for different masses or lifetimes
    lxy = 1200
    z = 3000
    etas = [1.0,2.5,4.0]
    samples_life = [mass+"_0p01ns",mass+"_0p1ns",mass+"_1ns",mass+"_10ns",mass+"_stable"]
    samples_mass = ["100_"+lifetime,"300_"+lifetime,"500_"+lifetime,"700_"+lifetime,"1000_"+lifetime]
    labels_eta  = ["|$\eta$| < {}".format(x) for x in etas]
    labels_life = [sampleLabel(s) for s in samples_life]
    labels_mass = [sampleLabel(s) for s in samples_mass]
    

    # eta x-axis
    effs_life = []
    errs_life = []
    for sample in samples_life:
        effs,errs = eff_array_eta(sample,lxy,z,etas)
        effs_life.append( effs ) 
        errs_life.append( errs ) 

    effs_mass = []
    errs_mass = []
    for sample in samples_mass:
        effs,errs = eff_array_eta(sample,lxy,z,etas)
        effs_mass.append( effs ) 
        errs_mass.append( errs ) 

    compare_effs(effs_life, errs_life, etas, labels_life,"plots/effs/acc_v_eta_for_life_m{}.pdf".format(mass))
    compare_effs(effs_mass, errs_mass, etas, labels_mass,"plots/effs/acc_v_eta_for_mass_l{}.pdf".format(lifetime))

    # sample lifetime or mass x-axis
    effs_life = []
    effs_mass = []
    errs_life = []
    errs_mass = []
    for eta in etas : 
        effs,errs = eff_array_samples(samples_life,lxy,z,eta) 
        effs_life.append( effs )
        errs_life.append( errs )
        effs,errs = eff_array_samples(samples_mass,lxy,z,eta)
        effs_mass.append( effs )
        errs_mass.append( errs )

    compare_effs(effs_life, errs_life, samples_life, labels_eta,"plots/effs/acc_v_life_for_eta_m{}.pdf".format(mass))
    compare_effs(effs_mass, errs_mass, samples_mass, labels_eta,"plots/effs/acc_v_mass_for_eta_l{}.pdf".format(lifetime))
    
# Compare efficiencies  


# Stage 1 efficiency versus different Lxy Cuts (n layer)
compare_eff_lxy("1ns" ,"500") 
compare_eff_lxy("10ns","100") 

# Stage 1 efficiency versus different eta cuts
compare_eff_eta("1ns" ,"500")
compare_eff_eta("10ns","100")


# Stage 2 efficiency for different pT cuts

# Stage 2 efficiency for different delays

# Stage 2 delay for different methods?
