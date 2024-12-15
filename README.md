# Rand-ESU Algorithm Adaptation for Binary-Weighted Networks

### To run:
1. Clone the repository or download and extract.
2. Navigate to the project folder in the terminal.
3. (Optional) Set up a virtual environment and activate it.
4. Install dependencies with pip install -r requirements.txt.
5. Ensure datasets are correctly placed and paths in scripts are valid.
6. Run the main script with python run.py.

## Description:
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

## Key Features: 
- Modified Rand-ESU Algorithm: The Rand-ESU algorithm was modified to handle binary-weighted networks, where edges with weights ≥ threshold are converted to 1, and others are 0.
- Dataset Evaluation: Comprehensive evaluation of subgraph sampling speed for multiple datasets and subgraph sizes.
- Visualization: Visual representation of detected subgraphs(for comparing the subgraph sampling significance) and comparative sampling speed plots for Initial Rand-ESU and Modified Rand-ESU.

## Modules and Files: 
- initial_rand_esu_eval.py: Evaluation of the initial Rand-ESU algorithm.
- weighted_rand_esu_eval.py: Evaluation of the modified Rand-ESU algorithm with binary-weighted networks.
- combined_plot.py: Combines and visualizes the sampling speed results for different datasets and algorithms.
- run.py: Runs all evaluation and plotting scripts sequentially.

## Algorithms:
### Initial Rand-ESU Algorithm Pseudo-code:
    function rand_esu_sampling_initial(Graph G, int k, List p_d):
        for each node v in G:
            V_subgraph ← {v}
            V_extension ← neighbors(v) where u > v
            call extend_subgraph_initial(V_subgraph, V_extension, 1)
        
    function extend_subgraph_initial(Set V_subgraph, Set V_extension, int depth):
        if |V_subgraph| = k:
            yield subgraph induced by V_subgraph
            return
        
        if depth ≥ |p_d|:
            return

        for each next_node in V_extension:
            if random() > p_d[depth]:
                continue

            V_extension ← V_extension \ {next_node}
            new_extension ← V_extension ∪ {neighbors(next_node) \ V_subgraph}
            call extend_subgraph_initial(V_subgraph ∪ {next_node}, new_extension, depth + 1)
            V_extension ← V_extension ∪ {next_node}
*Edit:* The variable w, originally representing the "next node" for extension, was renamed to next_node to clarify its role in subgraph expansion.

### New Algorithm: Rand-ESU for Binary Weighted Networks Pseudo-code:
    function rand_esu_sampling(Graph G, int k):
        for each node v in G:
            V_subgraph ← {v}
            V_extension ← neighbors(v) where u > v
            call extend_subgraph(V_subgraph, V_extension, 1)

    function extend_subgraph(Set V_subgraph, Set V_extension, int depth):
        if |V_subgraph| = k:
            yield subgraph induced by V_subgraph
            return

        V_extension_list ← shuffled list of V_extension
        for each next_node in V_extension_list:
            w ← weight of edge (min(V_subgraph), next_node) or (next_node, min(V_subgraph))

            if w is None:
                continue

            if w = 1 or (w = 0 and random() < 0.02):
                V_extension ← V_extension \ {next_node}
                new_extension ← V_extension ∪ {neighbors(next_node) \ V_subgraph}
                call extend_subgraph(V_subgraph ∪ {next_node}, new_extension, depth + 1)
                V_extension ← V_extension ∪ {next_node}
                
*Edge Weight Accounting:* The variable w explicitly tracks the edge weight between the subgraph and the candidate node.

*Binary Weight Filtering:* Edges with a weight of 1 are always included, while edges with a weight of 0 are included probabilistically (2% chance). The reason why it is set to 2% is the problem of not being able to sample subgraphs, which is encountered in different network datasets (especially with very few edges with weights larger than the treshold). For different jobs and projects, it can be changed.
For datasets with higher edge weights, it is recommended to reduce it if you want to focus on the most unique subgraphs as much as possible. 

*Shuffled Extension Set:* The extension set is shuffled at each recursion to introduce randomness into motif detection.

