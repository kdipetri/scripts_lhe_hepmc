import math

def visible(particle):
    # don't count neutrinos
    invisible = [12,14,16] # can add more if needed 
    if abs(particle.pid) in invisible : return False
    if abs(particle.pid) > 999999 : return False
    else : return True 

def deltaR(eta1,phi1,eta2,phi2):
    dEta = abs(eta1-eta2)
    dPhi = abs(phi1-phi2)
    if dPhi > math.pi : dPhi = abs(dPhi - 2*math.pi)
    # kdp: CHECK THIS WHEN WIFI
    #print(phi1,phi2,dPhi)

    return (dEta*dEta+dPhi*dPhi)**0.5

def get_iso(part,evt_particles,dR_cut=0.3):
    # This function computes the isolation of "part" 
    # Isolation = scalar sum of status 1 particles in a cone of dR_cut=0.3 around "part"
    # Divided by the "part" momentum

    sum_pt = 0
    # Loop over all particles
    for evt_particle in evt_particles:
       
        if evt_particle.status is not 1: continue # only keep status 1
        if not visible(evt_particle): continue # skip SUSY particle & neutrinos
        trk = evt_particle.momentum
        dR = deltaR(part.momentum.eta(),part.momentum.phi(),trk.eta(),trk.phi())
        if dR > dR_cut : continue # only keep in dR cone
    
        sum_pt += trk.pt() 

    iso = sum_pt / part.momentum.pt()
    #print(iso)
    return iso 
