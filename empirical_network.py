import matplotlib.pyplot as plt
import networkx as nx
import argparse
import collections
import os
from plot_fa2 import fa2_layout
from util import parse_network_from_csv

def plot_network(nx_graph, config=None, fname="test", show=False):
  positions = fa2_layout(nx_graph,iters=500)

  fig, (ax1,ax2) = plt.subplots(nrows=1,ncols=2,figsize=(16,6))

  if (config is not None):
    ax1.title.set_text(",".join([f"{k}:{v:.3f}" for k,v in config.items()]))
  nx.draw_networkx_nodes(nx_graph, positions, node_size=5, node_color="blue", alpha=0.4, ax=ax1)
  nx.draw_networkx_edges(nx_graph, positions, edge_color="green", alpha=0.05, ax=ax1)

  degree_sequence = sorted([d for n, d in nx_graph.degree()], reverse=True)  # degree sequence
  degreeCount = collections.Counter(degree_sequence)
  max_deg = max([d for n,d in nx_graph.degree()])
  for i in range(0,max_deg+1):
    if (i not in degreeCount):
      degreeCount[i] = 0
  deg, cnt = zip(*degreeCount.items())

  plt.bar(deg, cnt, width=0.80, color="b")

  plt.title("Degree Histogram")
  plt.ylabel("Count")
  plt.xlabel("Degree")
  ax2.set_xticks([d for d in deg])
  ax2.set_xticklabels(deg)
  plt.savefig(f"{fname}.png")
  if (show):
    plt.show()

if __name__ == "__main__":
  parser = argparse.ArgumentParser(description="Plot empirical Smallworld-Of-Words dataset from [Node],[Neighbors ...] adjacency list .csv")
  parser.add_argument('data')
  parser.add_argument('-cutoff',default=3,type=int)
  parser.add_argument('-fname',default="test",type=str)
  parser.add_argument('--weighted',action='store_true')
  parser.add_argument('--savefig',action='store_true')
  args = parser.parse_args()

  raw_graph = args.data # Local file storing adjlist data
  cutoff = args.cutoff  # How many reported instances before we connect an edge
  fname = args.fname    # Name of graph class

  print("Parsing Raw Network")
  G = parse_network_from_csv(raw_graph,cutoff=cutoff)
  print(nx.info(G))
  print(f"Avg. Clustering: {nx.average_clustering(G):.5f}")

  print("Getting largest connected component")
  S = G.subgraph(max(nx.connected_components(G),key=len)).copy()
  print(nx.info(S))
  print(f"Avg. Clustering: {nx.average_clustering(S):.5f}")
  print(f"Avg. PathLength: {nx.average_shortest_path_length(S,method='unweighted'):.5f}")

  if (args.savefig):
    input("ENTER to visualize graph")
    plot_network(S,fname=fname,show=True)