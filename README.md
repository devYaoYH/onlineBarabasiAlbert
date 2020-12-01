# Online Barabasi-Albert Random Graph Generator

The Barabasi-Albert model for network growth builds on the notion of preferrential attachment where higher-degree nodes have proportionally higher probability of forming an edge with a newly introduced node. Furthermore, the Exteneded Barabasi-Albert model introduces a probabilistic events for the addition of edges between already present nodes as well as the rewiring of already present edges, both in a preferrential manner.

Such a model has seen wide usage in modelling semantic networks in the domain of language knowledge modeling as it has an intuitive explanation for the acquisition of linguistic concepts. Furthermore, such sparse networks have found use in accounting for semantic closeness and spreading activation behavior observed in psychological studies.

This exploratory project attempts to implement an online version of the extended Barabasi-Albert random growth network model over a continuous stream of nodes. Such a process attempts to model the contextual upkeep and drift over a temporal domain as stimuli are presented to account for variation observed in psychological experiments that are not at the moment well captured.

# Preliminary Data

## Empirical Networks Investigation (Base Truth)

We use the openly accessible Smallworld-Of-Words study dataset and filter for UK_English from United Kingdom participants for less variance in our investigation.

```
> python .\empirical_network.py .\UK_native_english.csv -cutoff 3
Parsing Raw Network
Name:
Type: Graph
Number of nodes: 10462
Number of edges: 19861
Average degree:   3.7968
Avg. Clustering: 0.10957
Getting largest connected component
Name:
Type: Graph
Number of nodes: 10271
Number of edges: 19755
Average degree:   3.8468
Avg. Clustering: 0.11161
Avg. PathLength: 6.29308
```

These networks have a remarkably high clustering coefficient. Upon investigation, however, this is likely due to the disassortative nature of this network, with many 2-degree nodes (many spoke-like structures).

## Extended Babarasi-Albert networks

```
PS C:\Users\Yiheng\OneDrive - Washington University in St. Louis\20_Fall\ESE526_NetworkScience\onlineBarabasiAlbert> python test.py -n 10271 -m 2 -fname match
Name:
Type: Graph
Number of nodes: 10271
Number of edges: 20538
Average degree:   3.9992
Avg. Clustering: 0.00301
PS C:\Users\Yiheng\OneDrive - Washington University in St. Louis\20_Fall\ESE526_NetworkScience\onlineBarabasiAlbert> python test.py -n 10271 -m 2 -q 0.2 -fname match
Name:
Type: Graph
Number of nodes: 10271
Number of edges: 20538
Average degree:   3.9992
Avg. Clustering: 0.00192
PS C:\Users\Yiheng\OneDrive - Washington University in St. Louis\20_Fall\ESE526_NetworkScience\onlineBarabasiAlbert> python test.py -n 10271 -m 1 -p 0.5 -fname match
Name:
Type: Graph
Number of nodes: 10271
Number of edges: 20584
Average degree:   4.0082
Avg. Clustering: 0.00226
PS C:\Users\Yiheng\OneDrive - Washington University in St. Louis\20_Fall\ESE526_NetworkScience\onlineBarabasiAlbert> python test.py -n 10271 -m 1 -p 0.45 -fname match
Name:
Type: Graph
Number of nodes: 10271
Number of edges: 18652
Average degree:   3.6320
Avg. Clustering: 0.00283
Avg. PathLength: 5.24944
PS C:\Users\Yiheng\OneDrive - Washington University in St. Louis\20_Fall\ESE526_NetworkScience\onlineBarabasiAlbert> python test.py -n 10271 -m 2 -fname match
Name:
Type: Graph
Number of nodes: 10271
Number of edges: 20538
Average degree:   3.9992
Avg. Clustering: 0.00301
Avg. PathLength: 5.40704
```

Analytically, we would expect the average pathlength in the generated networks to approximate ![logN/loglogN](https://render.githubusercontent.com/render/math?math=\frac{\log%28N%29}{\log\log%28N%29}) which is 6.64924 for the case of ![N=10271](https://render.githubusercontent.com/render/math?math=N%3D10271). However, for the case (N=10271,M=2), we have a much lower 5.40704 value instead, possible due to the low N?

Otherwise, we empirically observe good concurrence with changing the m,p,q parameters for the extended BA model. Increasing p increases the number of edges as well as average degree and decreases the clustering as expected. Increasing q preserves the number of edges as well as average degree, but also decreases clustering as expected.