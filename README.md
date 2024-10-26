
# HALOSCOPE - Halo PropertieS having Covariance Preserved with Environment

## Citation

If you use this code, please cite the following paper:

> The multi-dimensional halo assembly bias can be preserved when enhancing halo properties with HALOSCOPE, [Ramakrishnan et al., 2024](https://arxiv.org/abs/2410.07361)

## ConditionalMultiVariateGaussian
This repository contains the `ConditionalMultiVariateGaussian` class, a model for predicting high-resolution dark matter halo properties conditioned on their local density environments. The model leverages conditional multivariate Gaussian modeling and supports customizable linear constraints on predictions. 
---

## Features
- **Conditional Multivariate Gaussian Modeling**: Models conditional dependencies between multivariate input and output data.
- **Quantile Transformation**: Transforms input and output data to approximate Gaussian distributions, which improves prediction accuracy.
- **Linear Constraints**: Ensures generated predictions meet specified linear constraints.
- **Random Sampling**: Supports probabilistic predictions by drawing samples from the conditional distribution.


---

## Installation

To use the `ConditionalMultiVariateGaussian` class, clone this repository and import it into your project as follows:
```python
from haloscope import ConditionalMultiVariateGaussian
```

Ensure that you have the necessary dependencies installed:
```bash
pip install numpy
pip intall sklearn
```

## Usage Example (for enhancing dark matter halo resolution in simulations)

Here’s an example script demonstrating how to use the `ConditionalMultiVariateGaussian` class to predict high-resolution properties of dark matter halos based on their local density environments. In this setup:
- **x_train** and **y_train** represent the local density environment and high-resolution halo properties from a high-resolution simulation.
- **x_test** represents the local density environment from a low-resolution simulation.

```python
import numpy as np
from haloscope import ConditionalMultiVariateGaussian 

# Initialize the ConditionalMultiVariateGaussian model without constraints
cg = ConditionalMultiVariateGaussian(A=A, b=b)

# Generate synthetic data for training and testing as an example

# High-resolution simulation data (for training)
# x_train represents the local density environment of dark matter halos in the high-res simulation
x_train = np.random.randn(100000, 2)  # Example: 100,000 halos with 2 environmental properties
# y_train represents high-resolution properties of dark matter halos in the high-res simulation
y_train = np.random.randn(100000, 3)  # Example: 100,000 halos with 3 detailed properties

# Low-resolution simulation data (for testing/prediction)
# x_test represents the local density environment of dark matter halos in the low-res simulation
x_test = np.random.randn(20000, 2)  # Example: 20,000 halos with 2 environmental properties

# Fit the model on the high-resolution simulation data
cg.fit(x_train, y_train)

# Make predictions for the low-resolution simulation data
# The model will predict high-resolution halo properties for the low-res environment
y_pred = cg.predict(x_test)

# Example usage: y_pred now contains the predicted high-resolution properties of the halos in the low-res simulation
print("Predicted high-resolution properties for low-resolution halos:", y_pred)
```

---

## Class Documentation

### `ConditionalMultiVariateGaussian(A=A, b=b)`

#### Parameters
- **A** (`np.array`, optional): Matrix defining linear constraints on predictions. 
- **b** (`np.array`, optional): Vector for constraints that predictions should meet. 

Default for **A** and **b** is a set of constraints for the dark matter halo properties described by equation 10 in [Ramakrishnan et al., 2024](https://arxiv.org/abs/2410.07361) .

### Methods

#### `fit(x, y)`
Fits the model to the training data.

- **x** (`np.array`): Input data matrix of shape `(n_samples, n_features)`.
- **y** (`np.array`): Output data matrix of shape `(n_samples, n_targets)`.

#### `predict(xP)`
Makes predictions based on new input data.

- **xP** (`np.array`): New input data matrix for predictions of shape `(n_samples, n_features)`.
- **Returns**: Predicted values for `y` of shape `(n_samples, n_targets)`.

---