*Recursive Expansion:* The algorithm expands the subgraph recursively while considering the binary weights of edges.

### Modifications Compared to Initial Rand-ESU:
*Weight Integration:* The algorithm incorporates edge weights to guide subgraph extension, unlike the initial algorithm which only considered nodes.

*Selective Inclusion:* The probabilistic inclusion of 0-weight edges balances efficiency with motif diversity.

## Evaluation Explanation and Analysis
The evaluation for the Initial Rand-ESU and Modified Rand-ESU (for Binary Weighted Networks) algorithms was performed across five diverse datasets:

1. Bitcoin Alpha Trust Network
2. Host Pathogen Interactions
3. Colombian City Inter-Zone Mobility
4. Resistance
5. Copenhagen Networks Study

- The original weights of the datasets were binary converted by taking treshold=2, i.e. edges with edge weight 1 were set equal to 0 and edges with edge weight 2 or more were set equal to 1. 
- Subgraphs of sizes 3 through 8 vertices were sampled, with 1000 iterations for each subgraph size.
- The sampling speed was measured in terms of subgraphs processed per second, and the results were plotted for comparison.

### Sampling Speed Plot Analysis:
As was done in A Faster Algorithm for Detecting Networks, where the Initial Rand-ESU algorithm was introduced, we evaluated our algorithm with Subgraph Sampling Speed. (The reason why we did not use a parameter like Subgraph Sampling Quality is that with the changes we made to motif significance, we have already enabled our new algorithm to sample more significant subgraphs).

