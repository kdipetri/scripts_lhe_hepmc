#!/usr/bin/env python
import argparse
import pyhepmc_ng as hep
import numpy
import math
import glob
import json
import numpy as np
import uproot4 as uproot
import scipy.interpolate
from scipy.interpolate import griddata
from scipy.interpolate import interpn
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
from random import seed
from random import random
from matplotlib import colors as mcolors
import colorsys

plt.ioff()

parser = argparse.ArgumentParser(description='process model')
parser.add_argument('model'  , type=str , default='staus', help='benchmark model: higgs or staus')

args = parser.parse_args()
model = args.model 
higgs = 'higgs'
staus = 'staus'
doTest = False #True# False 
maxevents = -1 


# Get Input files 
file_lists = {}
if model == higgs:
    cap_mod = 'Higgs'
    masses = [5,8,15,25,40,55]
    lifes  = ["0p01ns","0p1ns","1ns"]
    if doTest: 
        masses = [55]
        lifes = ["1ns"]
    for m in masses:
        for l in lifes:
            file_lists[m,l] = glob.glob("/eos/user/k/kdipetri/Snowmass_HepMC/run_higgsportal/higgsportal_125_%d_%s/events.hepmc"%(m,l))
    #=====================================================================================================
elif model == staus:
    cap_mod = 'Stau'
    #masses = [100,300,500]
    masses = [100,200,300,400,500,600]
    lifes  = ["0p01ns","0p1ns","1ns"]
    if doTest : 
        masses = [600]
        lifes  = ["1ns"]
    for m in masses:
        for l in lifes:
            file_lists[m,l] = glob.glob("/eos/user/k/kdipetri/Snowmass_HepMC/run_staus/stau_%d_0_%s/events.hepmc"%(m,l))
    #=====================================================================================================
else:
    print('Please enter either higgs or staus (case sensitive)')

zero = numpy.array([0,0,0])

charged_list = [1, 2, 3, 4, 5, 6, 7, 8, 11, 13, 15, 17, 24, 34, 37, 38, 62, 1000011, 1000013,
    1000015, 2000011, 2000013, 2000015, 2000024, 2000037, 211, 9000211, 100211,
    10211, 9010211, 213, 10213, 20213, 9000213, 100213, 9010213, 9020213, 30213,
    9030213, 9040213, 215, 10215, 9000215, 9010215, 217, 9000217, 9010217, 219,
    321, 9000321, 10321, 100321, 9010321, 9020321, 323, 10323, 20323, 100323,
    9000323, 30323, 325, 9000325, 10325, 20325, 9010325, 9020325, 327, 9010327, 329,
    9000329, 411, 10411, 413, 10413, 20413, 415, 431, 10431, 433, 10433, 20433, 435,
    521, 10521, 523, 10523, 20523, 525, 541, 10541, 543, 10543, 20543, 545, 2224,
    2214, 1114, 3222, 3112, 3224, 3114, 3312, 3314, 3334, 4122, 4222, 4212, 4224,
    4214, 4232, 4322, 4324, 4412, 4422, 4414, 4424, 4432, 4434, 4444, 5112, 5222,
    5114, 5224, 5132, 5312, 5314, 5332, 5334, 5242, 5422, 5424, 5442, 5444, 5512,
    5514, 5532, 5534, 5554, 9221132, 9331122]


#**************************************************************************************************************************

# Depth-first search of particle decay paths
# Based on this stackoverflow example:
#https://stackoverflow.com/questions/59132538/counting-the-length-of-each-branch-in-a-binary-tree-and-print-out-the-nodes-trav
def decaysToSelf(particle) :
    notSelfDecay = True
    for child in particle.end_vertex.particles_out:
        if ( abs(child.pid) == abs(particle.pid) and child.id!=particle.id and child.id < 100000) :
            notSelfDecay = False
            break
    return not notSelfDecay


