import json
import time
import numpy as np
import ROOT
import random
from pyjet import cluster
from pyjet.testdata import get_event
import mathutils
import math
from operator import itemgetter

#https://www.quora.com/What-is-matplotlib-use-and-why-do-we-use-them
import matplotlib 
matplotlib.use('pdf') # for speed? 
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
from util.plot_helper import *

prompt_configs = []
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

doTest = False    
#doTest = True    

def passes_d0_cut(d0track, d0cut):

    # Assume tracking efficiency decreases linearly w/ d0
    rng_check = random.random() # returns a number between 0 and 1

    y_inter = 1.0 
    effslope = -1.0/d0cut
    eff = effslope*d0track + y_inter
    if rng_check < eff: return True
    else: return False

def two_track_intersection(trk1, trk2):
    #mathutils.geometry.intersect_line_line(v1, v2, v3, v4)
    # Returns a tuple with the points on each line respectively closest to the other.

    #Parameters
    #v1 (mathutils.Vector) – First point of the first line
    #v2 (mathutils.Vector) – Second point of the first line
    #v3 (mathutils.Vector) – First point of the second line
    #v4 (mathutils.Vector) – Second point of the second line

    #Return type tuple of mathutils.Vector’s
    v1 = mathutils.Vector( (trk1["prod_x"], trk1["prod_y"], trk1["prod_z"] ) )
    v2 = v1 + mathutils.Vector( ( trk1["px"],trk1["py"], trk1["pz"] ) )
    v3 = mathutils.Vector( (trk2["prod_x"], trk2["prod_y"], trk2["prod_z"] ) )
    v4 = v3 + mathutils.Vector( ( trk2["px"],trk2["py"], trk2["pz"] ) )
    
    closest_points = mathutils.geometry.intersect_line_line(v1,v2,v3,v4)

    d = 9999.
    vtx = mathutils.Vector( (9999.,9999.,9999.) )
    if not closest_points: return d,vtx 
    elif not closest_points[0].x : return d,vtx 
    else : 
        (p1,p2) = closest_points 

        d = (p1-p2).magnitude
        vtx = (p1+p2)/2.
    
    return d,vtx

    #if d < 2 : 
    #    print( "PCA1 : ",  p1 )
    #    print( "PCA2 : ",  p2 )
    #    print( "dist : ",  d  )
    #    print( "line 1 : ", v1, v2) 
    #    print( "line 2 : ", v3, v4) 

    return d,vtx

def track_DV_intersection(trk, dv):
    #mathutils.geometry.intersect_line_line(v1, v2, v3, v4)
    # Returns a tuple with the points on each line respectively closest to the other.

    #Parameters
    #v1 (mathutils.Vector) – First point of the first line
    #v2 (mathutils.Vector) – Second point of the first line
    #v3 (mathutils.Vector) – First point of the second line
    #v4 (mathutils.Vector) – Second point of the second line

    #Return type tuple of mathutils.Vector’s
    v1 = mathutils.Vector( (trk["prod_x"], trk["prod_y"], trk["prod_z"] ) )
    v2 = v1 + mathutils.Vector( ( trk["px"],trk["py"], trk["pz"] ) )
    v3 = mathutils.Vector( (dv["x"], dv["y"], dv["z"] ) )
    v4 = v3 + mathutils.Vector( ( dv["tracks_px"], dv["tracks_py"], dv["tracks_pz"] ) )
    
    closest_points = mathutils.geometry.intersect_line_line(v1,v2,v3,v4)

    d = 9999.
    vtx = mathutils.Vector( (9999.,9999.,9999.) )
    if not closest_points: return d,vtx 
    elif not closest_points[0].x : return d,vtx 
    else : 
        (p1,p2) = closest_points 

        d = (p1-p2).magnitude
        vtx = (p1+p2)/2.

    return d,vtx


