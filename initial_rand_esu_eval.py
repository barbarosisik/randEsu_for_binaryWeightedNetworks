import networkx as nx
import time
import random
import matplotlib.pyplot as plt
from tqdm import tqdm
import pandas as pd
import pickle
import os
from networkx.drawing.nx_pylab import draw_networkx

#load dataset function
def load_edges(file_path, skip_rows_with='TIME'):
    G = nx.DiGraph()
    df = pd.read_csv(file_path)
    df.columns = df.columns.str.strip()

    for _, row in df.iterrows():
        if skip_rows_with and row['Source'] == skip_rows_with:
            continue #skipping rows with 'Source'

        node1 = row['Source']
        node2 = row['Target']

        try:
            node1 = float(node1)
            node2 = float(node2)
        except ValueError:
            pass

        G.add_edge(node1, node2)
    return G

#initial Rand-ESU Sampling
def rand_esu_sampling_initial(G, k, p_d):
    """
    Initial Rand-ESU algorithm for sampling subgraphs.
    Extends subgraphs iteratively, sampling with probability p_d at each depth.

    Parameters:
        G (nx.DiGraph): Input directed graph.
        k (int): Target size of subgraphs.
        p_d (list): Probabilities for including nodes at each depth.
    """
    def extend_subgraph(V_subgraph, V_extension, depth):
        if len(V_subgraph) == k: #if subgraph size reaches k, yield
            yield G.subgraph(V_subgraph)
            return

        if depth >= len(p_d): #terminating if depth exceeds probability array size
            return

        for _ in range(len(V_extension)):
            if random.random() > p_d[depth]: #skipping with probability (1 - p_d[depth])
                continue

            next_node = V_extension.pop() #choosing the next node to add
            #creating a new extension set by including neighbors of the chosen node
            new_extension = V_extension | {u for u in G.neighbors(next_node) if u > min(V_subgraph) and u not in V_subgraph}
            yield from extend_subgraph(V_subgraph | {next_node}, new_extension, depth + 1)
            V_extension.add(next_node) #adding back the node to the extension set for the next iteration

    for v in G.nodes: #starting the process for each node in the graph
        initial_extension = {u for u in G.neighbors(v) if u > v} #includes only higher-index neighbors
        yield from extend_subgraph({v}, initial_extension, 1)

#measure sampling speed and store detected subgraphs
def measure_sampling_speed_and_subgraphs_initial(G, k, p_d, iterations=1000):
    start_time = time.time()
    subgraphs = []
    for _ in tqdm(range(iterations), desc=f"Initial Rand-ESU Sampling speed for subgraph size {k}"):
        subgraph = next(rand_esu_sampling_initial(G, k, p_d))
        subgraphs.append(subgraph)
    end_time = time.time()
    sampling_speed = iterations / (end_time - start_time)
    return sampling_speed, subgraphs

#datasets
datasets = {
    "Bitcoin Alpha Trust Network": "/Users/barbarosisik/Desktop/social_network_analysis_for_computer_scientists/final_project/contribution/bitcoin_alpha_trust_network/bitcoinalpha.csv", 
    "Host Pathogen Interactions": "/Users/barbarosisik/Desktop/social_network_analysis_for_computer_scientists/final_project/contribution/host_pathogen_interactions_2015/species_interactions_eid2_weighted.csv",
    "Colombian City Inter-Zone Mobility": "/Users/barbarosisik/Desktop/social_network_analysis_for_computer_scientists/final_project/contribution/colombian_city_inter-zone_mobility/OD_DB_Man2005_weighted.csv",
    "Resistance": "/Users/barbarosisik/Desktop/social_network_analysis_for_computer_scientists/final_project/contribution/comm-f2f-Resistance/network/network17_new.csv",
    "Cophenagen Networks Study": "/Users/barbarosisik/Desktop/social_network_analysis_for_computer_scientists/final_project/contribution/cophenagen_networks_study_icon/bt_symmetric.csv"
}

#subgraph sizes and probabilities
subgraph_sizes = [3, 4, 5, 6, 7, 8]
p_d_values = [0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1]

sampling_speeds_all = {}
detected_subgraphs_all = {}

#evaluate for each dataset
for dataset_name, file_path in datasets.items():
    print(f"\nProcessing dataset: {dataset_name}")
    
    if dataset_name == "Resistance":
        graph = load_edges(file_path, skip_rows_with='TIME')
    else:
        graph = load_edges(file_path)

    sampling_speeds = {}
    detected_subgraphs = {}

    for size in subgraph_sizes:
        p_d = p_d_values[:size] #using probabilities for the current subgraph size
        print(f"\nEvaluating for subgraph size {size} with Initial Rand-ESU on {dataset_name}...")
        speed, subgraphs = measure_sampling_speed_and_subgraphs_initial(graph, size, p_d, iterations=1000)
        sampling_speeds[size] = speed
        detected_subgraphs[size] = subgraphs
        print(f"Initial Rand-ESU - Subgraph size {size} on {dataset_name}: Speed = {speed:.2f} subgraphs/second")

    sampling_speeds_all[dataset_name] = sampling_speeds
    detected_subgraphs_all[dataset_name] = detected_subgraphs

#results
with open("initial_rand_esu_results.pkl", "wb") as f:
    pickle.dump(sampling_speeds_all, f)

#visualizing Detected Subgraphs
output_dir = "detected_subgraphs_initial"
os.makedirs(output_dir, exist_ok=True)

for dataset_name, subgraphs_by_size in detected_subgraphs_all.items():
    for size, subgraphs in subgraphs_by_size.items():
        plt.figure(figsize=(15, 15))
        plt.title(f"Detected Motifs of Size {size} for {dataset_name}")
        count = 0
        for subgraph in subgraphs[:1]:
            plt.subplot(1, 10, count + 1)
            pos = nx.spring_layout(subgraph)
            draw_networkx(subgraph, pos=pos, with_labels=True, node_size=600, font_size=8)
            plt.axis('off')
            count += 1
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, f"{dataset_name}_detected_motifs_size_{size}.png"))
        plt.show()
