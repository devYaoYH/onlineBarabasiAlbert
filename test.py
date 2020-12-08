import matplotlib.pyplot as plt
import networkx as nx
import argparse
import collections
import os
import powerlaw
import numpy as np
import scipy
from plot_fa2 import fa2_layout

DEBUG = True

def gen_exBA(n=50,m=1,p=0,q=0):
  if (DEBUG):
    nx_graph = nx.extended_barabasi_albert_graph(n,m,p,q,seed=0) # Deterministic seed for debugging
  else:
    nx_graph = nx.extended_barabasi_albert_graph(n,m,p,q) # Truly random graph construction
  print(nx.info(nx_graph))
  print(f"Avg. Clustering: {nx.average_clustering(nx_graph):.5f}")
  print(f"Avg. PathLength: {nx.average_shortest_path_length(nx_graph,method='unweighted'):.5f}")
  print(f"Assortativity: {nx.degree_pearson_correlation_coefficient(nx_graph):.5f}")

  degree_sequence = sorted([d for n, d in nx_graph.degree()], reverse=True)  # degree sequence
  degreeCount = collections.Counter(degree_sequence)
  max_deg = max([d for n,d in nx_graph.degree()])
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

  return nx_graph

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
  parser = argparse.ArgumentParser(description="Plot Extended BA random network with Force Atlas 2 visualization")
  parser.add_argument('-n',default=50,type=int)
  parser.add_argument('-m',default=1,type=int)
  parser.add_argument('-p',default=0,type=float)
  parser.add_argument('-q',default=0,type=float)
  parser.add_argument('-fname',default="test",type=str)
  parser.add_argument('--scan',action='store_true')
  parser.add_argument('--show',action='store_true')
  args = parser.parse_args()

  N = args.n # Number of nodes
  M = args.m # Number of edges each iter
  P = args.p # % m edges preferentially added
  Q = args.q # % m edges rewired
  fname = args.fname # Name of graph class

  if (not os.path.exists(fname)):
    os.makedirs(fname)

  if (args.scan):
    for m in range(1,4):
      for p in range(5):
        curP = p*0.05
        for q in range(5):
          curQ = q*0.05
          plot_network(gen_exBA(N,m,curP,curQ),config={"n":N,"m":m,"add":curP,"rewire":curQ},fname=f"{fname}/Plot_{N}_{m}_{curP*100:.0f}_{curQ*100:.0f}",show=args.show)
  else:
    plot_network(gen_exBA(N,M,P,Q),fname=f"{fname}/Plot_{N}_{M}_{P*100:.0f}_{Q*100:.0f}",show=args.show)