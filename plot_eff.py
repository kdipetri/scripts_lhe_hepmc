import json
import time
import math
import numpy as np
#https://www.quora.com/What-is-matplotlib-use-and-why-do-we-use-them
import matplotlib 
matplotlib.use('pdf') # for speed? 
import matplotlib.pyplot as plt

def ytitle(dist):
    # maybe modify this
    if "eff_v" in dist: return "efficiency"
    if "acc_v" in dist: return "acceptance"
    if "axe_v" in dist: return "AxE"
    return ""

def xtitle(dist):
    if "v_pt" in dist: return "$p_{T}$ [GeV]" 
    elif "v_eta" in dist: return "$\eta$" 
    elif "v_phi" in dist: return "$\phi$" 
    elif "v_lxy" in dist: return "min $L_{xy}$ [mm]" 
    elif "v_z" in dist: return "$z$ [mm]" 
    elif "v_m" in dist: return "mass [GeV]"
    elif "v_life" in dist: return "lifetime, $\\tau$ [ns]"
    return "" 

def lifetime(txt):
    # changes lifetime text to number
    l=""
    if "0p001"  in txt: l = "0.001"
    elif "0p01" in txt: l = "0.01"
    elif "0p1"  in txt: l = "0.1"
    elif "1ns"  in txt: l = "1"
    elif "10ns" in txt: l = "10"
    elif "stable" in txt: l = "stable"
    return l
    
def sampleLabel(s):
    m = s.split("_")[0]
    l = lifetime(s.split("_")[1])
    label = "m={} GeV, $\\tau$={} ns".format(m,l) 
    if "stable" in label : 
        label = "m={} GeV, $\\tau$={}".format(m,l)
    return label
    
def yscale(dist):
    return "linear" 

def get_bins(xvariable,outfile):
    if "v_life" in outfile: 
        bins = [ lifetime(x) for x in xvariable]
    elif "v_mass" in outfile:
        bins = [ x.split("_")[0] for x in xvariable]
    else : 
        bins = xvariable
    return bins

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
    bins = get_bins(xvariable,outfile)
    plt.style.use('seaborn-colorblind')

    for i in range(0,len(yvals)):
        plt.errorbar( bins, yvals[i], yerrs[i], label=labels[i], marker = "o", alpha=0.5)
        #plt.plot(xvariable, arrays[i],  label=labels[i])
        #plt.hist(arrays[i], bins, histtype='step', label=labels[i])

    plt.legend(loc='upper left')
    plt.yscale(yscale(outfile))
    plt.ylim(0.0,1.0)
    plt.xlabel(xtitle(outfile))
    plt.ylabel(ytitle(outfile))
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
    labels_pt  = ["pT > {} GeV".format(x) for x in pts]
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

    delays=["None","delay0.5","delay1.0","delay2.0"]
    betas=["None","beta0.95","beta0.90","beta0.85"]
    mtofs=["None","mass10","mass20","mass50"]
    labels_delay  = ["delay > {} ns".format(x.strip("delay")) for x in delays]
    labels_delay[0]="None"
    labels_beta  = ["beta > {} ".format(x.strip("beta")) for x in betas]
    labels_beta[0]="None"
    labels_mtof  = ["mTOF > {} GeV".format(x.strip("mass")) for x in mtofs]
    labels_mtof[0]="None"
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
