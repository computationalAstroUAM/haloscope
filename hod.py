import numpy as np
from scipy import special
import scipy 
from scipy.stats import rankdata

class HOD(object):
	
	def __init__(self,logMmin,sigmalogM):
		self.logMmin = logMmin
		self.sigmalogM = sigmalogM
	
	def N_central(self,M,fa,fb,fc,fd,A_cen,B_cen,C_cen,D_cen):
		"""
		Returns the average central population for each halo of mass M and ranked halo property fa,fb,fc,fd, the HOD is modified to incorporate the assembly bias
		"""
		### fa,fb,fc,fd are ranks of the four halo properties
		logMmin_new = self.logMmin + A_cen*fa + B_cen*fb +C_cen*fc + D_cen*fd### modification to logMmin
		return (1/2*(1+special.erf((np.log10(M)-logMmin_new)/(self.sigmalogM))))

	def N_central_stand(self,M):
		"""
		Returns the average central population of halo of mass M in the standard HOD without assembly bias
		"""
		## standard HOD for centrals
		return (1/2*(1+special.erf((np.log10(M)-self.logMmin)/(self.sigmalogM))))
    
	def convert_to_rank(self,halomass,haloproperty):
		"""
		converts the iput halo property into rank which will range between -0.5 and 0.5
		use to obtain fa,fb,fc,fd to be used with the HOD
		"""     
		rank = np.zeros([len(haloproperty)])
		massbin = np.logspace(np.log10(halomass.min()),np.log10(halomass.max()),20)
		for i in range(len(massbin)-1):
			select = (halomass>massbin[i])&(halomass<massbin[i+1])
			x = haloproperty[select]
			rank[select] = (rankdata(x)-1)/(np.max(rankdata(x)))
		return rank-0.5

	def get_centrals(self,p):
		"""
		Generating len(p) samples, each sample drawn from binomial dstribution of success parameter p[i] where i is the sample index
		"""
		sel = np.random.binomial(1, p, size=[1,len(p)])
		return sel.flatten().astype(bool)
