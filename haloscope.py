#If you use this code, please cite the following paper:
#The multi-dimensional halo assembly bias can be preserved when enhancing halo properties with HALOSCOPE (https://arxiv.org/abs/2410.07361)
from sklearn.preprocessing import QuantileTransformer
import numpy as np

class ConditionalMultiVariateGaussian(object):
    def __init__(self, A=np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, -1, 1], [0, 0, 0, -1]]), 
                 b=np.array([0, 0, 0, 0, -1])):
        """
        Initialize the ConditionalMultiVariateGaussian class.

        Parameters:
        A : np.array
            Coefficient matrix for constraints.
        b : np.array
            Vector for constraints.
        """
        self.mux = None  # Mean of x
        self.muy = None  # Mean of y
        self.sigmaxx = None  # Covariance of x
        self.sigmayy = None  # Covariance of y
        self.sigmaxy = None  # Covariance between x and y
        self.qtx = QuantileTransformer(n_quantiles=500, random_state=0, output_distribution='normal')  # Transformer for x
        self.qty = QuantileTransformer(n_quantiles=500, random_state=0, output_distribution='normal')  # Transformer for y
        self.A = A  # Coefficient matrix for constraints
        self.b = b  # Constraint vector
        
    def fit(self, x, y):
        """
        Fit the model to the provided data.

        Parameters:
        x : np.array
            Feature vector (n_samples, n_features).
        y : np.array
            Target vector (n_samples, n_targets).
        """
        # Transform x and y to follow a Gaussian distribution
        x_gaussian = self.qtx.fit_transform(x)
        y_gaussian = self.qty.fit_transform(y)
        
        # Calculate medians of transformed data
        self.mux = np.median(x_gaussian, axis=0)
        self.muy = np.median(y_gaussian, axis=0)
        
        # Calculate the covariance matrix for the combined data
        sigma = np.cov(y_gaussian.T, x_gaussian.T)
        
        # Extract covariance submatrices
        self.sigmaxx = sigma[y.shape[1]:, y.shape[1]:]  # Covariance of x
        self.sigmayy = sigma[0:y.shape[1], 0:y.shape[1]]  # Covariance of y
        self.sigmaxy = sigma[y.shape[1]:, 0:y.shape[1]]  # Covariance between x and y
        
        # Compute conditional covariance
        self.sigmbar = self.sigmayy - self.sigmaxy.T @ np.linalg.inv(self.sigmaxx) @ self.sigmaxy
        
        return

    def mubar(self, x):
        """
        Calculate the conditional mean of y given x.

        Parameters:
        x : np.array
            Transformed feature vector (n_samples, n_features).

        Returns:
        np.array
            Conditional mean of y.
        """
        return self.muy.reshape([self.muy.shape[0], 1]).T + (
            self.sigmaxy.T @ np.linalg.inv(self.sigmaxx) @ (x.T - self.mux.reshape([self.mux.shape[0], 1]))).T

    def sampleP(self, size):
        """
        Sample from the conditional distribution of y given x.

        Parameters:
        size : int
            Number of samples to generate.

        Returns:
        np.array
            Sampled values from the conditional distribution.
        """
        return np.random.multivariate_normal(mean=np.zeros([self.sigmbar.shape[0]]), cov=self.sigmbar, size=size)
    
    def predict(self, xP):
        """
        Make predictions for new input data.

        Parameters:
        xP : np.array
            New feature vector for predictions (n_samples, n_features).

        Returns:
        np.array
            Predicted values for the target variable.
        """
        # Transform new input data to follow a Gaussian distribution
        xg = self.qtx.fit_transform(xP)  # Note: Should this be fit_transform or just transform?
        
        # Calculate the conditional mean
        mubar = self.mubar(xg)
        
        # Generate predictions based on the conditional mean and sampled noise
        ypred_g = mubar + self.sampleP(xg.shape[0])
        
        # Inverse transform to return predictions to original scale
        ypred = self.qty.inverse_transform(ypred_g)

        # Check for constraints if provided
        if self.A is not None:
            print("here")
            # Check if predictions satisfy constraints
            satisfies_constraints = np.all(np.dot(self.A, ypred.T) >= self.b.reshape(-1, 1), axis=0)
            j = 0  # Iteration counter
            total_sampling_number = len(satisfies_constraints)
            
            # Adjust predictions until they satisfy constraints or max iterations reached
            while np.all(satisfies_constraints) == False:
                total_sampling_number += np.sum(~satisfies_constraints)  # Update total count
                ypred_g[~satisfies_constraints] = mubar[~satisfies_constraints] + self.sampleP(xg[~satisfies_constraints].shape[0])
                ypred[~satisfies_constraints] = self.qty.inverse_transform(ypred_g[~satisfies_constraints])
                
                # Re-check constraints
                satisfies_constraints = np.all(np.dot(self.A, ypred.T) >= self.b.reshape(-1, 1), axis=0)
                j += 1  # Increment counter
                
                # Break loop if max iterations reached
                if j == 20:
                    break
            
            # Output acceptance rate of predictions
            print("acceptance rate is ", len(satisfies_constraints) / total_sampling_number * 100, "%")
        else:
            pass
        
        return ypred  # Return the final predictions