def randomXCheck(i,dv,tracks):

    v1 = ROOT.TLorentzVector()
    v1.SetPtEtaPhiM(tracks[i]["pt"],tracks[i]["eta"],tracks[i]["phi"],tracks[i]["m"])

    v2 = ROOT.TLorentzVector()
     
    if i in dv['itrks'] : 
        # remove & recompute dv 
        vtx = mathutils.Vector((dv["x"],dv["y"],dv["z"]))
        newtrks = [ ind for ind in dv['itrks']]
        newtrks.remove(i)
        tmpdv = newDV( vtx, newtrks, tracks)
        v2.SetPtEtaPhiM(tmpdv["tracks_pt"],tmpdv["tracks_eta"],tmpdv["tracks_phi"],tmpdv["mass"]) 
        mass_before = tmpdv["mass"]
    else :
        v2.SetPtEtaPhiM(dv["tracks_pt"],dv["tracks_eta"],dv["tracks_phi"],dv["mass"]) 
    
    dEta = abs(v1.Eta()-v2.Eta())
    dPhi = abs(v1.DeltaPhi(v2))
    if dPhi == 0 : return 0
    if dEta == 0 : return 0
    return  math.log10(dEta/dPhi) 


def newDV(vtx,itrks,tracks):

    dv = {}
    
    # temporarily
    # can do a re-fit later
    dv['x'] = vtx[0] #track["prod_x"]
    dv['y'] = vtx[1] #track["prod_y"]
    dv['z'] = vtx[2] #track["prod_z"]
    rxy = (dv['x']*dv['x']+dv['y']*dv['y'])**0.5
    dv['rxy'] = rxy

    #dv['DCA'] = distance 

    sumpt=0
    sumpt2=0
    ntracks=0
    v = ROOT.TLorentzVector()
    for x,track in enumerate(tracks): 
        if x in itrks:
            vtmp = ROOT.TLorentzVector()
            vtmp.SetPtEtaPhiM(track["pt"], track["eta"], track["phi"], 0.139)
            v+= vtmp
            sumpt+=track["pt"]
            sumpt2+=track["pt"]**2
            ntracks+=1

    dv['sumpt'] = sumpt 
    dv['sumpt2'] = sumpt2 
    dv['ntracks'] = ntracks 
    dv["tracks_pt"]  = v.Pt() 
    dv["tracks_eta"] = v.Eta()
    dv["tracks_phi"] = v.Phi()
    dv["tracks_px"]  = v.Px() 
    dv["tracks_py"]  = v.Py()
    dv["tracks_pz"]  = v.Pz()
    dv['mass'] = v.M()
    dv['itrks'] = itrks 

    return dv


def mergeDVs(dvs,tracks):

    mergedDVs=[]
    mergedIDs=[]
    notmerged = 0
    for i,dv1 in enumerate(dvs):
        if i in mergedIDs: 
            merged = 1 
            continue
        merged = 0
        for j,dv2 in enumerate(dvs):
            if i >= j: continue
            #print("IDs , " , i,j)
            if j in mergedIDs: continue
            
            # check for spatial compatibility`
            dx = abs(dv1['x'] - dv2['x'])
            dy = abs(dv1['y'] - dv2['y'])
            dz = abs(dv1['z'] - dv2['z'])
            compatible = ((dx*dx+dy*dy+dz*dz)**0.5 < 1.0)

            # check for subset
            subset = 0
            if ( all(t in dv1['itrks'] for t in dv2['itrks']) ): subset = True
            if ( all(t in dv2['itrks'] for t in dv1['itrks']) ): subset = True

            if compatible or subset : 

                #print("merging dvs ", i, j)
                new_tracks = list(set(dv1['itrks'] + dv2['itrks'])) 
                if len(new_tracks) > len(dv1['itrks']): #not a duplicate dv
                    #print("new tracks ", i, j)
                    x = (dv1['x'] + dv2['x'])/2.
                    y = (dv1['y'] + dv2['y'])/2.
                    z = (dv1['z'] + dv2['z'])/2.
                    vtx = mathutils.Vector((x,y,z))
                    dv1 = newDV(vtx,new_tracks,tracks)
                merged=1
                mergedIDs.append(j)
                mergedIDs.append(i)
        if merged==0: 
            #print("did not merge dv " , i)
            notmerged+=1
            mergedDVs.append(dv1)
        else : 
            mergedDVs.append(dv1)

    return mergedDVs
    #if len(mergedDVs)==len(dvs): return mergedDVs 
    #else: mergeDVs(mergedDVs,tracks)
    
            

