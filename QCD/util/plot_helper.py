
import numpy as np

def yscale(dist):
    if "nDV" in dist: return "log"
    if "n_dv" in dist: return "log"
    if "nTrack" in dist: return "log"
    if "pt" in dist: return "log" 
    if "d0" in dist: return "log"
    if "prod_rxy" in dist: return "log"
    if "n_jet" in dist: return "log"
    else : return "linear" 

def title(dist):
    if "for_qcd" in dist: return "QCD" 
    elif "for_higgsportal_125_55_1ns" in dist:
        return "$m_{h} = 125$ GeV, $m_{S} = 55$ GeV, $\\tau_{S} = 1$ ns" 
    elif "for_higgsportal_125_40_0p1ns" in dist:
        return "$m_{h} = 125$ GeV, $m_{S} = 40$ GeV, $\\tau_{S} = 0.1$ ns" 
    elif "pileup" in dist:
        pu = dist.split("_")[3].strip("pileup").strip(".pdf")
        return "$<\\mu>$ = {}".format(pu)
    if "l1ns"    in dist: return "Stau Lifetime $\\tau_{\\tilde{\\tau}} = 1$ ns"
    if "l10ns"   in dist: return "Stau Lifetime $\\tau_{\\tilde{\\tau}} = 10$ ns"
    if "lstable" in dist: return "Stau Lifetime $\\tau_{\\tilde{\\tau}} = $ stable"
    if "m100"    in dist: return "Stau Mass $m_{\\tilde{\\tau}} = 100$ GeV"
    if "m500"    in dist: return "Stau Mass $m_{\\tilde{\\tau}} = 500$ GeV"
    else : return ""

def leg_loc(dist):
    if "eff_v_mass" in dist: return "lower right"
    if "v_mass_for_eta" in dist: return "upper right"
    if "_hit_beta_" in dist : return "upper left"
    if "_hit" in dist : return "upper right"
    if "_pt" in dist: return "upper right"
    else : return "upper left"

def ytitle(dist):
    # maybe modify this
    if "track" in dist: return "Tracks"
    if "nTrack" in dist: return "Events"
    return "Events"

def xtitle(dist):
    if "n_tracks" in dist: return "$n_{\\mathsf{Track}}$" 
    if "n_jets" in dist: return "$n_{\\mathsf{Jet}}$" 
    if "nDVs" in dist: 
        if "2trk" in dist: return "$n_{\\mathsf{DVs}}$ ($\\geq2$ Tracks)"
        if "3trk" in dist: return "$n_{\\mathsf{DVs}}$ ($\\geq3$ Tracks)"
        if "4trk" in dist: return "$n_{\\mathsf{DVs}}$ ($\\geq4$ Tracks)"
        if "5trk" in dist: return "$n_{\\mathsf{DVs}}$ ($\\geq5$ Tracks)"
        else : return "$n_{\\mathsf{DVs}}$"
    if "n_dvs" in dist: return "$n_{\\mathsf{DVs}}$"
    if   "Prompt_nTrack" in dist: return "prompt $n_{\\mathsf{Track}}$" 
    elif "Displaced_nTrack" in dist: return "displaced $n_{\\mathsf{Track}}$" 
    if "jetht" in dist: 
        return "$H_{\\mathsf{T}}$ (GeV)"
    if "sumtrkpt" in dist: 
        return "$\\Sigma_{\\mathsf{Track}}~p_{\\mathsf{T}}$ (GeV)"
    if "nJet" in dist: 
        if "prompt" in dist: return "$n_{\\mathsf{Jet}}$"
        if "displaced" in dist: return "displaced $n_{\\mathsf{Jet}}$"
    if "nTrack" in dist: 
        if "prompt" in dist: return "prompt $n_{\\mathsf{Track}}$"
        if "displaced" in dist: return "displaced $n_{\\mathsf{Track}}$"
    if "HSCP" in dist: 
        if "highBeta" in dist: return "isolated $n_{\\mathsf{Track}}$ ($\\beta_{\\mathsf{TOF}}<0.98$)"
        elif "highM"  in dist: return "isolated $n_{\\mathsf{Track}}$ ($m_{\\mathsf{TOF}}>10$ GeV)"
        else                 : return "isolated $n_{\\mathsf{Track}}$"
    if "ndvs3" in dist : return "$n_{\\mathsf{DVs}}$ ($\\geq3$ Tracks)"
    if "ndvs4" in dist : return "$n_{\\mathsf{DVs}}$ ($\\geq4$ Tracks)"
    if "DV" in dist and "ntrack" in dist: return "DV $n_{\\mathsf{Track}}$"
    elif "pt" in dist: return "$p_{\\mathsf{T}}$ (Gev)" 
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
    
def get_bins(outfile,xvariable=[]):
    dist=outfile
    if "v_life" in outfile: 
        bins = [ lifetime(x) for x in xvariable]
    elif "v_mass" in outfile:
        bins = [ int(x.split("_")[0]) for x in xvariable]
    elif "nDVs" in outfile: 
        return np.linspace(-0.5,10.5,12)
    elif "Prompt_nTrack" in dist : return np.linspace(0,300,50)
    elif "Displaced_nTrack" in dist : 
        if "pileup" in dist : return np.linspace(-0.5,50.5,52)
        return np.linspace(-0.5,20.5,22)
    elif "n_dvs" in dist : return np.linspace(-0.5,10.5,12) 
    elif "n_tracks" in dist : 
        if "small" in dist : return np.linspace(-0.5,50.5,52)
        else : return np.linspace(0,300,50)
    elif "n_jets" in dist :  
        if "small" in dist : return np.linspace(-0.5,10.5,12)
        return np.linspace(-0.5,15.5,17)
    elif "pt"  in dist: return np.linspace(0,50,50)
    elif "eta" in dist: return np.linspace(-5,5,50)
    elif "phi" in dist: return np.linspace(-4,4,40)
    elif "d0"  in dist: return np.linspace(0,10,50)
    elif "r"   in dist: return np.linspace(0,1500,60)
    elif "rxy" in dist: return np.linspace(0,1500,60)
    elif "z"   in dist: return np.linspace(-1000,1000,50)
    elif "betagamma" in dist: return np.linspace(0,30,30)
    elif "isolation" in dist: return np.linspace(0,3,60)
    elif "decaytime" in dist: return np.linspace(0,6,60)
    elif "m"   in dist: return np.linspace(0,1100,50)
    else : 
        bins = xvariable

    return bins


