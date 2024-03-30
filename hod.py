import numpy as np
from scipy import special

class HOD(object):
    def __init__(self):
        self.logMmin = 11.95
        self.sigmalogM = 0.65
        self.m = None
        self.array_of_thresholdvalues = None

    def N_central(self,M,logMmin,sigmalogM):
        return (1/2*(1+special.erf((np.log10(M)-logMmin)/(sigmalogM))))

    #array should be of shape 4x samplesize 
    def choose_percentile(self,fraction,array):
        N = array.shape[-1]
        percentiles = np.arange(100)
        N_match = np.zeros(len(percentiles))
        p = np.percentile(array,percentiles,axis=-1)
        for i in range(len(percentiles)):
            boolarray=True
            for j in range(array.shape[0]):
                boolarray&=array[j,:]>p[i,j]
            N_match[i]=np.sum(boolarray)/N
        return np.interp(fraction,N_match[::-1],percentiles[::-1])

    def property_threshold(self,halomass,flag,logMmin=None,sigmalogM=None,haloproperty=None):
        """""
        flag = 0 compute the mass threshold relation yourself in this case the HOD parameter should be specified, flag = 1, compute the prev saved relation for default values
        return 4 arrays, each array gives the threshold value of the 4 halo properties respectively. 
        We imagine a scenario where galaxy formation is deterministically linked to whether the concentration of the halo is large, which is not too unreasonable, 
        as we know that haloes with larger concentration have denser inner region which can trigger 
        early galaxy formation, their accretion history suggest that they formed older and underwent more mergers increasing the probabilty to trigger galaxy formation.
        Rule to populate with central galaxy: when the halo has all 4 properties above their respective thresholds, it has a central galaxy.
        """""
        if flag==1:
            massbin = np.logspace(np.log10(halomass.min()),np.log10(halomass.max()),20)
            m = np.sqrt(massbin[1:]*massbin[0:-1])
            array_of_thresholdvalues = np.zeros([haloproperty.shape[0],len(m)])
            for i in range(len(m)):
                fraction = self.N_central(m[i],logMmin,sigmalogM)
                sel = (halomass>massbin[i])&(halomass<massbin[i+1])
                p = self.choose_percentile(fraction,haloproperty[:,sel])
                array_of_thresholdvalues[:,i] = np.percentile(haloproperty[:,sel],p,axis=-1)
            ## replace old default values with new default values
            self.m = m
            self.array_of_thresholdvalues = array_of_thresholdvalues
            self.logMmin = logMmin
            self.sigmalogM = sigmalogM
            a =  np.interp(halomass, m, array_of_thresholdvalues[0,:])
            b =  np.interp(halomass, m, array_of_thresholdvalues[1,:])
            c =  np.interp(halomass, m, array_of_thresholdvalues[2,:])
            d =  np.interp(halomass, m, array_of_thresholdvalues[3,:])
            return a, b, c ,d
        elif flag==0:
            a =  np.interp(halomass, self.m, self.array_of_thresholdvalues[0,:])
            b =  np.interp(halomass, self.m, self.array_of_thresholdvalues[1,:])
            c =  np.interp(halomass, self.m, self.array_of_thresholdvalues[2,:])
            d =  np.interp(halomass, self.m, self.array_of_thresholdvalues[3,:])
            return a,b,c,d
    
    def get_centrals(self,haloproperty,g):
        "returns a boolean array that corresponds to those haloes that do contain a central galaxy"
        sel1 = (haloproperty[0,:]>g[0])&(haloproperty[1,:]>g[1])&(haloproperty[2,:]>g[2])&(haloproperty[3,:]>g[3])        
        return sel1
