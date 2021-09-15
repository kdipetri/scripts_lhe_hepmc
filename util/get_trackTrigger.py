import pyhepmc_ng as hep


def getStageOneCutVals(cutOpt):
    cut_lxy = 0. # mm 
    cut_z   = 0. # mm
    cut_eta = 0. # rad 
    for opt in cutOpt.split(";"):
        if "lxy" in opt: cut_lxy=float(opt.strip("lxy"))
        if "z"   in opt: cut_z  =float(opt.strip("z"  ))
        if "eta" in opt: cut_eta=float(opt.strip("eta"))
    return(cut_lxy,cut_z,cut_eta)

def passStageOne(stau, cutOpt="lxy1000;z3000;eta2.5" ) :

    # get cut values
    (cut_lxy,cut_z,cut_eta) = getStageOneCutVals(cutOpt)
    s="_"+cutOpt

    passStageOne = 0  
    if ( stau["lxy"] > cut_lxy or abs(stau["z"]) > cut_z ) and abs(stau["eta"]) < cut_eta: passStageOne = 1 

    stau["pass_StageOne"+s] = passStageOne

    return stau

def getStageTwoCutVals(cutOpt):
    cut_pt    = -9999. # GeV 
    cut_delay = -9999 # ns 
    cut_beta  = 9999 #  
    cut_mass  = -9999 # GeV

    for opt in cutOpt.split(";"):
        if "pt"      in opt: cut_pt    =float(opt.strip("pt"))
        if "delay"   in opt: cut_delay = float(opt.strip("delay")) 
        if "beta"    in opt: cut_beta = float(opt.strip("beta"))
        if "mass"    in opt: cut_mass = float(opt.strip("mass"))
    return(cut_pt,cut_delay,cut_beta,cut_mass)

def passStageTwo(stau, cutOpt="pt10;None" , smearOpt="tHit50;tBS200;zBS50") :

    # get cut values
    (cut_pt,cut_delay,cut_beta,cut_mass) = getStageTwoCutVals(cutOpt)
    s="_"+cutOpt+"_"+smearOpt

    passStageTwo = 1  
    if  stau["pt"] < cut_pt  : passStageTwo = 0
    if  stau["hit_delay_"+smearOpt] < cut_delay: passStageTwo = 0 
    if  stau["hit_beta_"+smearOpt] > cut_beta: passStageTwo = 0
    if  stau["hit_mass_"+smearOpt] < cut_mass: passStageTwo = 0
    #print(cut_pt, stau["pt"], passStageTwo)

    stau["pass_StageTwo"+s] = passStageTwo

    return stau
