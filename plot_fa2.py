import os
import pickle
import networkx as nx
from fa2 import ForceAtlas2

CACHE_FOLDER = "cache"

def fa2_layout(nx_graph, iters=500):
  if (not os.path.exists(CACHE_FOLDER)):
    os.makedirs(CACHE_FOLDER)
  g_hash = nx.weisfeiler_lehman_graph_hash(nx_graph)
  fa2_cached_layout = f"{CACHE_FOLDER}/{g_hash}.fa2"
  if (os.path.isfile(fa2_cached_layout)):
    with open(fa2_cached_layout, 'rb') as fin:
      return pickle.load(fin)

  forceatlas2 = ForceAtlas2(
    # Behavior alternatives
    outboundAttractionDistribution=True,  # Dissuade hubs
    linLogMode=False,  # NOT IMPLEMENTED
    adjustSizes=False,  # Prevent overlap (NOT IMPLEMENTED)
    edgeWeightInfluence=0,

    # Performance
    jitterTolerance=1.0,  # Tolerance
    barnesHutOptimize=True,
    barnesHutTheta=1.2,
    multiThreaded=False,  # NOT IMPLEMENTED

    # Tuning
    scalingRatio=2.0,
    strongGravityMode=False,
    gravity=1.0,

    # Log
    verbose=True)

  positions = forceatlas2.forceatlas2_networkx_layout(nx_graph, pos=None, iterations=iters)
  with open(fa2_cached_layout, 'wb+') as fout:
    pickle.dump(positions, fout)
  return positions