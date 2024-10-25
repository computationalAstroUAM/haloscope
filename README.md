
# HALOSCOPE - Halo PropertieS having Covariance Preserved with Environment

## ConditionalMultiVariateGaussian

This repository contains the `ConditionalMultiVariateGaussian` class, a model for predicting high-resolution dark matter halo properties conditioned on their local density environments. The model leverages conditional multivariate Gaussian modeling and supports customizable linear constraints on predictions. 
---

## Features
- **Conditional Multivariate Gaussian Modeling**: Models conditional dependencies between multivariate input and output data.
- **Quantile Transformation**: Transforms input and output data to approximate Gaussian distributions, which improves prediction accuracy.
- **Linear Constraints**: Ensures generated predictions meet specified linear constraints.
- **Random Sampling**: Supports probabilistic predictions by drawing samples from the conditional distribution.

## Citation

If you use this code, please cite the following paper:

> The multi-dimensional halo assembly bias can be preserved when enhancing halo properties with HALOSCOPE, [Ramakrishnan et al., 2024](https://arxiv.org/abs/2410.07361)

---

## Installation

To use the `ConditionalMultiVariateGaussian` class, clone this repository and import it into your project as follows:
```python
from haloscope import ConditionalMultiVariateGaussian

