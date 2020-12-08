import matplotlib.pyplot as plt
import networkx as nx
import argparse
import collections
import os
import powerlaw
import numpy as np
import scipy
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
  # print(f"Avg. PathLength: {nx.average_shortest_path_length(S,method='unweighted'):.5f}")
  print(f"Assortativity: {nx.degree_pearson_correlation_coefficient(S):.5f}")

  degree_sequence = sorted([d for n, d in S.degree()], reverse=True)  # degree sequence
  degreeCount = collections.Counter(degree_sequence)
  max_deg = max([d for n,d in S.degree()])
  # for i in range(0,max_deg+1):
  #   if (i not in degreeCount):
  #     degreeCount[i] = 0
  deg, cnt = zip(*sorted(list(degreeCount.items()),key=lambda x: x[0]))

  log_deg = np.log10(deg)
  log_cnt = np.log10(cnt)
  slope, intercept, r_val, p_val, std_err = scipy.stats.linregress(log_deg[4:40], log_cnt[4:40])

  print(f"Min Deg: {min(deg)} Max Deg: {max(deg)}")
  print(f"Powerlaw fit exponent: {abs(slope):.3f}")

  fit_x = np.linspace(0,3,100)
  fit_y = slope*fit_x + intercept

  plt.figure()
  plt.scatter(np.log10(deg),np.log10(cnt))
  plt.plot(fit_x, fit_y, '-r', label=r'$\alpha=${:.3f}'.format(abs(slope)))
  plt.xlim(-0.5, 2.5)
  plt.ylim(-0.5, 4)
  plt.legend(loc='upper right')
  plt.show()

  if (args.savefig):
    input("ENTER to visualize graph")
    plot_network(S,fname=fname,show=True)