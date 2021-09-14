#!/usr/bin/env python

import pyhepmc_ng as hep
from util.get_iso import *
from util.get_timing import *
from util.get_trackTrigger import *
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


# Stage 1: Decay in geometric acceptance
tracker_configs=[]
# vary Lxy (N layers)
tracker_configs.append("lxy600;z3000;eta2.5")
tracker_configs.append("lxy800;z3000;eta2.5")
tracker_configs.append("lxy1000;z3000;eta2.5")
tracker_configs.append("lxy1200;z3000;eta2.5")
# vary eta
tracker_configs.append("lxy1200;z3000;eta1.0")
tracker_configs.append("lxy1200;z3000;eta2.5")
tracker_configs.append("lxy1200;z3000;eta4.0")

# Stage 2: Track Selection
timing_configs=[]
timing_configs.append("tHit0;tBS0;zBS0") # truth  
timing_configs.append("tHit50;tBS0;zBS0") # hit res only 
timing_configs.append("tHit0;tBS200;zBS0") # beamspot only  
timing_configs.append("tHit0;tBS0;zBS50") # z0 only  
timing_configs.append("tHit50;tBS200;zBS0") # hit + beamspot res  
timing_configs.append("tHit50;tBS200;zBS50") # all

# vary time delay (ns) 
track_sels=[]
track_sels.append("pt10;delay0.5")
track_sels.append("pt10;delay1.0")
track_sels.append("pt10;delay2.0")
# vary pt
track_sels.append("pt10;delayNone")
track_sels.append("pt20;delayNone")
track_sels.append("pt50;delayNone")
track_sels.append("pt100;delayNone")
# vary mass? needs pt smearing


# For picking out the staus
pids     = [2000015, 1000015]
statuses = [62,1]
toGeV = 1000.

# Initialize output arrays 
staus = [] # stau level info
events = [] # event level info

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

    # Initialize event dict
    event = {}
    
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
         stau["z"]          =  fourvec.z 
         stau["decaytime" ] =  decayTime(particle)  # need to check this
    
       
       # otherwise, this particle isn't decaying
       else :
         if doTest : print("This particle is stable!")
         # set decay values to arbitrarily large values
         stau["lxy"] = 999999
         stau["z"]   = 999999  
         stau["decaytime"] = 999999 

       # get isolation 
       stau["isolation"] =  get_iso( particle, evt.particles )

       # Stage One Selection 
       # Is the stau in acceptance (decaying past the tracker)
       for tracker_config in tracker_configs: 
            stau = passStageOne(stau,cutOpt=tracker_config)

            pass_sel = "pass_StageOne_"+tracker_config
            nstau = "nStau_"+pass_sel
            if pass_sel in event : event[nstau] += stau[pass_sel] # key exists  
            else : event[nstau] = stau[pass_sel]

       # Stage Two Selection: stau pT and/or delay 
       # Use timing layer hit
       # returns hit times in ns, takes in resolutions in ps
       pass_sel1 = "pass_StageOne_lxy1200;z3000;eta2.5" # need to make sure we hit the timing layer

       for timing_config in timing_configs: 
            stau = getHit(stau,particle,smearOpt=timing_config) 

            for track_sel in track_sels: 
                stau = passStageTwo(stau,cutOpt=track_sel,smearOpt=timing_config) 

                pass_sel2 = "pass_StageTwo_"+track_sel+"_"+timing_config
                nstau = "nStau_"+pass_sel2
                #print(stau[pass_sel1], stau[pass_sel2], stau[pass_sel1]*stau[pass_sel2])
                if pass_sel2 in event : event[nstau] += stau[pass_sel1] * stau[pass_sel2] # key exists  
                else : event[nstau] = stau[pass_sel1] * stau[pass_sel2]




       staus.append(stau)
       # end stau loop
    
    # 
    # compute if event has at least one stau passing trigger 
    #

    # stage 1
    for tracker_config in tracker_configs: 
        pass_sel = "pass_StageOne_"+tracker_config
        nstau = "nStau_"+pass_sel
        event[pass_sel] =  event[nstau] >= 1

    # stage 2
    for timing_config in timing_configs: 
       for track_sel in track_sels: 
            pass_sel = "pass_StageTwo_"+track_sel+"_"+timing_config
            nstau = "nStau_"+pass_sel
            event[pass_sel] =  event[nstau] >= 1

    events.append(event)
    # end event loop

data = {
    "staus" : staus,
    "events" : events,
}

with open('output/stau_{}_{}.json'.format(mass,lifetime), 'w') as fp:
    json.dump(data, fp)
