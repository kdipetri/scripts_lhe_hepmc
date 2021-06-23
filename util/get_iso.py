import math
import pyhepmc_ng as hep

def visible(particle):
    # don't count neutrinos
    invisible = [12,14,16] # can add more pdgIds here if needed 
    if abs(particle.pid) in invisible : return False
    if abs(particle.pid) > 999999 : return False
    else : return True 

def get_iso(particle,other_particles,dR_cut=0.3):
    # This function computes the isolation of "particle" 
    # Isolation = scalar sum of status 1 particles in a cone of dR_cut=0.3 around "partcle"
    # Divided by the "particle" momentum

    sum_pt = 0
    # Loop over all particles
    for trk in other_particles:
       
        if trk.status is not 1: continue # only keep status 1
        if not visible(trk): continue # skip SUSY particle & neutrinos
        dR = hep.delta_r_eta(particle.momentum,trk.momentum)
        if dR > dR_cut : continue # only keep in dR cone
    
        sum_pt += trk.momentum.pt() 

    iso = sum_pt / particle.momentum.pt()
    #print(iso)
    return iso 
