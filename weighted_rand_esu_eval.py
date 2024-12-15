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
        weight = row['Weight']

        try:
            node1 = float(node1)
            node2 = float(node2)
        except ValueError:
            pass

        G.add_edge(node1, node2, weight=int(weight))
    return G

#converting weighted network to binary-weighted network
def convert_to_binary_weighted(G, threshold=2):
    binary_G = nx.DiGraph()
    for u, v, data in G.edges(data=True):
        weight = data['weight']
        binary_weight = 1 if weight >= threshold else 0
        binary_G.add_edge(u, v, weight=binary_weight)
    return binary_G

#modified Rand-ESU Sampling (for binary-weight subgraph sampling)
def rand_esu_sampling(G, k):
    """
    Modified Rand-ESU algorithm for binary-weighted networks.
    Extends subgraphs iteratively, considering edge weights.
    
    Parameters:
        G (nx.DiGraph): Input binary-weighted directed graph.
        k (int): Target size of subgraphs.
    """
    def extend_subgraph(V_subgraph, V_extension, depth):
        if len(V_subgraph) == k: #if subgraph size reaches k, yield
            yield G.subgraph(V_subgraph)
            return

        V_extension_list = list(V_extension)
        random.shuffle(V_extension_list) #shuffling to ensure randomness
        for next_node in V_extension_list:
            w = None #edge weight
            if (min(V_subgraph), next_node) in G.edges:
                w = G.edges[min(V_subgraph), next_node]['weight']
            elif (next_node, min(V_subgraph)) in G.edges:
                w = G.edges[next_node, min(V_subgraph)]['weight']

            #if the weight is 1, it expands the subgraph in that direction with 98% probability, or selects edges with weight 0 with 2% probability and expands them in that direction.
            if w is not None:
                if w == 1 or (w == 0 and random.random() < 0.02):
                    new_extension = V_extension - {next_node}
                    new_extension |= {u for u in G.neighbors(next_node) if u > min(V_subgraph) and u not in V_subgraph}
                    yield from extend_subgraph(V_subgraph | {next_node}, new_extension, depth + 1)

    for v in G.nodes:
        initial_extension = {u for u in G.neighbors(v) if u > v}
        yield from extend_subgraph({v}, initial_extension, 1)

#measuring sampling speed and storing detected subgraphs
def measure_sampling_speed_and_subgraphs(G, k, iterations=1000):
    start_time = time.time()
    subgraphs = []
    for _ in tqdm(range(iterations), desc=f"Modified Rand-ESU Sampling speed for subgraph size {k}"):
        subgraph = next(rand_esu_sampling(G, k))
        subgraphs.append(subgraph)
    end_time = time.time()
    sampling_speed = iterations / (end_time - start_time)
    return sampling_speed, subgraphs

#datasets
datasets = {
    "Bitcoin Alpha Trust Network": "path/to/bitcoin_alpha_trust_network/bitcoinalpha.csv", 
    "Host Pathogen Interactions": "path/to/host_pathogen_interactions_2015/species_interactions_eid2_weighted.csv",
    "Colombian City Inter-Zone Mobility": "path/to/colombian_city_inter-zone_mobility/OD_DB_Man2005_weighted.csv",
    "Resistance": "path/to/comm_f2f_Resistance/network/network17_new.csv",
    "Cophenagen Networks Study": "path/to/cophenagen_networks_study_icon/bt_symmetric.csv"
}

#subgraph sizes to evaluate
subgraph_sizes = [3, 4, 5, 6, 7, 8]
sampling_speeds_all = {}
detected_subgraphs_all = {}

#evaluate for each dataset
for dataset_name, file_path in datasets.items():
    print(f"\nProcessing dataset: {dataset_name}")
    
    if dataset_name == "Resistance":
        graph = load_edges(file_path, skip_rows_with='TIME')
    else:
        graph = load_edges(file_path)

    binary_graph = convert_to_binary_weighted(graph)
    sampling_speeds = {}
    detected_subgraphs = {}

    for size in subgraph_sizes:
        print(f"\nEvaluating for subgraph size {size} with Modified Rand-ESU on {dataset_name}...")
        speed, subgraphs = measure_sampling_speed_and_subgraphs(binary_graph, size, iterations=1000)
        sampling_speeds[size] = speed
        detected_subgraphs[size] = subgraphs
        print(f"Modified Rand-ESU - Subgraph size {size} on {dataset_name}: Speed = {speed:.2f} subgraphs/second")

    sampling_speeds_all[dataset_name] = sampling_speeds
    detected_subgraphs_all[dataset_name] = detected_subgraphs

#results
with open("modified_rand_esu_results.pkl", "wb") as f:
    pickle.dump(sampling_speeds_all, f)

#visualizing detected subgraph
output_dir = "detected_subgraphs"
os.makedirs(output_dir, exist_ok=True)

for dataset_name, subgraphs_by_size in detected_subgraphs_all.items():
    for size, subgraphs in subgraphs_by_size.items():
        plt.figure(figsize=(15, 15))
        plt.title(f"Detected Motifs of Size {size} for {dataset_name}")
        count = 0
        for subgraph in subgraphs[:1]:
            plt.subplot(1, 1, count + 1)
            pos = nx.spring_layout(subgraph)
            draw_networkx(subgraph, pos=pos, with_labels=True, node_size=400, font_size=8)
            plt.axis('off')
            count += 1
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, f"{dataset_name}_detected_motifs_size_{size}.png"))
        plt.show()
