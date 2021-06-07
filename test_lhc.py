from lhereader import LHEReader
import ROOT
import statistics

#reader = LHEReader('/eos/user/k/kpachal/TrackTrigStudies/LHEFiles/sleptons/slepton_300_0_1ns.lhe')
reader = LHEReader('/afs/cern.ch/work/k/kpachal/TrackTrigStudy/Generation/run_sleptons/slepton_300_0_1ns/events.lhe')
#reader = LHEReader('/eos/user/k/kpachal/TrackTrigStudies/RunDirectories/run_higgsportal/higgsportal_125_15_1ns/events.lhe')

vtau_vals = []

for iev, event in enumerate(reader):

  for particle in event.particles :
    if particle.vtau > 0 :
      vtau_vals.append(particle.vtau)

  if iev < 11 : 
    print("Event",iev)
    for particle in event.particles :
      print(particle)


print ("Compatible with", int(float(len(vtau_vals))/2.), "events")
print ("Average vtau is", statistics.mean(vtau_vals))

