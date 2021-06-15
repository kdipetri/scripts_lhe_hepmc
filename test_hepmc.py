#!/usr/bin/env python

import pyhepmc_ng as hep
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

# If this is true, stop after 10 events

stau_eta = []
stau_phi = []
stau_pt = []
stau_m = []
stau_lxy = []
stau_betagamma = []
stau_decaytime = []

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
    if evt.event_number % 1000 == 0 : print("Event",evt.event_number)

    # From here on, do things with the event!
    if doTest: print("In event",evt.event_number)
 
    # Get particles with evt.particles
    # Get vertices with evt.vertices
    # Various classes link the two together

    for particle in evt.particles :
    # This is what's in the "particle" class: http://hepmc.web.cern.ch/hepmc/classHepMC3_1_1GenParticle.html
      #print(particle.id," ",particle.pid)
      if abs(particle.pid)==2000015 and particle.status==62 :
        if doTest : print("This is a stau particle")

        # Get the particle four vector
        particlemom = particle.momentum
        stau_eta.append( particlemom.eta() )
        stau_phi.append( particlemom.phi() )
        stau_pt .append( particlemom.pt()/1000. )
        stau_m  .append( particlemom.m()/1000. )
        mag = ( particlemom.px**2 + particlemom.py**2 + particlemom.pz**2 )**0.5
        stau_betagamma.append( mag  / particlemom.m() )
    
        # Get the vertex where it decays and print its properties
        decayvtx = particle.end_vertex

        # If decayvtx isn't None, it exists and we can look at it.
        if(decayvtx) :

          # Access some of the vertex properties.
          # These are the methods available for the GenVertex class:
          # http://hepmc.web.cern.ch/hepmc/classHepMC3_1_1GenVertex.html
          status = decayvtx.status
          fourvec = decayvtx.position
          products = decayvtx.particles_out
          if doTest : print("number of decay products is",len(products)) 
 
          # And let's try doing something with the
          # vertex, like assessing its location.
          # The FourVector class is here: 
          # http://hepmc.web.cern.ch/hepmc/classHepMC3_1_1FourVector.html
          if doTest : print("Decay location is: x",fourvec.x,", y",fourvec.y,", z",fourvec.z,", t",fourvec.t)
          stau_lxy       .append( fourvec.perp() )
          stau_decaytime .append( fourvec.t ) # need to check this
    

        # Otherwise, this particle isn't decaying
        else :
          if doTest : print("This particle is stable!")


data = {
 "stau_eta" : stau_eta,
 "stau_phi" : stau_phi,
 "stau_pt"  : stau_pt,
 "stau_m"   : stau_m,
 "stau_lxy" : stau_lxy,
 "stau_betagamma" : stau_betagamma,
 "stau_decaytime" : stau_decaytime,
}

with open('output/stau_{}_{}.json'.format(mass,lifetime), 'w') as fp:
    json.dump(data, fp)
