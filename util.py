import sys
import networkx as nx
from collections import defaultdict

def read_adjlist_from_csv(fname):
  adjlist = defaultdict(lambda:defaultdict(int))
  with open(fname, 'r') as fin:
    headers = fin.readline()
    for line in fin:
      tokens = [l.strip() for l in line.split(',')]
      node = tokens[0]
      for res in tokens[1:]:
        if (res == "NA"):
          continue
        adjlist[node][res] += 1
  return adjlist

def parse_network_from_csv(fname, cutoff=3):
  adjlist = read_adjlist_from_csv(fname)
  for key in adjlist.keys():
    adjlist[key] = [k[0] for k in filter(lambda x: x[1] >= cutoff, adjlist[key].items())]
  G = nx.Graph()
  for key, li in adjlist.items():
    for neighbor in li:
      G.add_edge(key,neighbor)
  return G