def resolveDVambiguity(dvs,tracks):


    for i,trk in enumerate(tracks):

        best_dv = -1
        min_dist = 1.5 
        best_vtx = (0,0,0)
        # figure out which dv track belongs to
        # remove track from all other dvs
        # repeat for all tracks
        for j,dv in enumerate(dvs): 

            # find distance of closest approach for track & dv
            d,vtx = track_DV_intersection(trk,dv)

            # if fit is acceptable 
            if d < 1.5:  
                # then do additional consistency checks
                hit_consistency = abs(trk["prod_rxy"] - dv["rxy"]) 
                z_consistency   = randomXCheck(i,dv,tracks)
                # now test
                #print("made it here", hit_consistency, z_consistency)
                if hit_consistency < 40. and z_consistency < 1.5 :  
                    if best_dv == -1 or dvs[best_dv]["ntracks"] < dv["ntracks"]: 
                        min_dist = d 
                        best_dv = j
                        best_vtx = vtx
                    # store if it's the best track-dv fit
                    elif d < min_dist: 
                        min_dist = d 
                        best_dv = j
                        best_vtx = vtx

        # Now that you know which DV you want.. add or remove tracks from the remaining DVs
        #print( "Now adding or removing tracks to DV" )
        #print( 'track ',i, " best_dv ",best_dv)
        for j,dv in enumerate(dvs):

            #print ( '   checking dv' , j , ' has tracks ' , dv['itrks'] )

            # if it's the best fit DV, then add track to that dv if necessary 
            if j==best_dv:
                if i not in dv['itrks'] and dv['ntracks'] >= 2: # add
                    new_trks = dv['itrks'] + [i]
                    dv = newDV(best_vtx,new_trks,tracks)
                    #print("added track")
                #else : print ("doing nothing")
            # if it's not the best fit, then remove track from that dv if necessary
            else : 
                if i in dv['itrks'] : # remove 
                    #print("need to remove track")
                    #print(dv['itrks'],i)
                    if len(dv['itrks']) <= 2: # no more DV
                        dv["ntracks"]-=1 
                        dv["itrks"]=[-1] 
                    else : 
                        new_trks = dv['itrks']
                        new_trks.remove(i)
                        vtx = mathutils.Vector( (dv['z'],dv['y'],dv['z']) )
                        dv = newDV(vtx,new_trks,tracks)
                #else : print("doing nothing")

    # final loop over dvs
    resolved_dvs = []
    for dv in dvs: 
        if len(dv['itrks']) < 2 : continue
        resolved_dvs.append(dv)
    # remove any dvs with <2 tracks?

    return resolved_dvs 


