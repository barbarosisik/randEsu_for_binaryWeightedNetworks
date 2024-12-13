# Rand-ESU Algorithm Adaptation for Binary-Weighted Networks

### Description:
This project focuses on adapting and evaluating the Rand-ESU algorithm to work with binary-weighted networks. The primary objectives include implementing modifications to the Rand-ESU algorithm for binary-weighted networks, evaluating its performance on multiple datasets, and visualizing the detected subgraphs and sampling speed. Offering a new way to detect more significant subgraphs in binary weighted networks.

### The network datasets are:
*Bitcoin Alpha Trust Network:* Bitcoin Alpha trust network data in a directed graph with weights.
(https://www.kaggle.com/datasets/boneacrabonjac/bitcoin-alpha) (S. Kumar, F. Spezzano, V.S. Subrahmanian, C. Faloutsos. Edge Weight Prediction in Weighted Signed Networks.)

*Host Pathogen Interactions:* Protein-protein interaction networks.
(https://figshare.com/articles/dataset/SpeciesInteractions_EID2/1381853?file=2196534) (Maya Wardeh, Claire Risley, Marie McIntyre, Christian Setzkorn, Matthew Baylis)

*Colombian City Inter-Zone Mobility:* Traffic flow between zones in a city.
(https://datadryad.org/stash/dataset/doi:10.5061/dryad.hj1t4) (L. Lotero et al., "Rich do not rise early: spatio-temporal patterns in the mobility networks of different socio-economic classes." Royal Society Open Science 3, 150654 (2016))
(We only used the dataset: OD_DB_Man2005.xlsx)

*Resistance:* Dynamic face-to-face interaction network between group of people.
(https://snap.stanford.edu/data/comm-f2f-Resistance.html) (S. Kumar, C.Bai, V.S. Subrahmanian, J. Leskovec. Deception Detection in Group Video Conversations using Dynamic Interaction Networks. 15th International AAAI Conference on Web and Social Media (ICWSM), 2021.)
(We only used: network17.csv)

*Copenhagen Networks Study:* Social interaction networks for scientific studies.
(https://figshare.com/articles/dataset/The_Copenhagen_Networks_Study_interaction_data/7267433/1) (P. Sapiezynski, et al., "Interaction data from the Copenhagen Networks Study." Scientific Data 6, 315 (2019))
(We only used: bt_symmetric.csv)

### Key Features: 
Modified Rand-ESU Algorithm: The Rand-ESU algorithm was modified to handle binary-weighted networks, where edges with weights ≥ threshold are converted to 1, and others are 0.
Dataset Evaluation: Comprehensive evaluation of subgraph sampling speed for multiple datasets and subgraph sizes.
Visualization: Visual representation of detected subgraphs(for comparing the subgraph sampling significance) and comparative sampling speed plots for Initial Rand-ESU and Modified Rand-ESU.

### Modules and Files: 
initial_rand_esu_eval.py: Evaluation of the initial Rand-ESU algorithm.
weighted_rand_esu_eval.py: Evaluation of the modified Rand-ESU algorithm with binary-weighted networks.
combined_plot.py: Combines and visualizes the sampling speed results for different datasets and algorithms.
run.py: Runs all evaluation and plotting scripts sequentially.

### Barbaros ISIK & Virginia SAMEZ.
