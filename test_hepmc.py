#!/usr/bin/env python

import pyhepmc_ng as hep
from util.get_iso import *
from util.get_timing import *
import os
import json
import argparse

#make certain things configurable
parser = argparse.ArgumentParser(description='Input configuration for running')
parser.add_argument('--mass'    , type=str , default='400', help='slepton mass in GeV')
parser.add_argument('--lifetime', type=str , default='1ns', help='lifetime in ns, eg. 0p01ns') 
parser.add_argument('--nevents' , type=int , default=-1   , help='nevents to run')
parser.add_argument('--doTest'  , type=bool, default=False, help='run a test')

args = parser.parse_args()
mass = args.mass
lifetime = args.lifetime
doTest = args.doTest 
nevents = args.nevents

# Get the file we want to run
infile = "/eos/user/k/kdipetri/Snowmass_HepMC/run_staus/stau_{}_0_{}/events.hepmc".format(mass,lifetime)

# Check that the input file exists 
exists = os.path.isfile(infile)
if exists: 
    print("Running {} GeV, {} lifetime".format(mass,lifetime))
else : 
    print("File not found!")
    print(infile)
    exit()

# For various acceptance 
minLxyTrk = 1100 
minLxyTime = 1150 
minZTrk = 2700
minZTime = 3000
minPt = [2,10,100] 
minNtracks = 1

# For efficiency studies?
#tResBS = 0.2 # 200 ps
#tRes = [1,30,50,100]

# For picking out the staus
pids     = [2000015, 1000015]
statuses = [62,1]
toGeV = 1000.

# Initialize output array 
staus = []

# Reads the file
with hep.open(infile) as f:
  # Just keeps looping
  while True :

    # Try to get an event
    evt = f.read()
    # If it doesn't work, we're at the end of the file. 
    # Just stop.
    if not evt : break
    
    # Stop if this is just a test
    if doTest and evt.event_number > 10 :
      break
    if nevents > 0 and evt.event_number > nevents : break
    if evt.event_number % (nevents/10) == 0 : print("Event",evt.event_number)
    
    # From here on, do things with the event!
    if doTest: print("In event",evt.event_number)
    
    # Get particles with evt.particles
    # Get vertices with evt.vertices
    # Various classes link the two together

    for particle in evt.particles :
    # This is what's in the "particle" class: 
    # http://hepmc.web.cern.ch/hepmc/classHepMC3_1_1GenParticle.html
       if abs(particle.pid) not in pids : continue 
       if particle.status not in statuses : continue
       if doTest : print("This is a stau particle")


       # initialize stau dict
       stau = {}

       # Get the particle four vector
       particlemom = particle.momentum
       stau["eta"] = particlemom.eta() 
       stau["phi"] = particlemom.phi() 
       stau["pt" ] = particlemom.pt()/toGeV 
       stau["p"  ] = particlemom.length()/toGeV 
       stau["m"  ] = particlemom.m()/toGeV 
       stau["betagamma"]  = stau["p"]/stau["m"] 
    
       # Get the vertex where it decays and print its properties
       decayvtx = particle.end_vertex

       # If decayvtx isn't None, it exists and we can look at it.
       if(decayvtx) :

         # Access some of the vertex properties.
         # These are the methods available for the GenVertex class:
         # http://hepmc.web.cern.ch/hepmc/classHepMC3_1_1GenVertex.html
         fourvec = decayvtx.position
         products = decayvtx.particles_out
         if doTest : print("number of decay products is",len(products)) 
 
         # And let's try doing something with the
         # vertex, like assessing its location.
         # the fourvector class is here: 
         # http://hepmc.web.cern.ch/hepmc/classHepMC3_1_1FourVector.html
         if doTest : print("Decay location is: x",fourvec.x,", y",fourvec.y,", z",fourvec.z,", t",fourvec.t)
         stau["lxy"]        =  fourvec.perp() 
         stau["decaytime" ] =  decayTime(particle)  # need to check this
    
       
       # otherwise, this particle isn't decaying
       else :
         if doTest : print("This particle is stable!")
         stau["lxy"] = -1  
         stau["decaytime"] = -1 

       # get isolation 
       stau["isolation"] =  get_iso( particle, evt.particles )

       # get hit timing
       # returns times in ns, takes in resolutions in ps
       stau = getHit(stau,particle,smearOpt="tHit0;tBS0;zBS0") # truth  
       stau = getHit(stau,particle,smearOpt="tHit50;tBS0;zBS0") # hit res only 
       stau = getHit(stau,particle,smearOpt="tHit0;tBS200;zBS0") # beamspot only  
       stau = getHit(stau,particle,smearOpt="tHit0;tBS0;zBS50") # z0 only  
       stau = getHit(stau,particle,smearOpt="tHit50;tBS200;zBS0") # hit + beamspot res  
       stau = getHit(stau,particle,smearOpt="tHit50;tBS200;zBS50") # all

       #stau_hit.append(hit)
       #stau_hit_z.append(z)
       #stau_hit_t.append(t)
       #stau_hit_dist.append(hit_dist)
       #stau_hit_beta.append(hit_beta)
       #stau_hit_mass.append(hit_mass)
       #stau_hit_delay.append(hit_delay)

       staus.append(stau)

data = {
   "staus" : staus,
 #"stau_eta" : stau_eta,
 #"stau_phi" : stau_phi,
 #"stau_pt"  : stau_pt,
 #"stau_p"   : stau_p,
 #"stau_m"   : stau_m,
 #"stau_lxy" : stau_lxy,
 #"stau_betagamma" : stau_betagamma,
 #"stau_decaytime" : stau_decaytime,
 #"stau_isolation" : stau_isolation,
 #"stau_hit" : stau_hit,
 #"stau_hit_r" : stau_hit_r,
 #"stau_hit_z" : stau_hit_z,
 #"stau_hit_t" : stau_hit_t,
 #"stau_hit_dist"  : stau_hit_dist,
 #"stau_hit_beta"  : stau_hit_beta,
 #"stau_hit_mass"  : stau_hit_mass,
 #"stau_hit_delay" : stau_hit_delay,
}

with open('output/stau_{}_{}.json'.format(mass,lifetime), 'w') as fp:
    json.dump(data, fp)