def constructDVs(tracks,sample='qcd'):

    #print(" ")
    # Seed DVs
    # make all possible 2-track pairs
    dv_2tracks = []

    # only use leading 10 pT tracks to make life easier
    for i,track1 in enumerate(tracks): 
        for j,track2 in enumerate(tracks): 

            if i<=j : continue
            if track1['d0'] < 1.0 : continue # only seed with extra displaced tracks
            if track2['d0'] < 1.0 : continue # only seed with extra displaced tracks

            distance,vtx = two_track_intersection(track1,track2)

            if distance < 1.0: 

                dv = newDV(vtx,[i,j],tracks)
                # mimic hit consistency
                if abs(tracks[i]["prod_rxy"] - dv["rxy"]) > 40.: continue
                if abs(tracks[j]["prod_rxy"] - dv["rxy"]) > 40.: continue

                dv_2tracks.append(dv)
                #print("i,x,y,z : ",i, dv["x"], dv["y"], dv["z"])
                #print("dca : ", distance )
                #print("tracks : ", dv["itrks"])

    # Merge DVs which share tracks or are nearby in x,y,z
    dvs_merged = mergeDVs(dv_2tracks,tracks)

    # clean up track four vector, can't be saved to json
    #print("merged")
    #for dv in dvs_merged: 
    #    print("x,y,z : ", dv["x"], dv["y"], dv["z"])
    #    print("tracks : ", dv["itrks"])

    # check for additional tracks to add and resolve ambiguity for leading tracks
    dvs_resolved = resolveDVambiguity(dvs_merged,tracks) 

    # clean up track four vector, can't be saved to json
    #print("resolved")
    #for dv in dvs_resolved: 
    #    print("x,y,z : ", dv["x"], dv["y"], dv["z"])
    #    print("tracks : ", dv["itrks"])

    #return dvs
    return dvs_resolved # temp

def clusterJets(tracks):

    vectors = np.zeros( len(tracks), dtype=np.dtype([('pT', 'f8'), ('eta', 'f8'), ('phi', 'f8'), ('mass', 'f8'), ('d0', 'f8'), ('prod_z', 'f8')] ) )

    for i,trk in enumerate(tracks): 
        vectors[i] = (trk["pt"], trk["eta"], trk["phi"], 0.139 , trk["d0"], trk["prod_z"])

    sequence = cluster(vectors, R=0.4, p=-1)
    jets = sequence.inclusive_jets()  # list of PseudoJets

    return jets

def compare1D(arrays,labels,weights,outfile,norm=0):
    if "withbkg" in outfile : norm=1
    bins = get_bins(outfile)
    plt.style.use('seaborn-v0_8-colorblind')
    plt.figure(figsize=(6,5.5))

    for i in range(0,len(arrays)):
        (counts, bins) = np.histogram(arrays[i], bins=bins, weights=weights[i])
        factor = len(arrays[i])
        hist_weights = counts/factor if  norm==1 else counts
        if "SM" in labels[i]: 
            plt.hist(bins[:-1], bins, histtype='stepfilled', color="tab:gray", alpha=0.7, label=labels[i], weights=hist_weights)
        else : 
            plt.hist(bins[:-1], bins, histtype='step', label=labels[i], weights=hist_weights)

    if "hit_t" in outfile:
        ax = plt.axes()
        ax.xaxis.set_major_locator(plt.MaxNLocator(5))
        ax.yaxis.set_major_locator(plt.MaxNLocator(5))

    plt.subplots_adjust(left=0.18, right=0.95, top=0.9, bottom=0.18)
    plt.grid(visible=True, which='major', axis='both', color='gainsboro')

    plt.yscale(yscale(outfile))
    #plt.ylim(-0.05,1.05)
   
    size=20 
    plt.xlabel(xtitle(outfile),fontsize=size, labelpad=size/2)
    plt.ylabel(ytitle(outfile),fontsize=size, labelpad=size/2)
    plt.xticks(fontsize=size-4)
    plt.yticks(fontsize=size-4)
    plt.title(title(outfile),fontsize=size-4)
    plt.legend(prop={'size':size-4,})
    #plt.legend(loc=leg_loc(outfile),prop={'size':size-4,})

    plt.savefig(outfile)
    plt.clf()
    plt.close()
    print(outfile)
    return

