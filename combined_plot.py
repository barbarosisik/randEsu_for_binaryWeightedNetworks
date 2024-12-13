import matplotlib.pyplot as plt
import matplotlib.cm as cm
import pickle

#loading saved results
with open("modified_rand_esu_results.pkl", "rb") as f:
    modified_results = pickle.load(f)

with open("initial_rand_esu_results.pkl", "rb") as f:
    initial_results = pickle.load(f)

#subgraph sizes
subgraph_sizes = [3, 4, 5, 6, 7, 8]

#plotting
plt.figure(figsize=(12, 8))
colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k'] 
linestyles = ['-', '--', ':']

for idx, dataset_name in enumerate(modified_results.keys()):
    #weight included Rand-ESU results
    plt.plot(subgraph_sizes, list(modified_results[dataset_name].values()), color=colors[idx], linestyle=linestyles[0], marker='o', label=f'Modified Rand-ESU {dataset_name}')
    #initial Rand-ESU results
    plt.plot(subgraph_sizes, list(initial_results[dataset_name].values()), color=colors[idx], linestyle=linestyles[1], marker='x', label=f'Initial Rand-ESU {dataset_name}')

plt.xscale('linear')
plt.yscale('log')
plt.xlabel('Subgraph Size (vertices)')
plt.ylabel('Sampling Speed (subgraphs/second)')
plt.title('Rand-ESU Sampling Speed vs Subgraph Size for Different Datasets')
plt.legend()
plt.savefig("combined_rand_esu_sampling_speed_plot.png")
plt.show()
