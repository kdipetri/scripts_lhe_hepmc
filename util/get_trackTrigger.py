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
    cut_pt    = 0. # GeV 
    cut_delay = 0. # ns 
    for opt in cutOpt.split(";"):
        if "pt "     in opt: cut_lxy=float(opt.strip("pt"))
        if "delay"   in opt: 
            if "None" in opt: cut_delay=-9999
            else : cut_delay  =float(opt.strip("delay"))
    return(cut_pt,cut_delay)

def passStageTwo(stau, cutOpt="pt10;delayNone" , smearOpt="tHit50;tBS200;zBS50") :

    # get cut values
    (cut_pt,cut_delay) = getStageTwoCutVals(cutOpt)
    s="_"+cutOpt+"_"+smearOpt

    passStageTwo = 0  
    if  stau["pt"] > cut_pt and stau["hit_delay_"+smearOpt] > cut_delay: passStageTwo = 1 

    stau["pass_StageTwo"+s] = passStageTwo

    return stau
