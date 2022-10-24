#!/usr/bin/env python

from particle import Particle
from util.passTrackTrigger import *
import ROOT 
import pyhepmc as hep
import os
import json
import math
import argparse

#make certain things configurable
parser = argparse.ArgumentParser(description='Input configuration for running')
parser.add_argument('--sample'  , type=str , default="qcd", help='input signal sample')
parser.add_argument('--nevents' , type=int , default=-1   , help='nevents to run')
parser.add_argument('--doTest'  , type=bool, default=False, help='run a test')

args = parser.parse_args()
doTest  = args.doTest 
nevents = args.nevents
sample = args.sample

# Get the file we want to run
# Units are in mm and GeV for qcd, sueps
# Units are in mm and MeV for higgs, staus
#sample = "qcd"
#sample = "higgsportal_125_40_0p1ns"
#sample = "higgsportal_125_55_1ns"
#sample = "stau_300_0p1ns"
#sample = "stau_300_1ns"
#sample = "stau_300_stable"
infile = "inputs/{}.hepmc".format(sample)

GeV = 1000. if "higgs" in sample or "stau" in sample else 1.

# Check that the input file exists 
exists = os.path.isfile(infile)
if exists: 
    print("Running {}".format(sample))
else : 
    print("File not found!")
    print(infile)
    exit()


# Stage 1: Decay in geometric acceptance
prompt_configs=[]
prompt_configs.append("pt0.5")
prompt_configs.append("pt1.0")
prompt_configs.append("pt1.5")
prompt_configs.append("pt2.0")

# Stage 2: Track Selection
displaced_configs=[]
displaced_configs.append("pt0.5;d050")
displaced_configs.append("pt1.0;d050")
displaced_configs.append("pt2.0;d050")
displaced_configs.append("pt10.0;d050")
displaced_configs.append("pt1.0;d0100")
displaced_configs.append("pt2.0;d0100")
displaced_configs.append("pt10.0;d0100")

# Initialize output arrays 
tracks = [] # all status 1 stable tracks?
events = [] # event level info
event_tracks = [] # tracks per event...


charged_pids = [543, 5334, 5314, 20413, 4122, 4124]
neutral_pids = [35,5212, 5214, 551]
keeps = [1000015,2000015,1000039,2000039]
# Get charge
def isCharged(particle):
    if abs(particle.pid) == 1000015 : return 1
    if abs(particle.pid) == 2000015 : return 1
    if abs(particle.pid) == 1000039 : return 1
    if abs(particle.pid) == 2000039 : return 1
    if abs(particle.pid) > 9000000 : return 0
    if abs(particle.pid) > 5122 and abs(particle.pid) < 5555 : return 0 # bottom
    if abs(particle.pid) > 4122 and abs(particle.pid) < 4445 : return 0 # bottom
    if abs(particle.pid) in charged_pids : return 1
    if abs(particle.pid) in neutral_pids : return 0
    part = Particle.from_pdgid(particle.pid)
    if part.charge !=0 : return 1
    else : return 0

def deltaPhi( p1, p2):
    '''Computes delta phi, handling periodic limit conditions.'''
    res = p1 - p2
    while res > math.pi:
        res -= 2*math.pi
    while res < -math.pi:
        res += 2*math.pi
    return res


