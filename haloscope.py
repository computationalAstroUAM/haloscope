from sklearn.preprocessing import QuantileTransformer
import numpy as np
class ConditionalMultiVariateGaussian(object):
    def __init__(self, A = np.array([[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,-1,1],[0,0,0,-1]]),b=np.array([0,0,0,0,-1])):        
        self.mux = None
        self.muy = None
        self.sigmaxx = None
        self.sigmayy = None
        self.sigmaxy = None
        self.qtx = QuantileTransformer(n_quantiles=500, random_state=0, output_distribution='normal')
        self.qty = QuantileTransformer(n_quantiles=500, random_state=0, output_distribution='normal')
        self.A = A
        self.b = b
        
    def fit( self,x, y):
        """
        Input:
        x - feature vector (n_samples,n_features)
        y - target vector  (n_samples,n_targets)
        """
        
        x_gaussian = self.qtx.fit_transform(x)
        y_gaussian = self.qty.fit_transform(y)
        
        self.mux = np.median(x_gaussian,axis = 0)
        self.muy = np.median(y_gaussian,axis = 0)
        sigma = np.cov(y_gaussian.T,x_gaussian.T)
        self.sigmaxx = (sigma[y.shape[1]:,y.shape[1]:])
        self.sigmayy = (sigma[0:y.shape[1],0:y.shape[1]])
        self.sigmaxy = (sigma[y.shape[1]:,0:y.shape[1]])
        self.sigmbar = self.sigmayy - self.sigmaxy.T @ np.linalg.inv(self.sigmaxx) @ self.sigmaxy
        return

    def mubar(self,x):
        return self.muy.reshape([self.muy.shape[0],1]).T + (self.sigmaxy.T @ np.linalg.inv(self.sigmaxx) @ (x.T-self.mux.reshape([self.mux.shape[0],1]))).T

    def sampleP(self,size):
        return np.random.multivariate_normal(mean = np.zeros([self.sigmbar.shape[0]]), cov = self.sigmbar, size=size)
    
    def predict(self,xP):
        xg = self.qtx.fit_transform(xP)     ### should this be fit transform or just transform??
        mubar = self.mubar(xg)
        ypred_g = mubar+self.sampleP(xg.shape[0])  
        ypred = self.qty.inverse_transform(ypred_g)
        if self.A is not None:
            print ("here")
            satisfies_constraints = np.all(np.dot(self.A, ypred.T) >= self.b.reshape(-1, 1), axis=0)
            j=0
            total_sampling_number = len(satisfies_constraints)
            while np.all(satisfies_constraints)==False:
                total_sampling_number += np.sum(~satisfies_constraints)
                ypred_g[~satisfies_constraints] = mubar[~satisfies_constraints] + self.sampleP(xg[~satisfies_constraints].shape[0])
                ypred[~satisfies_constraints] = self.qty.inverse_transform(ypred_g[~satisfies_constraints])
                satisfies_constraints = np.all(np.dot(self.A, ypred.T) >= self.b.reshape(-1, 1), axis=0)
                j+=1
                if j==20:
                    break
            print ("acceptance rate is ",len(satisfies_constraints)/total_sampling_number*100,"%")
        else:
            pass
        return ypred