![combined_rand_esu_sampling_speed_plot](https://github.com/user-attachments/assets/09ac833c-640e-4e9c-8402-c7588318c0ec)

The plot depicts the sampling speed (logarithmic scale) against the subgraph size for both algorithms across all datasets. Key observations and analysis are as follows:

- *Expected Decrease in Sampling Speed for New Algorithm (Binary Weight Rand-ESU):*
As expected, the Modified Rand-ESU is slower than the Initial Rand-ESU due to the added complexity of weight accounting. The additional weight-checking mechanism and probabilistic inclusion of lower-weight edges inherently slow down the process.

- *Performance Comparison Highlights:*
Despite the slower overall performance of the modified algorithm, there are notable instances where the new algorithm equaled or surpassed the sampling speed of the initial algorithm:
    - Modified Rand-ESU for Bitcoin Alpha Trust Network nearly matched the Initial Rand-ESU for Copenhagen Networks Study when sampling 5-vertex subgraphs.
    - The Modified Rand-ESU Bitcoin Alpha Trust Network outperformed the Initial Rand-ESU for Host Pathogen Interactions in sampling 4-vertex subgraphs. This demonstrates the potential of the new algorithm in specific network conditions.

- *Dataset-Specific Variations:*
    - The Bitcoin Alpha Trust Network consistently performed better under the Modified Rand-ESU algorithm, likely due to its high density and binary structure, which aligned well with the algorithm’s design.

### Conclusion:

The Modified Rand-ESU Algorithm successfully incorporates edge weights into the subgraph sampling process, with a tradeoff in sampling speed. While the new algorithm is generally slower than the Initial Rand-ESU, it demonstrates competitive performance in certain datasets and subgraph sizes, which validates its utility for weighted network analysis.

This evaluation underscores that the modified algorithm is particularly suited for datasets where edge weights carry significant importance in motif detection, while the Initial Rand-ESU remains advantageous for purely topological motif analysis.

Based on all these results, we can see that we have made the Rand-ESU algorithm suitable for Binary Weighted Networks, without taking it too far from the purpose for which it was developed (to be faster than the previous algorithm, ESA).

## Detecting Significant Subgraphs:
To test one of the main sub-objectives of our project, to focus on more significant subgraphs, we printed and analyzed a random selected subgraph detected in 8 sized-subgraphs of the Bitcoin Alpha Trust Network, Resistance and Copenhagen network datasets.

### Bitcoin Alpha Trust Network:
*From Initial Algorithm:*

![bitcoin_initial_subgraph_significance](https://github.com/user-attachments/assets/c3425869-1bd8-4fc7-ad32-a120dbd5ac27)

As seen above, the weights of all edges of the first obtained 8-sized subgraph from the network, if we sort the edges going to each node in the clockwise order starting from 7595->7556:
-10,1,2,1,1,1,1. After binarization: 0,0,1,0,0,0,0.

Then,

*From New Algorithm:*

![bitcoin_weighted_subgraph_significance](https://github.com/user-attachments/assets/fa6b53a8-8281-4be5-8729-6bdfae4dc0f5)

With the new algorithm, if we want to see the edge-weights of the 8-sized subgraph obtained again, we see that the edge-weights of the subgraph above, starting from 1->1261, we go through the nodes clockwise in order and look at the edge-weights:
2,1,2,2,2,3,2 and after binarization: 1,0,1,1,1,1,1.

So, we can easily see that the subgraphs acquired after the new algorithm is included are much, much significant.
Initial Algorithms subgraphs binary edge weights: 0,0,1,0,0,0,0.
New Algorithms subgraphs binary edge weights: 1,0,1,1,1,1,1.

When we did the same for other datasets, we got the following results:
### Resistance Network:

*From Initial Algorithm:*

![resistance_initial_subgraph_significance](https://github.com/user-attachments/assets/956f96bd-8100-457f-ba52-b0774c7f4bc2)

Starting from 0.0->0.517, if we go through the nodes clockwise in order and look at the edge-weights:
1,1,1,7,1,1,1,2 and after binarization: 0,0,0,1,0,0,0,1.

*From New Algorithm:*

![resistance_weighted_subgraph_significance](https://github.com/user-attachments/assets/7c61d1e8-adc0-47fc-ab39-6a962e68692e)

Starting from 0.0->0.056, if we go through the nodes clockwise in order and look at the edge-weights:
1,2,7,1,4,1,2,1 and after binarization: 0,1,1,0,1,0,1,0.

Initial Algorithms subgraphs binary edge weights: 0,0,0,1,0,0,0,1.
New Algorithms subgraphs binary edge weights: 0,1,1,0,1,0,1,0.

### Copenhagen Network:
*From Initial Algorithm:*

![copenhagen_initial_subgraph_significance](https://github.com/user-attachments/assets/a2ae89a9-b29c-4dac-a6d9-eee2deb1c154)

Starting from 0.0->2.0, if we go through the nodes clockwise in order and look at the edge-weights:
1,1,310,1,1,1,1,1 and after binarization:0,0,1,0,0,0,0,0.

*From New Algorithm:*

![cophenagen_weighted_subgraph_significance](https://github.com/user-attachments/assets/98c9b62d-ad2c-43dc-a863-b7b833b29748)

Starting from 0.0->599.0, if we go through the nodes clockwise in order and look at the edge-weights:
2,2,310,2,2,2,2,2 and after binarization: 1,1,1,1,1,1,1,1.

Initial Algorithms subgraphs binary edge weights: 0,0,1,0,0,0,0,0.

New Algorithms subgraphs binary edge weights: 1,1,1,1,1,1,1,1.

The comparison of subgraphs detected by the initial and new algorithms highlights the significant improvement in the quality and relevance of subgraphs obtained using the new algorithm. By incorporating edge weights into the motif detection process, the new algorithm consistently identifies subgraphs with higher significance across all datasets. For example, in the Bitcoin Alpha Trust Network, the new algorithm produced subgraphs with a majority of binary weights as 1, indicating stronger connections, whereas the initial algorithm's subgraphs predominantly contained binary weights of 0. Similar results were observed in the Resistance and Copenhagen networks, where the new algorithm identified subgraphs with more meaningful structures and higher-weight edges. These findings demonstrate that the modified Rand-ESU algorithm successfully prioritizes more significant subgraphs, aligning with the project’s goal of enhancing motif detection in weighted networks.

### Barbaros ISIK & Virginia SAMEZ.
