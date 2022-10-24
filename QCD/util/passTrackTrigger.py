import pyhepmc_ng as hep
import random

# prompt cuts
cut_prod = 300. #mm https://arxiv.org/abs/2203.07314
cut_rxy = 1000. #mm
cut_z   = 3000. #mm
cut_eta = 2.5
cut_d0  = 1.0 #mm

def passes_d0_cut(d0track, d0cut):

    # Assume tracking efficiency decreases linearly w/ d0
    rng_check = random.random() # returns a number between 0 and 1

    y_inter = 1.0 
    effslope = -1.0/d0cut
    eff = effslope*d0track + y_inter
    if rng_check < eff: return True
    else: return False

def promptCutVals(cutOpt):
    cut_pt   = 0. # GeV 
    for opt in cutOpt.split(";"):
        if "pt"  in opt: cut_pt =float(opt.strip("pt" ))
    return(cut_pt)

def passPrompt(track,z0, cutOpt="pt1.0;" ) :

    # get cut values
    (cut_pt) = promptCutVals(cutOpt)
    s="_"+cutOpt

    passPrompt = 1  
    if ( track["decay_rxy"] < cut_rxy and abs(track["decay_z"]) < cut_z ) : passPrompt = 0 
    if  abs(track["eta"]) > cut_eta : passPrompt = 0 
    if track["pt"] < cut_pt : passPrompt = 0 
    if track["d0"] > cut_d0 : passPrompt = 0 
    if abs(track["prod_z"] - z0) > 1 : passPrompt = 0

    return passPrompt 

def displacedCutVals(cutOpt):
    cut_pt   = 0. # GeV 
    max_d0   = 99999. # mm  

    for opt in cutOpt.split(";"):
        if "pt"   in opt: cut_pt    = float(opt.strip("pt"))
        if "d0"   in opt: max_d0    = float(opt.strip("d")) 
    return(cut_pt,max_d0)

def passDisplaced(track, cutOpt="pt1.0;d010") :

    # get cut values
    (cut_pt,max_d0) = displacedCutVals(cutOpt)
    s="_"+cutOpt

    passDisplaced = 1  
    if ( track["decay_rxy"] < cut_rxy and abs(track["decay_z"]) < cut_z ) : passDisplaced = 0 
    if  track["prod_rxy"] > cut_prod : passDisplaced = 0
    if  abs(track["eta"]) > cut_eta : passDisplaced = 0
    if  track["pt"] < cut_pt : passDisplaced = 0
    if  track["d0"] < cut_d0 : passDisplaced = 0 
    #if  track["d0"] > max_d0 : passDisplaced = 0 # replace w/ linearly decreasing slope
    if  passes_d0_cut(track["d0"], max_d0) == 0: passDisplaced = 0

    return  passDisplaced 

