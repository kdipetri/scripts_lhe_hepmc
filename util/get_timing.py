
import pyhepmc_ng as hep

c=299792458 #m/s

def decayTime(particle):
    # finds a particles decay time in nanoseconds 
    
    decayvtx = particle.end_vertex
    if (decayvtx) :
        
        # Math goes like this
        #Decay time = decay length/velocity
        #Decay time = decay length/(beta * c)
        #Decay time = decay length/(betagamma / gamma* c ) 
        #Decay time = decay length/(LLP momentum / (LLP gamma * LLP mass) * c) 

        decay_pos = decayvtx.position.length() # in mm
        betagamma = particle.momentum.length()/particle.momentum.m() 
        gamma = ( 1 + (betagamma/c)**2 )**0.5
        velocity = betagamma/gamma * c * 1000. # in mm per second
        decay_time = decay_pos/(velocity)*1e9 # in nanoseconds

        # Consistency tests
        #print()
        #print(decayvtx.position )# length())
        #print()
        #print(particle.momentum)
        #print("p   = ",particle.momentum.length())
        #print("m   = ",particle.momentum.m())
        #print("bg  = ", betagamma)
        #print("gam = ", gamma)
        #print("v = ",velocity)
        #print("t = ",decay_time)
        #print(decay_time, decayvtx.position.t)

        return decay_time # in ns 
    else : return -1 # particle is stable
