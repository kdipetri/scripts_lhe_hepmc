import json
import time
import numpy as np
from pyjet import cluster
from pyjet.testdata import get_event

#https://www.quora.com/What-is-matplotlib-use-and-why-do-we-use-them
import matplotlib 
matplotlib.use('pdf') # for speed? 
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
from util.plot_helper import *

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
displaced_configs.append("pt1.5;d050")
displaced_configs.append("pt2.0;d050")
displaced_configs.append("pt5.0;d050")
displaced_configs.append("pt10.0;d050")
displaced_configs.append("pt1.0;d010")
displaced_configs.append("pt1.0;d020")
displaced_configs.append("pt1.0;d0100")

# Step 1
def simulatePileup(pileup=1,sample='qcd'):

    # Get min-bias/qcd events
    f = open('output/'+sample+'_forpileup.json') 
    data = json.load(f)

    event_array         = data["events"]
    event_track_array   = data["event_tracks"] # each row is one event's tracks
    weight_array        = [ event["weight"] for event in event_array ] # event weight

    f.close()

    # Get min-bias/qcd events
    f = open('output/qcd_forpileup.json') 
    qcd_data = json.load(f)

    qcd_event_array       = qcd_data["events"]
    qcd_event_track_array = qcd_data["event_tracks"] # each row is one event's tracks
    qcd_weight_array      = [ event["weight"] for event in qcd_event_array ] # event weight

    f.close()
    
    if pileup<2: # don't need to do anything
        outdata = {
            "weights" : weight_array,
            "event_tracks" : event_track_array,
            "events" : event_array,
        }
        
        with open('output/{}_pileup{}.json'.format(sample,pileup), 'w') as fp:
            json.dump(data, fp)
        return 
    else : 
        # convert qcd weights to rough probabilities
        sumweights = sum(qcd_weight_array)
        probs = [ x/sumweights for x in qcd_weight_array ]
        prob_array = np.array(probs)

        # testing weights
        #print("scaled weights")
        #for i in range(0,10):
        #    print(weight_array[i], prob_array[i])

        # get dimensions
        nevents =  len(event_track_array) #n events to play with
        size_qcd = len(qcd_event_track_array) # nqcd events

        # add up tracks from pile-up events, to the sample of interest 
        event_track_array      = np.array(event_track_array,dtype=object) # convert sample to numpy array  
        qcd_event_track_array  = np.array(qcd_event_track_array,dtype=object) # convert bkg to numpy array  
        pileup_track_array  = event_track_array # will add tracks here 

        # add up ntracks passing various configs 
        event_array      = np.array(event_array,dtype=object) # convert sample to numpy array  
        qcd_event_array  = np.array(qcd_event_array,dtype=object) # convert bkg to numpy array  
        pileup_event_array  = event_array # will add tracks here 

        #print("signal arrays shape : ", event_array.shape, event_track_array.shape)
        #print("pileup arrays shape : ",pileup_event_array.shape, pileup_track_array.shape)
        for pu in range(0,pileup-1): 
            # sample pileup event indices
            event_index = np.random.choice(size_qcd,size=nevents,p=prob_array) # get qcd event indices, in array matching sample size 


            # can check for PV z consistency here for counting prompt vertices
            new_events       = qcd_event_array[event_index]
            new_event_tracks = qcd_event_track_array[event_index] # use it to make an array of new events
            for i in range(nevents):

                pvdist = abs(pileup_event_array[i]['z0'] - new_events[i]['z0'])  

                for sel in new_events[i].keys():
                    #print(sel)
                    if pvdist > 1.0 and "prompt" in sel : continue
                    if 'z0' in sel : continue
                    pileup_event_array[i][sel] += new_events[i][sel]   

                for trk in new_event_tracks[i]:
                    
                    if trk["d0"] > 1.0: continue # keep track 
                    elif pvdist < 1.0 : continue # keep track
                    else : new_event_tracks[i].remove(trk) # remove track

            pileup_track_array = [ i+j for i,j in zip(pileup_track_array,new_event_tracks) ] 
    
        print("ntracks saved/event, Signal 0 PU, QCD 0 PU, Total {} PU".format(pileup))
        for i in range(10): # print out 10 event's info
            print(len(event_track_array[i]), len(list(new_event_tracks[i])), len(pileup_track_array[i])) 
    
        #for i in range(10):
        #    print( pileup_event_array[i] )


        outdata = {
            "weights" : weight_array,
            "event_tracks" : pileup_track_array,
            "events" : pileup_event_array.tolist()
        }
        
        with open('output/{}_pileup{}.json'.format(sample,pileup), 'w') as fp:
            json.dump(outdata, fp)

        print("data saved to file")
        return 


# Run over...

samples = []
#samples.append("qcd")
#samples.append("stau_300_0p1ns")
#samples.append("stau_300_1ns")
samples.append("stau_300_stable")
#samples.append("higgsportal_125_55_1ns")
#samples.append("higgsportal_125_40_0p1ns")
#samples.append("suep_mMed-200_mDark-1.0_temp-1.0")
#samples.append("suep_mMed-600_mDark-1.0_temp-1.0")
pileups = [2,5,50,100,200]
#pileups = [2,5,50,100]
pileups = [200]

for sample in samples: 
    for pileup in pileups:  
        simulatePileup(pileup,sample)

