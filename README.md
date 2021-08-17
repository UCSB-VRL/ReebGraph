# Reeb Graph for modeling neuronal fiber pathways

Given the trajectories of neuronal fiber pathways, we model the evolution of trajectories that encodes geometrically significant events and calculate their point correspondence in the 3D brain space. Trajectory inter-distance is used as a parameter to control the granularity of the model that allows local or global representation of the tractogram. 

For more details about our algorithm, please refer to our [paper](https://arxiv.org/abs/2108.01175).

## Citation

The system was employed for our research presented in [1], where we propose a novel and efficient algorithm to model high-level topological structures of neuronal fibers. Tractography constructs complex neuronal fibers in three dimensions that exhibit the geometry of white matter pathways in the brain. However, most tractography analysis methods are time consuming and intractable. We develop a computational geometry-based tractography representation that aims to simplify the connectivity of white matter fibers. If the use of the software or the idea of the paper positively influences your endeavours, please cite [1].

[1] Shailja, S., Angela Zhang, and B. S. Manjunath. "A computational geometry approach for modeling neuronal fiber pathways." arXiv preprint arXiv:2108.01175 (2021).

## Requirements

To download all prerequisites, in the terminal type
`pip install -r requirements.txt`

The code has been tested only on python version 3.7.


## Example usage

`python ReebGrraphConstruction.py` will run the code on example track.

 To run the code on a given .trk file, follow these steps:
 1. Store the appear, disappear, connect, and disconnect events for all pair of the trajectories. To do this, run `python dic_dump.py` and use the same path as trkfolder. Note: Change the 'eps' parameter in the files. Also, set the track files path.

 2.`python R_properties.py` will run the code on the provided track. Please change the trkfolder and trkfolderI path in the file. You can compute the graph properites using this file.
 
 An example .trk file has been included in the Data directory.

## Dataset

The code was tested on the publicly available Alzheimer's Disease Neuroimaging Initiative (ADNI) [dataset](http://adni.loni.usc.edu/).

## Acknowledgements

Thanks to the Vision Research Laboratory at the University of California, Santa Barbara.

For latest code updates, please follow this link https://github.com/s-shailja/ucsb_reeb.
