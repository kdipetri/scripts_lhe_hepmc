import json
import time
import numpy as np
import copy


# Step 1
def simulatePileup(pileup=1,sample='qcd',opt='sumpt2'):

    # Get min-bias/qcd events
    f = open('output/'+sample+'_forpileup.json') 
    data = json.load(f)

    sig_event_array   = data["events"]
    sig_track_array   = data["event_tracks"] # each row is one event's tracks
    weight_array      = [ event["weight"] for event in sig_event_array ] # event weight

    f.close()

    # Get min-bias/qcd events
    f = open('output/qcd_2TeV_forpileup.json') 
    qcd_data = json.load(f)

    qcd_event_array       = qcd_data["events"]
    qcd_track_array       = qcd_data["event_tracks"] # each row is one event's tracks
    qcd_weight_array      = [ event["weight"] for event in qcd_event_array ] # event weight

    f.close()
    
    if pileup<2: # don't need to do anything
        outdata = {
            "weights" : weight_array,
            "event_tracks" : sig_event_array,
            "events" : sig_event_array,
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
        n_sig_events = len(sig_track_array) #n events to play with
        n_qcd_events = len(qcd_track_array) # nqcd events

        # add up tracks from pile-up events, to the sample of interest 
        np_sig_events = np.array(sig_event_array,dtype=object) # convert sample to numpy array  
        np_sig_tracks = np.array(sig_track_array,dtype=object) # convert sample to numpy array  
        np_qcd_events = np.array(qcd_event_array,dtype=object) # convert sample to numpy array  
        np_qcd_tracks = np.array(qcd_track_array,dtype=object) # convert sample to numpy array  

        pileup_event_array  = copy.deepcopy(np_sig_events) # will add tracks here 
        pileup_track_array  = copy.deepcopy(np_sig_tracks) # will add tracks here 

        #print("signal arrays shape : ", event_array.shape, event_track_array.shape)
        #print("pileup arrays shape : ",pileup_event_array.shape, pileup_track_array.shape)

        nPVwrong=0
        for evt in range(0,n_sig_events):

            # Randomly choose N qcd events to overlay 
            pu_index = np.random.choice(n_qcd_events,size=pileup,p=prob_array) # get qcd event indices, in array matching sample size 

            # can check for PV z consistency here for counting prompt vertices
            pu_events = np_qcd_events[pu_index]
            pu_tracks = np_qcd_tracks[pu_index] # use it to make an array of new events
            
            # pick the primary vertex
            sel      = "{}_pass_prompt_pt1.0".format(opt)  
            sumpt_pv = np_sig_events[evt][sel]
            z0_pv    = np_sig_events[evt]['z0']
            qcd_pv = -1
            
            for pu in range(0,pileup-1): 
                sumpt_pu = pu_events[pu][sel]
                if sumpt_pu > sumpt_pv: 
                    sumpt_pv = sumpt_pu 
                    z0_pv = pu_events[pu]['z0']
                    qcd_pv = pu
            
            if qcd_pv > -1 : nPVwrong +=1
            
            # treat the signal event
            pileup_event_array[evt]['z0'] = z0_pv

            dz = abs(sig_event_array[evt]['z0'] - z0_pv)
            for sel in pileup_event_array[evt].keys():
                if 'z0' in sel : continue 
                if 'weight' in sel : continue 
                if dz > 1 and 'prompt' in sel : 
                    pileup_event_array[evt][sel] -= np_sig_events[evt][sel]
                
            for trk in pileup_track_array[evt]: 
                dz = abs(trk['prod_z'] - z0_pv)
                d0 = trk['d0'] 
                if d0 > 1. and "sumpt2" in opt: continue # keep 
                if d0 < 1. and dz < 1 : continue # keep
                pileup_track_array[evt].remove(trk)
        

            # treat the pu events
            for pu in range(0,pileup-1): 
                
                dz = abs(pu_events[pu]['z0'] - z0_pv)

                for sel in pu_events[pu].keys():
                    if 'weight' in sel : continue 
                    if 'z0' in sel : continue
                    if dz > 1.0 and "prompt" in sel : continue
                    pileup_event_array[evt][sel] += pu_events[pu][sel]   

                for trk in pu_tracks[pu]:
                    dz = abs(trk['prod_z'] - z0_pv)
                    d0 = trk['d0'] 
                    if d0 > 1.0 and "sumpt2" not in opt : continue # remove track 
                    if d0 < 1. and dz > 1.0 : continue # remove if prompt and not from PV 
                    pileup_track_array[evt].append(trk) # else add 

    
        sel = "nTrack_pass_prompt_pt1.0"
        for i in range(10):
            print(np_sig_events[i][sel], np_qcd_events[i][sel], pileup_event_array[i][sel])

        for i in range(10): # print out 10 event's info
            print(len(np_sig_tracks[i]), len(np_qcd_tracks[i]), len(pileup_track_array[i])) 
    

        print("N Wrong PV ", nPVwrong)

        outdata = {
            "weights" : weight_array,
            "event_tracks" : pileup_track_array.tolist(),
            "events" : pileup_event_array.tolist()
        }
        
        fname = 'output/{}_pileup{}.json'.format(sample,pileup)
        if opt == "nTrack" : fname = 'output/{}_pileup{}_nTrack.json'.format(sample,pileup)
        if opt == "sumpt"  : fname = 'output/{}_pileup{}_nTrack.json'.format(sample,pileup)

        with open(fname, 'w') as fp:
            json.dump(outdata, fp)

        print("data saved to file")

        return 


# Run over...

samples = []
samples.append("qcd_2TeV")
samples.append("stau_300_0p1ns")
samples.append("stau_300_1ns")
samples.append("stau_300_stable")
samples.append("higgsportal_125_55_1ns")
samples.append("higgsportal_125_40_0p1ns")

samples_suep = []
samples_suep.append("qcd_2TeV")
samples_suep.append("suep_mMed-200_mDark-1.0_temp-1.0")
samples_suep.append("suep_mMed-600_mDark-1.0_temp-1.0")


pileup = 200 

for sample in samples: 
    simulatePileup(1,sample)
    simulatePileup(pileup,sample)
for sample in samples_suep:
    simulatePileup(pileup,sample,"nTrack")

