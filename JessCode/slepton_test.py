#!/usr/bin/env python

import pyhepmc_ng as hep
import numpy
import math
import matplotlib.pyplot as plt
from datetime import datetime


infile = "/eos/user/k/kpachal/TrackTrigStudies/HepMCFiles/sleptons/slepton_300_0_1ns.hepmc"

slept_ids = [1000011, 1000012, 1000013, 1000014, 1000015, 1000016, 2000011, 2000012, 2000013, 2000014, 
            2000015, 2000016]

decay_pt = [] 
dtr_ids = []
tot_dist = []
trans_dist = []
decay_points = []
hats = []
line_points = []
dists = []
zero = numpy.array([0, 0, 0])

doTest = True

with hep.open(infile) as f:

  while True:
    evt = f.read()
    if not evt: 
      break
    if doTest and evt.event_number > 50:  
      break

    #print("\n Event ", evt.event_number, "\n")

    prods = []
    temp_decay_points = []
    
    for particle in evt.particles:
      is_slept = False
      for i in range(len(slept_ids)):
        if abs(particle.pid) == slept_ids[i]:
          is_slept = True

      if is_slept == True and particle.status != 1:
        decayvtx = particle.end_vertex
        #print("\n", particle.pid, decayvtx)

        if (decayvtx):
          status = decayvtx.status
          fourvec = decayvtx.position
          # if evt.event_number <= 10:
          #   print(fourvec)
          decay_x = fourvec.x
          decay_y = fourvec.y
          decay_z = fourvec.z
          decay_t = fourvec.t
          point = numpy.array([decay_x, decay_y, decay_z])
          tot_dist_temp = math.sqrt((decay_x ** 2) + (decay_y ** 2) + (decay_z ** 2))

          dup = False
          for i in range(len(prods)):
            if prods[i].id == particle.id:
              dup = True  

          if (tot_dist_temp) != 0:
            tot_dist.append(tot_dist_temp)
            trans_dist.append(math.sqrt((decay_x ** 2) + (decay_y ** 2)))
            products = decayvtx.particles_out

            for i in range(len(products)):
              prods.append(products[i])
              temp_decay_points.append(point)
      
      daughter = False
      for i in range(len(prods)):
        if particle.id == prods[i].id:
          daughter = True
          decay_points.append(temp_decay_points[i])
      
      if daughter == True:
        dtr_mom_x = particle.momentum.x
        dtr_mom_y = particle.momentum.y
        dtr_mom_z = particle.momentum.z
        dtr_mom_mag = math.sqrt((dtr_mom_x ** 2) + (dtr_mom_y ** 2) + (dtr_mom_z ** 2))
        dtr_mom_hat = numpy.array([dtr_mom_x / dtr_mom_mag, dtr_mom_y / dtr_mom_mag, dtr_mom_z / dtr_mom_mag])
        hats.append(dtr_mom_hat)
        decay_pt.append((math.sqrt((dtr_mom_x ** 2) + (dtr_mom_y ** 2))) / 1000)
        dtr_ids.append(abs(particle.pid))


ids = []
counts = []
for i in range(len(dtr_ids)):
  prior = False
  for j in range(len(ids)):
    if dtr_ids[i] == ids[j]:
      prior = True
      counts[j] += 1
  if prior == False:    
    ids.append(dtr_ids[i])
    counts.append(1)

id_dict = {}
for i in range(len(ids)):
  id_dict[str(ids[i])] = counts[i]
      
for i in range(len(hats)):
  line_points.append(hats[i] * 10 + decay_points[i])

for i in range(len(line_points)):
  d = (numpy.cross(decay_points[i]-line_points[i],zero-line_points[i]) / 
       numpy.linalg.norm(decay_points[i]-line_points[i]))
  #print(d)
  d_mag = numpy.sqrt(numpy.square(d[0]) + numpy.square(d[1]))
  dists.append(d_mag)


fig, axs = plt.subplots()
axs.set_title("Decay Product IDs")
axs.set_xlabel("PID (absolute)")
axs.bar(id_dict.keys(), id_dict.values())
fig.savefig('sleptons_decay_ids.svg', filetype = 'svg')

fig, axs = plt.subplots()
axs.set_title("Decay Vertex Total Distance")
axs.set_xlabel("Distance (mm)")
axs.hist(tot_dist)
fig.savefig('sleptons_tot_dist.svg', filetype = '.svg')

fig, axs = plt.subplots()
axs.set_title("Decay Vertex Transverse Distance")
axs.set_xlabel("Distance (mm)")
axs.hist(trans_dist)
fig.savefig('sleptons_trans_dist.svg', filetype = '.svg')

fig, axs = plt.subplots()
axs.set_title("Decay Product Transverse Momentum")
axs.set_xlabel("Transverse Momentum (GeV)")
axs.hist(decay_pt)
fig.savefig('sleptons_decay_pt.svg', filetype = '.svg')

fig, axs = plt.subplots()
axs.set_title("Decay Product d0")
axs.set_xlabel("Distance (mm)")
axs.hist(dists, bins = 20)
fig.savefig('sleptons_d0.svg', filetype = '.svg')