def analyzePUevents(pileup=2,sample='qcd'):

    # Get events with correct pileup
    f = open('output/{}_pileup{}.json'.format(sample,pileup)) 
    data = json.load(f)
    event_tracks = data['event_tracks']
    weight_array = data['weights']
    event_array  = data['events']
    event_jets = []
    event_dvs = []

    # Initialize output arrays 
    nvertices = [] # event level info

    if "stau" in sample or "suep" in sample: 
        # no need to process DVs or jets, just count
        outdata = {
            "weights"   : weight_array,
            "events"    : event_array,
        }
        with open('output/analyzed_{}_pileup{}.json'.format(sample,pileup), 'w') as fp:
            json.dump(outdata, fp)
        return 

    # Else, we need to loop over pileup events
    for i,trks in enumerate(event_tracks): 

        if doTest and i > 100 : break

        if i%1000==0 : print("event number ",i)  

        z0 = event_array[i]["z0"]
    
        #print(i,z0)
        # Different displaced configs
        for config in displaced_configs:

            #print(config)
            ptcut  = float(config.split(";")[0].strip("pt"))
            d0cut  = float(config.split(";")[1].strip("d")) 

            # Process tracks to form DVs for each config
            tracks = []
            dv_tracks = []
            sum_trk_pt  = 0
            sum_trk_pt2 = 0
            for j,trk in enumerate(trks):

                if trk["pt"] < ptcut : continue
                if abs(trk["eta"]) > 2.5 : continue
                if passes_d0_cut(trk["d0"],d0cut) == 0 : continue
                if trk["prod_rxy"] > 300: continue
                if trk["prod_z"] > 300: continue

                #print(trk["pt"], trk["eta"], trk["phi"], trk["d0"])

                #if abs(trk["prod_z"]-z0) > 1.0 and trk["d0"]<1.0 : continue
                #tracks.append(trk)

                if trk["d0"] < 0.5 : continue
                dv_tracks.append(trk)
                if trk["d0"] < 1.0 : continue
                sum_trk_pt  += trk["pt"]
                sum_trk_pt2 += trk["pt"]**2
        
            # Reconstruct Jets
            #jets = clusterJets(tracks) 
            #evt_jets = []

            #nJetsPrompt    = 0
            #nJetsTotal     = 0
            #nJetsTrackless = 0
            #nJetsDisplaced = 0
            #for j,jet in enumerate(jets): 

            #    if jet.pt < 10.: continue 
            #    nPVConstit = 0
            #    nPromptConstit = 0
            #    nDisplacedConstit = 0

            #    ntrk = float(len(jet.constituents_array()))
            #    if ntrk < 2: continue 

            #    nJetsTotal+=1
            #    for t in jet:
            #        #print(j, jet.pt,t.prod_z,t.d0)
            #        if t.d0 < 0.1 : 
            #            nPromptConstit+=1
            #            if abs(t.prod_z-z0) < 1.0 : nPVConstit+=1
            #        if t.d0 > 1.0 : nDisplacedConstit+=1
            #    if nPVConstit/ntrk > 0.7 : nJetsPrompt += 1
            #    if nPromptConstit/ntrk < 0.7 : nJetsTrackless += 1
            #    if nDisplacedConstit >= 3 and nDisplacedConstit>nPromptConstit  : 
            #        nJetsDisplaced += 1
            #        #print("total,prompt,PV,displaced ",ntrk,nPromptConstit,nPVConstit,nDisplacedConstit)
            #    
            #    jet_dict  = {}
            #    jet_dict["mass"] = jet.mass
            #    jet_dict["pt"] = jet.pt
            #    jet_dict["eta"] = jet.eta
            #    jet_dict["ntrk"] = ntrk 
            #    jet_dict["nPVConstit"] = nPVConstit 
            #    jet_dict["nPromptConstit"] = nPromptConstit
            #    jet_dict["nDisplacedConstit"] = nDisplacedConstit 
            #    jet_dict["fracPV"] = nPVConstit/ntrk
            #    jet_dict["fracDisplaced"] = nDisplacedConstit/ntrk
            #    #print(jet, len(jet.constituents_array()))
            #
            #evt_jets.append(jet_dict)

            # save nJet info to event arrays
            #event_array[i]["nJetsTotal_" +config] = nJetsTotal 
            #event_array[i]["nJetsPrompt_" +config] = nJetsPrompt 
            #event_array[i]["nJetsTrackless_" +config] = nJetsTrackless
            #event_array[i]["nJetsDisplaced_" +config] = nJetsDisplaced

            # Reconstruct DVs
            dvs = constructDVs(dv_tracks,sample) 

            nDVs2 = 0
            nDVs3 = 0
            nDVs4 = 0
            nDVs5 = 0
            for dv in dvs: 
                if dv["rxy"] < 2: continue
                if dv["rxy"] > 300. : continue
                if abs(dv["z"]) > 300. : continue
                if dv["sumpt"] < 6. : continue
                if dv["mass"]  < 2. : continue
                if dv["ntracks"] >= 2 : nDVs2+=1 
                if dv["ntracks"] >= 3 : nDVs3+=1 
                if dv["ntracks"] >= 4 : nDVs4+=1 
                if dv["ntracks"] >= 5 : nDVs5+=1 
                if doTest and dv["ntracks"] > 2 : print("ntrk, rxy, z, sumpt, mass : ", dv["ntracks"], dv["rxy"], dv["z"], dv["sumpt"], dv["mass"])

            # save nDV info to event arrays
            event_array[i]["nDVs_2trks_" +config] = nDVs2 
            event_array[i]["nDVs_3trks_" +config] = nDVs3
            event_array[i]["nDVs_4trks_" +config] = nDVs4
            event_array[i]["nDVs_5trks_" +config] = nDVs5

            event_array[i]["displacedTrack_ptsum_"  +config] = sum_trk_pt 
            event_array[i]["displacedTrack_ptsum2_" +config] = sum_trk_pt2 

            if "pt1.0;d0100" in config: event_dvs.append(dvs)
    

    if doTest: return 

    # event loop over
    # make some quick debugging plots 
    #for config in displaced_configs: 
            
        #nDVs2  = [ evt["nDVs_2trks_" +config] for evt in event_array] 
        #nDVs3  = [ evt["nDVs_3trks_" +config] for evt in event_array]
        #nDVs4  = [ evt["nDVs_4trks_" +config] for evt in event_array]
        #nDVs5  = [ evt["nDVs_5trks_" +config] for evt in event_array]
        #n_dv_arrays = [ nDVs2, nDVs3, nDVs4, nDVs5 ]
        #weights = [weight_array, weight_array, weight_array, weight_array]
        #labels  = ["$\\geq 2$ tracks", "$\\geq 3$ tracks", "$\\geq 4$ tracks", "$\\geq 5$ tracks"]

        #outfile="plots/pileup_fast/n_dvs_{}_pileup{}_config_{}.pdf".format(sample,pileup,config)
        #compare1D(n_dv_arrays,labels,weights,outfile)

        #nJetsTotal      = [ evt["nJetsTotal_" +config] for evt in event_array] 
        #nJetsPrompt     = [ evt["nJetsPrompt_" +config] for evt in event_array] 
        #nJetsTrackless  = [ evt["nJetsTrackless_" +config] for evt in event_array]
        #nJetsDisplaced  = [ evt["nJetsDisplaced_" +config] for evt in event_array]
        #n_dv_arrays = [ nJetsTotal, nJetsPrompt, nJetsTrackless, nJetsDisplaced ]
        #weights = [weight_array, weight_array, weight_array, weight_array ]
        #labels = ["Total", "Prompt", "Trackless", "Displaced"]

        #outfile="plots/pileup_fast/n_jetsDisplaced_{}_pileup{}_config_{}.pdf".format(sample,pileup,config)
        #compare1D(n_dv_arrays,labels,weights,outfile)


    outdata = {
        "weights"   : weight_array,
        "events"    : event_array,
        "event_dvs" : event_dvs  
    }
    

    with open('output/analyzed_{}_pileup{}.json'.format(sample,pileup), 'w') as fp:
        json.dump(outdata, fp)

    return




samples = []
samples.append("higgsportal_125_40_0p1ns")
samples.append("higgsportal_125_55_1ns")
samples.append("qcd")
samples.append("stau_300_1ns")
samples.append("stau_300_0p1ns") 

for sample in samples:
    analyzePUevents(200,sample)