def findBSMParticles(truthparticles, PDGID=None, decays=False) :
    #print("Start")
    BSM_particles = []

    for iparticle,particle in enumerate(truthparticles):
        # Handed it a PDG ID?
        if PDGID :
            if model == higgs:
                if abs(particle.pid) != PDGID:
                    continue
            elif model == staus:
                if abs(particle.pid) not in PDGID:
                    continue

        # Otherwise, interested in SUSY particles only
        elif abs(particle.pid) < 999999:
            continue
        #Find stable particles or particle not decaying into itself
        if particle.end_vertex :
            if not decaysToSelf(particle) :
                BSM_particles.append(particle)
        if not particle.end_vertex :
            BSM_particles.append(particle)

    if len(BSM_particles) != 2:
        print(len(BSM_particles))
        print("Oops - there aren't 2 BSM particles!!! Evacute Earth")

    return BSM_particles


def dfs_paths(stack, particle, stable_particles = []):

    if particle == None:
        return

    # append this particle ID to the path array
    stack.append(particle.id)

    # If this particle is the end of the chain, save it
    if(not particle.end_vertex):

        # Check status
        if particle.status != 1 :
            print("Uh oh! Stable particle has status",particle.status())
            exit(1)

        # Append
        stable_particles.append(particle)

    # Otherwise try each particle from decay
    else :
        for child in particle.end_vertex.particles_out :
            dfs_paths(stack, child, stable_particles)

    # Magic
    stack.pop()


# Only works if you decayed the parent in the generation
# step, or you're running this on a post-simulation xAOD
def findBSMDecayProducts(particle,charge=False,charge_eta=False) :

    stable_descendents = []
    dfs_paths([],particle,stable_descendents)
    # If we want charged and eta ok only, subdivide
    if charge_eta :
        children = [i for i in stable_descendents if ((abs(i.pid) in charged_list) and (abs(i.momentum.eta()) <= 2.5))]
        return children
    elif charge :
        children = [i for i in stable_descendents if (abs(i.pid) in charged_list) ]
        return children
    else :
        return stable_descendents

def deltaPhi( p1, p2):
    '''Computes delta phi, handling periodic limit conditions.'''
    res = p1 - p2
    while res > math.pi:
        res -= 2*math.pi
    while res < -math.pi:
        res += 2*math.pi
    return res

#**************************************************************************************************************************

#File Level Start ===================================================================================================


