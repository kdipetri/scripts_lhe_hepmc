import pyhepmc_ng as hep


def getCutVals(cutOpt):
    cut_lxy = 0. # mm 
    cut_z   = 0. # mm
    cut_eta = 0. # rad 
    for opt in cutOpt.split(";"):
        if "lxy" in opt: cut_lxy=float(opt.strip("lxy"))
        if "z"   in opt: cut_z  =float(opt.strip("z"  ))
        if "eta" in opt: cut_eta=float(opt.strip("eta"))
    return(cut_lxy,cut_z,cut_eta)

def passTrackTrigger(stau, cutOpt="lxy1000;z3000;eta2.5" ) :

    # get cut values
    (cut_lxy,cut_z,cut_eta) = getCutVals(cutOpt)
    s="_"+cutOpt

    passStageOne = 0  
    if ( stau["lxy"] > cut_lxy or abs(stau["z"]) > cut_z ) and abs(stau["eta"]) < cut_eta: passStageOne = 1 

    stau["pass_StageOne"+s] = passStageOne

    return stau
