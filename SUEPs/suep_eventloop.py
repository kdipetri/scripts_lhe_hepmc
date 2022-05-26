#!/usr/bin/env python

import json
import pyhepmc_ng as hep
import numpy
import math
from datetime import datetime

file_list = ["/eos/user/k/kdipetri/Snowmass_SUEPs/mMed-125_mDark-1.0_temp-1.0.hepmc",
            "/eos/user/k/kdipetri/Snowmass_SUEPs/mMed-200_mDark-1.0_temp-1.0.hepmc",
            "/eos/user/k/kdipetri/Snowmass_SUEPs/mMed-400_mDark-1.0_temp-1.0.hepmc",
            "/eos/user/k/kdipetri/Snowmass_SUEPs/mMed-600_mDark-1.0_temp-1.0.hepmc",
            "/eos/user/k/kdipetri/Snowmass_SUEPs/mMed-800_mDark-1.0_temp-1.0.hepmc",
            "/eos/user/k/kdipetri/Snowmass_SUEPs/mMed-1000_mDark-1.0_temp-1.0.hepmc"]

charged_list = [1, 2, 3, 4, 5, 6, 7, 8, 11, 13, 15, 17, 24, 34, 37, 38, 1000011, 1000013,
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



efficiencies = []
errors = []
ht_05_tot = [] # ht with pT > 0.5 threshold
ht_1_tot  = [] # ht with pT > 1 threshold
ht_2_tot  = [] # ht with pT > 2 threshold
nTrack_05_tot = [] # nTracks with pT > 0.5 threshold
nTrack_1_tot = [] # nTracks with pT > 1.0 threshold
nTrack_2_tot = [] # nTracks with pT > 2.0 threshold
pt_tot = [] 

for m in range(len(file_list)):
  infile = file_list[m]
  
  pass_05_100 = 0
  pass_05_150 = 0
  pass_05_200 = 0
  pass_1_100 = 0
  pass_1_150 = 0 
  pass_1_200 = 0
  pass_2_100 = 0
  pass_2_150 = 0
  pass_2_200 = 0
  event_count = 0
  ht_05 = []
  ht_1 = []
  ht_2 = []
  pt = []
  nTrack_05 = []
  nTrack_1  = []
  nTrack_2  = []
    

  #Change this depending on test run or full run!
  doTest = False 

  with hep.open(infile) as f:
    
    while True:
      evt = f.read()
      if not evt: 
        break
      if doTest and evt.event_number > 1000:  
        break

      cutoff1_count = 0
      cutoff2_count = 0
      cutoff3_count = 0
      event_count += 1
      ht_05_event = 0
      ht_1_event = 0
      ht_2_event = 0


      if evt.event_number % 1000 == 0:
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        print("Current time is:", current_time, " On file:", m+1, " Event:", evt.event_number)

      for particle in evt.particles:
        check = False
        for i in range(len(charged_list)):
          if abs(particle.pid) == charged_list[i]:
            check = True

        eta_check = False
        if abs(particle.momentum.eta()) < 2.5:
          eta_check = True

        if particle.status == 1 and check == True and eta_check == True:
          p_T = numpy.sqrt(numpy.square(particle.momentum.px) + numpy.square(particle.momentum.py))
          tot_mom = numpy.sqrt(numpy.square(particle.momentum.px) + numpy.square(particle.momentum.py) + numpy.square(particle.momentum.pz))
          if p_T > 0.5:
            cutoff1_count += 1
            ht_05_event += tot_mom
          if p_T > 1:
            cutoff2_count += 1
            ht_1_event += tot_mom
          if p_T > 2:
            cutoff3_count += 1
            ht_2_event += tot_mom

          pt.append(p_T) # fill per track

      ht_05.append(ht_05_event) # fill per event
      ht_1.append(ht_1_event)
      ht_2.append(ht_2_event)

      nTrack_05.append(cutoff1_count)
      nTrack_1.append(cutoff2_count)
      nTrack_2.append(cutoff3_count)


      if cutoff1_count > 100:
          pass_05_100 += 1
          if cutoff1_count > 150:
              pass_05_150 += 1
              if cutoff1_count > 200:
                  pass_05_200 += 1    

      if cutoff2_count > 100:
          pass_1_100 += 1
          if cutoff2_count > 150:
              pass_1_150 += 1
              if cutoff2_count > 200:
                  pass_1_200 += 1  

      if cutoff3_count > 100:
          pass_2_100 += 1
          if cutoff3_count > 150:
              pass_2_150 += 1
              if cutoff3_count > 200:
                  pass_2_200 += 1



  efficiencies.append([pass_05_100 / event_count, pass_05_150 / event_count, pass_05_200 /event_count, 
              pass_1_100 / event_count, pass_1_150 / event_count, pass_1_200 / event_count, 
              pass_2_100 /event_count, pass_2_150 /event_count, pass_2_200 / event_count])

  errors.append([math.sqrt((pass_05_100 / event_count)*(1- (pass_05_100 / event_count)) / event_count),
                 math.sqrt((pass_05_150 / event_count)*(1- (pass_05_150 / event_count)) / event_count),
                 math.sqrt((pass_05_200 / event_count)*(1- (pass_05_200 / event_count)) / event_count),
                 math.sqrt((pass_1_100 / event_count)*(1- (pass_1_100 / event_count)) / event_count),
                 math.sqrt((pass_1_150 / event_count)*(1- (pass_1_150 / event_count)) / event_count),
                 math.sqrt((pass_1_200 / event_count)*(1- (pass_1_200 / event_count)) / event_count),
                 math.sqrt((pass_2_100 / event_count)*(1- (pass_2_100 / event_count)) / event_count),
                 math.sqrt((pass_2_150 / event_count)*(1- (pass_2_150 / event_count)) / event_count),
                 math.sqrt((pass_2_200 / event_count)*(1- (pass_2_200 / event_count)) / event_count),])

  ht_05_tot.append(ht_05)
  ht_1_tot.append(ht_1)
  ht_2_tot.append(ht_2)

  nTrack_05_tot.append(nTrack_05)
  nTrack_1_tot.append(nTrack_1)
  nTrack_2_tot.append(nTrack_2)

  pt_tot.append(pt)


data = {
    "trackPt" : [
        {"mass": "125" , "pt": pt_tot[0] },
        {"mass": "200" , "pt": pt_tot[1] },
        {"mass": "400" , "pt": pt_tot[2] },
        {"mass": "600" , "pt": pt_tot[3] },
        {"mass": "800" , "pt": pt_tot[4] },
        {"mass": "1000", "pt": pt_tot[5] }],
    "nTrack" : [
        {"mass": "125" , "nTrack_05": nTrack_05_tot[0], "nTrack_1": nTrack_1_tot[0], "nTrack_2": nTrack_2_tot[0]},
        {"mass": "200" , "nTrack_05": nTrack_05_tot[1], "nTrack_1": nTrack_1_tot[1], "nTrack_2": nTrack_2_tot[1]},
        {"mass": "400" , "nTrack_05": nTrack_05_tot[2], "nTrack_1": nTrack_1_tot[2], "nTrack_2": nTrack_2_tot[2]},
        {"mass": "600" , "nTrack_05": nTrack_05_tot[3], "nTrack_1": nTrack_1_tot[3], "nTrack_2": nTrack_2_tot[3]},
        {"mass": "800" , "nTrack_05": nTrack_05_tot[4], "nTrack_1": nTrack_1_tot[4], "nTrack_2": nTrack_2_tot[4]},
        {"mass": "1000", "nTrack_05": nTrack_05_tot[5], "nTrack_1": nTrack_1_tot[5], "nTrack_2": nTrack_2_tot[5]}],
    "ht": [
        {"mass": "125" , "ht_05": ht_05_tot[0], "ht_1": ht_1_tot[0], "ht_2": ht_2_tot[0]},
        {"mass": "200" , "ht_05": ht_05_tot[1], "ht_1": ht_1_tot[1], "ht_2": ht_2_tot[1]},
        {"mass": "400" , "ht_05": ht_05_tot[2], "ht_1": ht_1_tot[2], "ht_2": ht_2_tot[2]},
        {"mass": "600" , "ht_05": ht_05_tot[3], "ht_1": ht_1_tot[3], "ht_2": ht_2_tot[3]},
        {"mass": "800" , "ht_05": ht_05_tot[4], "ht_1": ht_1_tot[4], "ht_2": ht_2_tot[4]},
        {"mass": "1000", "ht_05": ht_05_tot[5], "ht_1": ht_1_tot[5], "ht_2": ht_2_tot[5]}],
    "data": [
        {"cut": "125_pt05_n100", "efficiency": efficiencies[0][0], "error" : errors[0][0]},
        {"cut": "125_pt05_n150", "efficiency": efficiencies[0][1], "error" : errors[0][1]},
        {"cut": "125_pt05_n200", "efficiency": efficiencies[0][2], "error" : errors[0][2]},
        {"cut": "125_pt1_n100" , "efficiency": efficiencies[0][3], "error" : errors[0][3]},
        {"cut": "125_pt1_n150" , "efficiency": efficiencies[0][4], "error" : errors[0][4]},
        {"cut": "125_pt1_n200" , "efficiency": efficiencies[0][5], "error" : errors[0][5]},
        {"cut": "125_pt2_n100" , "efficiency": efficiencies[0][6], "error" : errors[0][6]},
        {"cut": "125_pt2_n150" , "efficiency": efficiencies[0][7], "error" : errors[0][7]},
        {"cut": "125_pt2_n200" , "efficiency": efficiencies[0][8], "error" : errors[0][8]},
        {"cut": "200_pt05_n100", "efficiency": efficiencies[1][0], "error" : errors[1][0]},
        {"cut": "200_pt05_n150", "efficiency": efficiencies[1][1], "error" : errors[1][1]},
        {"cut": "200_pt05_n200", "efficiency": efficiencies[1][2], "error" : errors[1][2]},
        {"cut": "200_pt1_n100" , "efficiency": efficiencies[1][3], "error" : errors[1][3]},
        {"cut": "200_pt1_n150" , "efficiency": efficiencies[1][4], "error" : errors[1][4]},
        {"cut": "200_pt1_n200" , "efficiency": efficiencies[1][5], "error" : errors[1][5]},
        {"cut": "200_pt2_n100" , "efficiency": efficiencies[1][6], "error" : errors[1][6]},
        {"cut": "200_pt2_n150" , "efficiency": efficiencies[1][7], "error" : errors[1][7]},
        {"cut": "200_pt2_n200" , "efficiency": efficiencies[1][8], "error" : errors[1][8]},
        {"cut": "400_pt05_n100", "efficiency": efficiencies[2][0], "error" : errors[2][0]},
        {"cut": "400_pt05_n150", "efficiency": efficiencies[2][1], "error" : errors[2][1]},
        {"cut": "400_pt05_n200", "efficiency": efficiencies[2][2], "error" : errors[2][2]},
        {"cut": "400_pt1_n100" , "efficiency": efficiencies[2][3], "error" : errors[2][3]},
        {"cut": "400_pt1_n150" , "efficiency": efficiencies[2][4], "error" : errors[2][4]},
        {"cut": "400_pt1_n200" , "efficiency": efficiencies[2][5], "error" : errors[2][5]},
        {"cut": "400_pt2_n100" , "efficiency": efficiencies[2][6], "error" : errors[2][6]},
        {"cut": "400_pt2_n150" , "efficiency": efficiencies[2][7], "error" : errors[2][7]},
        {"cut": "400_pt2_n200" , "efficiency": efficiencies[2][8], "error" : errors[2][8]},
        {"cut": "600_pt05_n100", "efficiency": efficiencies[3][0], "error" : errors[3][0]},
        {"cut": "600_pt05_n150", "efficiency": efficiencies[3][1], "error" : errors[3][1]},
        {"cut": "600_pt05_n200", "efficiency": efficiencies[3][2], "error" : errors[3][2]},
        {"cut": "600_pt1_n100" , "efficiency": efficiencies[3][3], "error" : errors[3][3]},
        {"cut": "600_pt1_n150" , "efficiency": efficiencies[3][4], "error" : errors[3][4]},
        {"cut": "600_pt1_n200" , "efficiency": efficiencies[3][5], "error" : errors[3][5]},
        {"cut": "600_pt2_n100" , "efficiency": efficiencies[3][6], "error" : errors[3][6]},
        {"cut": "600_pt2_n150" , "efficiency": efficiencies[3][7], "error" : errors[3][7]},
        {"cut": "600_pt2_n200" , "efficiency": efficiencies[3][8], "error" : errors[3][8]},
        {"cut": "800_pt05_n100", "efficiency": efficiencies[4][0], "error" : errors[4][0]},
        {"cut": "800_pt05_n150", "efficiency": efficiencies[4][1], "error" : errors[4][1]},
        {"cut": "800_pt05_n200", "efficiency": efficiencies[4][2], "error" : errors[4][2]},
        {"cut": "800_pt1_n100" , "efficiency": efficiencies[4][3], "error" : errors[4][3]},
        {"cut": "800_pt1_n150" , "efficiency": efficiencies[4][4], "error" : errors[4][4]},
        {"cut": "800_pt1_n200" , "efficiency": efficiencies[4][5], "error" : errors[4][5]},
        {"cut": "800_pt2_n100" , "efficiency": efficiencies[4][6], "error" : errors[4][6]},
        {"cut": "800_pt2_n150" , "efficiency": efficiencies[4][7], "error" : errors[4][7]},
        {"cut": "800_pt2_n200" , "efficiency": efficiencies[4][8], "error" : errors[4][8]},
        {"cut": "1000_pt05_n100", "efficiency": efficiencies[5][0], "error" : errors[5][0]},
        {"cut": "1000_pt05_n150", "efficiency": efficiencies[5][1], "error" : errors[5][1]},
        {"cut": "1000_pt05_n200", "efficiency": efficiencies[5][2], "error" : errors[5][2]},
        {"cut": "1000_pt1_n100" , "efficiency": efficiencies[5][3], "error" : errors[5][3]},
        {"cut": "1000_pt1_n150" , "efficiency": efficiencies[5][4], "error" : errors[5][4]},
        {"cut": "1000_pt1_n200" , "efficiency": efficiencies[5][5], "error" : errors[5][5]},
        {"cut": "1000_pt2_n100" , "efficiency": efficiencies[5][6], "error" : errors[5][6]},
        {"cut": "1000_pt2_n150" , "efficiency": efficiencies[5][7], "error" : errors[5][7]},
        {"cut": "1000_pt2_n200" , "efficiency": efficiencies[5][8], "error" : errors[5][8]}]}
        

with open('SUEP_effieciencies.json', 'w') as fp:
    json.dump(data, fp)
    
    


