#!/usr/bin/env python

import pyhepmc_ng as hep

infile = "/eos/user/k/kpachal/TrackTrigStudies/HepMCFiles/higgsportal/higgsportal_125_35_1ns.hepmc"

# If this is true, stop after 10 events
doTest = True

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

    # From here on, do things with the event!
    print("In event",evt.event_number)
 
    # Get particles with evt.particles
    # Get vertices with evt.vertices
    # Various classes link the two together

    for particle in evt.particles :
    # This is what's in the "particle" class: http://hepmc.web.cern.ch/hepmc/classHepMC3_1_1GenParticle.html
      #print(particle.id," ",particle.pid)
      if (abs(particle.pid)==35) :
        print("This is a H0 particle")

        # Get the particle four vector
        particlemom = particle.momentum
        thiseta = particlemom.eta()
        print(thiseta)

        # Get the vertex where it decays and print its properties
        decayvtx = particle.end_vertex
        print(decayvtx)

        # If decayvtx isn't None, it exists and we can look at it.
        if(decayvtx) :

          # Access some of the vertex properties.
          # These are the methods available for the GenVertex class:
          # http://hepmc.web.cern.ch/hepmc/classHepMC3_1_1GenVertex.html
          status = decayvtx.status
          fourvec = decayvtx.position
          products = decayvtx.particles_out
          print(status,fourvec,"number of decay products is",len(products)) 
 
          # And let's try doing something with the
          # vertex, like assessing its location.
          # The FourVector class is here: 
          # http://hepmc.web.cern.ch/hepmc/classHepMC3_1_1FourVector.html
          print("Decay location is: x",fourvec.x,", y",fourvec.y,", z",fourvec.z,", t",fourvec.t)

        # Otherwise, this particle isn't decaying
        else :
          print("This particle is stable!")

