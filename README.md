# Reeb Graph for modeling neuronal fiber pathways

Given the trajectories of neuronal fiber pathways, we model the evolution of trajectories that encodes geometrically significant events and calculate their point correspondence in the 3D brain space. Trajectory inter-distance is used as a parameter to control the granularity of the model that allows local or global representation of the tractogram. 

For more details about our algorithm, please refer to our [paper](https://arxiv.org/abs/2108.01175).

## Citation

The system was employed for our research presented in [1], where we propose a novel and efficient algorithm to model high-level topological structures of neuronal fibers. Tractography constructs complex neuronal fibers in three dimensions that exhibit the geometry of white matter pathways in the brain. However, most tractography analysis methods are time consuming and intractable. We develop a computational geometry-based tractography representation that aims to simplify the connectivity of white matter fibers. If the use of the software or the idea of the paper positively influences your endeavours, please cite [1].

[1] **S. Shailja**, Angela Zhang, and B.S. Manjunath, "[A computational geometry approach for modeling neuronal fiber pathways.](https://arxiv.org/abs/2108.01175)"  Submitted to MICCAI 2021.

## Requirements

To download all prerequisites, in the terminal type
`pip install -r requirements.txt`
The code has been tested only on python version 3.7.

For latest code updates, please follow this link https://github.com/s-shailja/ucsb_reeb.