# Reads the file
num = 0
with hep.open(infile) as f:
  # Just keeps looping
  while True :
    num+=1

    # Try to get an event
    evt = f.read()
    # If it doesn't work, we're at the end of the file. 
    # Just stop.
    # print(evt)
    if not evt : break
    
    # Stop if this is just a test
    if doTest and evt.event_number > 100 :
      break
    if nevents > 0 and evt.event_number > nevents : break
    if evt.event_number % 1000 == 0 : print("Event",evt.event_number)

    # From here on, do things with the event!
    if doTest: print("In event",evt.event_number)


    # Initialize event dict
    event = {}
    event["weight"]= evt.weights[0]

    # get a z0 per event
    z0 = random.gauss(0.0,50.0) # 50 mm spread in z 
    event["z0"] = z0

    sumpt  = "sumpt2_pass_prompt_pt1.0"
    event[sumpt] = 0
    for prompt_config in prompt_configs: 
         ntrack = "nTrack_pass_prompt_"+prompt_config
         event[ntrack] = 0 # ensure key exists  

    for displaced_config in displaced_configs: 
         ntrack = "nTrack_pass_displaced_"+displaced_config
         event[ntrack] = 0 # ensure key exists  

    # Get particles with evt.particles
    # Get vertices with evt.vertices
    # Various classes link the two together

    evt_tracks = []

    # Select tracks from all particles
    met_v = ROOT.TLorentzVector()
    met_v.SetPtEtaPhiM(0,0,0,0)
    trk_v = ROOT.TLorentzVector()
    trk_v.SetPtEtaPhiM(0,0,0,0)

    for particle in evt.particles :
    # This is what's in the "particle" class: 
    # http://hepmc.web.cern.ch/hepmc/classHepMC3_1_1GenParticle.html

       # Select only charged status 1 or 2 particles
       if particle.status > 1 : continue  #and (abs(particle.pid) not in keeps): continue
       if not isCharged(particle) : continue 

       # initialize track dict
       track = {}

       # Get the particle four vector
       particlemom = particle.momentum
       track["eta"] = particlemom.eta() 
       track["phi"] = particlemom.phi() 
       track["pt" ] = particlemom.pt()/GeV 
       track["px" ] = particlemom.px/GeV 
       track["py" ] = particlemom.py/GeV 
       track["pz" ] = particlemom.pz/GeV 
       track["p"  ] = particlemom.length()/GeV 
       track["m"  ] = particlemom.m()/GeV
       #track["betagamma"]  = track["p"]/track["m"] 

       # apply basic acceptance requirements
       if track["pt"] < 0.5 : continue # GeV
       if abs(track["eta"]) > 2.5 : continue
    
       # Get the production and decay vertices 
       prodvtx  = particle.production_vertex
       decayvtx = particle.end_vertex

       if (prodvtx) :
            prodvec = prodvtx.position
            track["prod_rxy"]  =  prodvec.perp() 
            track["prod_x"] = prodvec.x
            track["prod_y"] = prodvec.y
            track["prod_z"] = prodvec.z + z0
            if doTest : 
                print("Prod vtx: x",prodvec.x,", y",prodvec.y,", z",prodvec.z,", t",prodvec.t)
       else : 
            track["prod_rxy"] = 0. 
            track["prod_x"] = 0. 
            track["prod_y"] = 0.
            track["prod_z"] = 0.

       # If decayvtx isn't None, it exists and we can look at it.
       if(decayvtx) :

            # Access some of the vertex properties.
            # These are the methods available for the GenVertex class:
            # http://hepmc.web.cern.ch/hepmc/classHepMC3_1_1GenVertex.html
            decayvec = decayvtx.position
            products = decayvtx.particles_out
            if doTest : print("number of decay products is",len(products)) 
 
            # And let's try doing something with the decay vector
            # http://hepmc.web.cern.ch/hepmc/classHepMC3_1_1FourVector.html
            if doTest : print("Decay location is: x",decayvec.x,", y",decayvec.y,", z",decayvec.z,", t",decayvec.t)
            track["decay_rxy"]  =  decayvec.perp() 
            track["decay_x"]    =  decayvec.x 
            track["decay_y"]    =  decayvec.y 
            track["decay_z"]    =  decayvec.z + z0 
    
       # otherwise, this particle isn't decaying
       else :
            if doTest : print("This particle is stable!")
            # set decay values to arbitrarily large values
            track["decay_rxy"]  =  99999  
            track["decay_x"]    =  99999  
            track["decay_y"]    =  99999  
            track["decay_z"]    =  99999  

    
       Lxy = track["decay_rxy"] - track["prod_rxy"]

       # basic acceptance cuts
       if Lxy < 200 : continue # require 200 mm track length 

       # get an approximate d0 = Rxy*sin(dPhi), 
       # where dPhi is between the PV-to-DV vector 
       # and the track from the DV
       dPhi = deltaPhi( prodvec.phi(), track["phi"] )
       d0   = track["prod_rxy"]*math.sin(abs(dPhi));
       if doTest : 
           print( 'pt', track["pt"] ) 
           print( "phi1, phi2, dPhi:", prodvec.phi(), track["phi"], dPhi)
           print( "rxy, d0:", track["prod_rxy"], d0)
       track["d0"] = d0
       track["length"] = Lxy
    

       # Prompt Track Selection 
       for prompt_config in prompt_configs: 
            if passPrompt(track,z0,cutOpt=prompt_config):
                pass_sel = "pass_prompt_"+prompt_config
                ntrack = "nTrack_"+pass_sel
                event[ntrack] += 1   
                if "pt1.0" in prompt_config: 
                    event[sumpt] += 1*(track["pt"]**2)
                    trk_v.SetPtEtaPhiM( track["pt"],  track["eta"],  track["phi"], 0.103)
                    met_v += trk_v 

       # Displaced Track Selection 
       for displaced_config in displaced_configs: 
            if passDisplaced(track,cutOpt=displaced_config) :
                pass_sel = "pass_displaced_"+displaced_config
                ntrack = "nTrack_"+pass_sel
                event[ntrack] += 1   
       

       # end track loop
       # only save tracks passing a reasonable pt cut  
       if track["pt"] < 1.0: continue 
       evt_tracks.append(track)

    # update PV info with met sum
    event[sumpt] += met_v.Pt()**2 
    
    if doTest : print( "PV ntracks, sumpt2 : ", event["nTrack_pass_prompt_pt1.0"], event["sumpt2_pass_prompt_pt1.0"]) 
    events.append(event)
    event_tracks.append(evt_tracks)
    # end event loop

data = {
    "events" : events,
    "event_tracks" : event_tracks,
}

if doTest==False :
    with open('output/{}_forpileup.json'.format(sample), 'w') as fp:
        json.dump(data, fp)
