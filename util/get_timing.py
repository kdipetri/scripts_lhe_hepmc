import math
import random
import pyhepmc_ng as hep

c=299792458 #m/s


def velocity(particle) : # returns velocity in mm/s

    # Compute velocity
    # velocity = beta * c
    # velocity = betagamma / gamma * c  

    betagamma = particle.momentum.length()/particle.momentum.m() 
    gamma = ( 1 + (betagamma)**2 )**0.5
    velocity = betagamma/gamma * c * 1000. # in mm per second

    return velocity
    
def decayTime(particle):
    # finds a particle's decay time in nanoseconds 
    
    decayvtx = particle.end_vertex
    if (decayvtx) :
        
        # Decay time = decay length/velocity

        decay_pos  = decayvtx.position.length() # in mm
        decay_time = decay_pos/(velocity(particle))*1e9 # in nanoseconds

        return decay_time # in ns 
    else : return -1 # particle is stable

def getSmearVals(smearOpt):
    sig_tHit = 0. # ns
    sig_tBS  = 0. # ns
    sig_zBS  = 0. # mm 
    for opt in smearOpt.split(";"):
        if "tHit" in opt: sig_tHit=float(opt.strip("tHit"))/1000.
        if "tBS"  in opt: sig_tBS =float(opt.strip("tBS" ))/1000.
        if "zBS"  in opt: sig_zBS =float(opt.strip("zBS" ))
    return(sig_tHit,sig_tBS,sig_zBS)
    
def getHit(stau, particle, r_=1150, z_=3000, smearOpt="tHit50;tBS200;zBS50" ) : 
    # computes hit time for cylindrical detector
    #   barrel: fixed r(xy)_ variable z
    #   endcap: variable r(xy)_, fixed z
    #   assumes barrel and endcap meet at r(xy)_,z
    #   default values for MIP timing detector 
    # returns a dictionary "hit" with the following information 
    #     r(xy) and z in mm
    #     and time in ns 
    
    # step0 parse options
    (sig_tHit,sig_tBS,sig_zBS) = getSmearVals(smearOpt)
    # remove default opt
    #s="" if smearOpt=="tHit50;tBS200;zBS50" else "_"+smearOpt
    s="_"+smearOpt

    # step 1 find Z0, t0 from beamspot spread
    z0=random.gauss(0.0, sig_zBS) # default sigma 50 mm
    t0=random.gauss(0.0, sig_tBS) # default 200 ps gauss

    stau["hit_z0"+s] = z0
    stau["hit_t0"+s] = t0

    # step 2 find the particle's distance traveled, dist, and hit r=rxy,z
    eta=particle.momentum.eta()
    theta=particle.momentum.theta()
    if (theta)>math.pi/2 : theta=abs(theta-math.pi)
    
    # First we do math for a barrel scenario 
    r=r_
    z=abs(z0+r_/math.tan(theta))
    dist=r_/math.sin(theta)
    if z > z_: # we actually need to do math for the endcap scenario
        z=z_
        r=(z_-z0)*math.tan(theta)
        dist=(z_-z0)/math.cos(theta)
        if r>r_ : print("OOPs something is wrong")
    # TODO:
    # add checks for if particle decays before layers
    # add checks for if particle eta is too large 

    # save hit distances
    dist_origin = (r**2+z**2)**0.5 # assumes you don't know z0
    stau["hit_z"+s] = z
    stau["hit_r"+s] = r
    stau["hit_R"+s] = dist_origin 

    # step 3, find hit time
    t=dist/velocity(particle)*1e9 # in ns
    
    # step 5, smear hit time by hit res
    hitres=random.gauss(0.0, sig_tHit)

    t=t+t0+hitres
    stau["hit_time"+s] = t 

    # test
    # print(r,eta,theta,z,t)

    # return other useful info
    
    # beta = v/c = d/t /c 
    beta = ( dist_origin  / 1e3 )/( t / 1e9 )/c #measured beta
    gamma = 1.0/(1-beta**2)**0.5 if beta < 1 else 100 # measured gamma
    mass = stau["p"]/(beta*gamma) if beta < 1 else 0

    betaRes = beta - velocity(particle) / c / 1000.
    massRes = mass - stau["m"]

    stau["hit_beta"+s] = beta 
    stau["hit_betaRes"+s] = betaRes 
    stau["hit_gamma"+s] = gamma  
    stau["hit_mass"+s] = mass 
    stau["hit_massRes"+s] = massRes 
    
    # delay = time difference with respect to particle with beta=1
    # assumes we dont know z0
    # hit_delay = t - ( hit_dist * 1e-3 )/c * 1e9 # ns
    stau["hit_delay"+s] = t  - ( dist_origin / 1e3 )/c*1e9  

    # for testing
    #print(stau)
    return stau # r,z in mm, t in ns 

    

