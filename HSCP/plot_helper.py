
import numpy as np

def yscale(dist):
    if "_lxy" in dist: return "log" 
    if "_decaytime" in dist: return "log" 
    if "_hit_betaRes" in dist: return "log" 
    if "_hit_massRes" in dist: return "log" 
    else : return "linear" 

def title(dist):
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
    if "eff_v" in dist: return "Efficiency"
    if "acc_v" in dist: return "Acceptance"
    if "axe_v" in dist: return "AxE"
    if "compare" in dist: return "Tracks [AU]"
    return ""

def xtitle(dist):
    if "v_pt" in dist: return "$p_{\\mathsf{T}}$ (GeV)" 
    elif "v_eta" in dist: return "$\eta$" 
    elif "v_phi" in dist: return "$\phi$" 
    elif "v_lxy" in dist: return "min $L_{\\mathsf{xy}}$ (mm)" 
    elif "v_z" in dist: return "$Z$ (mm)" 
    elif "v_m" in dist: return "Stau Mass $m_{\\tilde{\\tau}}$ (GeV)"
    elif "v_life" in dist: return "Stau Lifetime $\\tau_{\\tilde{\\tau}}$ (ns)"
    elif "_pt" in dist: return "$p_{\\mathsf{T}}$ (GeV)" 
    elif "_eta" in dist: return "$\eta$" 
    elif "_phi" in dist: return "$\phi$" 
    elif "_lxy" in dist: return "$L_{\\mathsf{xy}}$ (mm)" 
    elif "_z" in dist: return "$Z$ (mm)"
    elif "_betagamma" in dist: return "$\\beta\\gamma_{\\mathsf{True}}$" 
    elif "_isolation" in dist: return "isolation" 
    elif "_decaytime" in dist: return "decay time (ns)" 
    elif "_hit_t"     in dist: return "$t_{\\mathsf{hit}}$ (ns)" 
    elif "_hit_delay" in dist: return "$t_{\\mathsf{hit}}-t_{0}$ (ns)" 
    elif "_hit_betaRes" in dist: return "$\\beta_{\\mathsf{TOF}}-\\beta_{\\mathsf{True}}$" 
    elif "_hit_massRes" in dist: return "$m_{\\mathsf{TOF}}-m_{\\mathsf{True}}$ (GeV)" 
    elif "_hit_beta" in dist: return "$\\beta_{\\mathsf{TOF}}$" 
    elif "_hit_invBeta" in dist: return "$1/\\beta_{\\mathsf{TOF}}$" 
    elif "_hit_mass" in dist: return "$m_{\\mathsf{TOF}}$ (GeV)" 
    elif "_m" in dist: return "mass [GeV]"
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
    elif "_hit_t"       in dist: return np.linspace(0,30,60) 
    elif "_hit_delay"   in dist: return np.linspace(-2,10,60) 
    elif "_hit_betaRes" in dist: return np.linspace(-0.2,0.2,50) 
    elif "_hit_massRes" in dist: return np.linspace(-400,400,50) 
    elif "_hit_beta"    in dist: return np.linspace(0,1.2,60) 
    elif "_hit_invBeta" in dist: return np.linspace(0,5,50) 
    elif "_hit_invBetaRes" in dist: return np.linspace(-10,10,50) 
    elif "_hit_mass"       in dist: return np.linspace(0,1200,60) 
    elif "_pt"  in dist: return np.linspace(0,1500,50)
    elif "_eta" in dist: return np.linspace(-5,5,50)
    elif "_phi" in dist: return np.linspace(-4,4,40)
    elif "_lxy" in dist: return np.linspace(0,1500,60)
    elif "_z"   in dist: return np.linspace(-1000,1000,50)
    elif "_betagamma" in dist: return np.linspace(0,30,30)
    elif "_isolation" in dist: return np.linspace(0,3,60)
    elif "_decaytime" in dist: return np.linspace(0,6,60)
    elif "_m"   in dist: return np.linspace(0,1100,50)
    else : 
        bins = xvariable

    return bins