zero = numpy.array([0., 0., 0.])
for m,l in file_lists:
    infile = file_lists[m,l][0]
    print(m,l,infile)

    # distributions...
    track_pt  = [] # track pt  
    track_d0  = [] # transverse impact parameter 
    track_phi = [] # 
    track_eta = []
    vtx_lxy  = [] # llp decay distance in x,y
    vtx_r    = [] # llp decay distance in r(x,y,z)
    vtx_z    = [] # llp decay distance in z
    ntracks = [] # Number of trackable particles in an event
    ntracks_d0  = [] # Number of displaced trackable particles in an event
    ntracks_acc = [] # Number of trackable particles in acceptance in an event

    output = {}

    with hep.open(infile) as f:

    #Event Level Start ==============================================================================================

        while True :
            evt = f.read()
            if not evt:
                break
            if doTest and evt.event_number > 10:
                break
            if maxevents!=-1 and evt.event_number > maxevents : break
            if evt.event_number % 1000 == 0:
                now = datetime.now()
                current_time = now.strftime("%H:%M:%S")
                print("Current time is:", current_time, " On mass:", m, "Lifetime:", l, " Event:", evt.event_number)


            #finds all the BSM pdgid 35 particles that decay into something else
            if model == higgs:
                BSM_particles = findBSMParticles(evt.particles, PDGID = 35)
            elif model == staus:
                BSM_particles = findBSMParticles(evt.particles, PDGID = [1000015, 2000015])


        #Particle Level Start =========================================================================================

            ntrk=0
            ntrk_d0=0
            ntrk_acc=0
            for bsm_part in BSM_particles:


                if doTest : 
                    print("")
                    print("")
                    print(bsm_part)

                # decay vertex 
                decayvtx = bsm_part.end_vertex
                fourvec = decayvtx.position 
                vtx_lxy .append( (fourvec.x**2 + fourvec.y**2)**0.5 ) 
                vtx_r   .append( (fourvec.x**2 + fourvec.y**2 + fourvec.z**2)**0.5 )
                vtx_z   .append( fourvec.z ) 

                decay_prods = findBSMDecayProducts(bsm_part,charge=True)

                for part in decay_prods:

                    if doTest : print(part)

                    # Vertex info
                    prod_vtx   = part.production_vertex
                    prod_vec   = prod_vtx.position
                    prod_point = numpy.array( [prod_vec.x, prod_vec.y, prod_vec.z] )
                    prod_rxy   = (prod_vec.x**2 + prod_vec.y**2)**0.5 

                    # Particle info
                    mom = part.momentum
                    pt  = mom.perp()/1000.
                    eta = mom.eta()
                    phi = mom.phi()

                    if (pt < 0.5) : continue

                    fail_track_length = False 
                    if part.end_vertex:
                        decay_vtx    = part.end_vertex
                        decay_vec    = decay_vtx.position
                        decay_point  = numpy.array([decay_vec.x, decay_vec.y, decay_vec.z])
                        track_vec    = decay_point - prod_point
                        track_length = math.sqrt( sum(x**2 for x in track_vec ))
                        if track_length < 200: fail_track_length = True 
                    if fail_track_length: continue 

                    # Fill arrays if reconstructable
                    track_pt .append(pt)
                    track_eta.append(eta)
                    track_phi.append(phi)
                
                    # get an approximate true d0 = Rxy*sin(dPhi), 
                    # where dPhi is between the PV-to-DV vector 
                    # and the track from the DV
                    dPhi = deltaPhi( prod_vec.phi(), phi )
                    d0   = prod_rxy*math.sin(abs(dPhi));
                    if doTest: 
                        print( 'pt', pt ) 
                        print( "phi1, phi2, dPhi:", prod_vec.phi(), phi, dPhi)
                        print( "rxy, d0:",prod_rxy, d0)
                    track_d0.append(d0)

                    # Jesse's method... p sure something's wrong 
                    #mom_mag = math.sqrt((mom.x ** 2) + (mom.y ** 2) + (mom.z ** 2))
                    #mom_hat = numpy.array([mom.x / mom_mag, mom.y / mom_mag, mom.z / mom_mag])
                    #line_point = mom_hat * 10 + prod_point
                    #d = numpy.cross(prod_point - line_point, zero - line_point) / numpy.linalg.norm(prod_point - line_point)
                    #d02 = numpy.sqrt(numpy.square(d[0]) + numpy.square(d[1]))

                    #https://jiafulow.github.io/blog/2019/11/04/track-impact-parameter/
                    # assuming no mag field...
                    # 𝑑0=𝑥𝑣sin𝜙−𝑦𝑣cos𝜙
                    #d02 = prod_vec.x * math.sin(phi) - prod_vec.y * math.cos(phi)
                    #if doTest: print( 'd02:,', d02)

                    # fill ntrack info
                    ntrk+=1
                    if abs(d0) > 1.0 : ntrk_d0+=1
                    if abs(d0) > 1.0 and prod_rxy < 300 and abs(eta)<2.5 : ntrk_acc+=1

            ntracks.append(ntrk)
            ntracks_d0 .append(ntrk_d0)
            ntracks_acc.append(ntrk_acc)
            # per event


        # while true 

    # loop over files
    output = { "track_pt":track_pt,
                    "track_d0" : track_d0,
                    "track_phi": track_phi,
                    "track_eta": track_eta,
                    "vtx_lxy" : vtx_lxy,
                    "vtx_r" : vtx_r,
                    "vtx_z" : vtx_z, 
                    "ntracks" : ntracks,
                    "ntracks_d0" : ntracks_d0,
                    "ntracks_acc" : ntracks_acc
        }


    if doTest : 
        #print( "track_pt" , track_pt  ) # track pt  
        #print( "track_eta", track_eta )
        #print( "track_phi", track_phi ) # 
        #print( "track_d0" , track_d0  ) # transverse impact parameter 
        #print( "vtx_lxy"  , vtx_lxy ) # llp decay distance in x,y
        #print( "vtx_r"    , vtx_r   ) # llp decay distance in r(x,y,z)
        #print( "vtx_z"    , vtx_z   ) # llp decay distance in r(x,y,z)
        #print( "ntracks"  , ntracks ) # Number of trackable particles in an event
        break


    save_name = 'output/%s_%d_%s_distributions.json'%(model,m,l)
    with open(save_name, 'w') as fp:
            json.dump(output, fp)



