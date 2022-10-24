import ROOT 
import math
import random

c=299792458 #m/s


def velocity(track) : # returns velocity in mm/s

    # Compute velocity
    # velocity = beta * c
    # velocity = betagamma / gamma * c  

    betagamma = track["p"]/track["m"] 
    gamma = ( 1 + (betagamma)**2 )**0.5
    velocity = betagamma/gamma * c * 1000. # in mm per second

    #print("velocity", track["p"], track["m"], betagamma, velocity)
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

    
def momentumSmear(p,res):

    pSmear = random.gauss( p , res * p ) 
    if pSmear < 0 : pSmear = momentumSmear(res,p)
    if pSmear > 10000 : pSmear = momentumSmear(res,p)
    return pSmear

def getHit(track, r_=1150, z_=3000  ) : 
    # computes hit time for cylindrical detector
    #   barrel: fixed r(xy)_ variable z
    #   endcap: variable r(xy)_, fixed z
    #   assumes barrel and endcap meet at r(xy)_,z
    #   default values for MIP timing detector 
    # returns a dictionary "hit" with the following information 
    #     r(xy) and z in mm
    #     and time in ns 
    
    # step0 parse options
    sig_tHit = 50/1000. #50 ps, in ns

    # step 1 find Z0, t0 from beamspot spread
    z0= track["prod_z"] # already has beamspot spread 
    t0= 0 # assume we know timespread

    track["hit_z0"] = z0
    track["hit_t0"] = t0

    # step 2 find the particle's distance traveled, dist, and hit r=rxy,z
    v = ROOT.TLorentzVector()
    v.SetPtEtaPhiM( track["pt"] ,track["eta"], track["phi"], track["m"])
    theta=v.Theta()
    
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
    #print("r,z,dist",r,z,dist)

    # save hit distances
    dist_origin = (r**2+z**2)**0.5 # assumes you don't know z0
    track["hit_z"] = z
    track["hit_r"] = r
    track["hit_R"] = dist #_origin 

    # step 3, find hit time
    t=dist/velocity(track)*1e9 # in ns
    
    # step 5, smear hit time by hit res
    hitres=random.gauss(0.0, sig_tHit)

    #print('t,t0,hitres',t,t0,hitres)
    t=t+t0+hitres
    track["hit_time"] = t 

    # test
    # print(r,eta,theta,z,t)

    # return other useful info
    
    # beta = v/c = d/t /c 
    beta = ( dist  / 1e3 )/( t / 1e9 )/c #measured beta
    invBeta = 1./beta if beta > 0.1 else 10 # inverse beta
    gamma = 1.0/(1-beta**2)**0.5  if beta < 1  else 100 # measured gamma


    # momentum smearing sigma(pT)/pT = A * pT (meas errr) + const. (multiple scattering)
    # 0.02 * pT for barrel, 7% for endcaps?
    # fix this later!! or make CMS dependent
    res = 0.02
    if abs(track["eta"]) > 0.7 : res = 0.03
    if abs(track["eta"]) > 1.5 : res = 0.03 + (abs(track["eta"])-1.5)*0.20
    if track["p"] > 100.: res = res + 0.01 * track["p"] /100. #  

    pSmear = momentumSmear(track["p"],res)
    
    #print( track["p"], track["eta"], res, pSmear )

    mass = 0.
    if beta < 1. and beta > 0. :
        mass = pSmear/(beta*gamma) 

    betaRes = beta - velocity(track) / c / 1000.
    invBetaRes = invBeta - 1.0 / ( velocity(track) / c / 1000. )
    massRes = mass - track["m"]

    # debugging
    #if beta < 0 : 
    #    print( track["pdgID"],track["pt"], track["eta"], track["phi"], track["m"])
    #    print(beta,gamma,mass,betaRes,massRes)

    track["hit_beta"] = beta 
    track["hit_betaRes"] = betaRes 
    track["hit_invBeta"] = invBeta  
    track["hit_invBetaRes"] = invBetaRes  
    track["hit_gamma"] = gamma  
    track["hit_mass"] = mass 
    track["hit_massRes"] = massRes 
    
    # delay = time difference with respect to particle with beta=1
    # assumes we know z0 
    # hit_delay = t - ( hit_dist * 1e-3 )/c * 1e9 # ns
    track["hit_delay"] = t  - ( dist / 1e3 )/c*1e9  

    #print ("p","delay","b","m",track["p"],track["hit_delay"], beta, mass)

    # for testing
    #print(track)
    return track # r,z in mm, t in ns 

    

