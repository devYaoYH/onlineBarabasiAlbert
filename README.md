# Online Barabasi-Albert Random Graph Generator

The Barabasi-Albert model for network growth builds on the notion of preferrential attachment where higher-degree nodes have proportionally higher probability of forming an edge with a newly introduced node. Furthermore, the Exteneded Barabasi-Albert model introduces a probabilistic events for the addition of edges between already present nodes as well as the rewiring of already present edges, both in a preferrential manner.

Such a model has seen wide usage in modelling semantic networks in the domain of language knowledge modeling as it has an intuitive explanation for the acquisition of linguistic concepts. Furthermore, such sparse networks have found use in accounting for semantic closeness and spreading activation behavior observed in psychological studies.

This exploratory project attempts to implement an online version of the extended Barabasi-Albert random growth network model over a continuous stream of nodes. Such a process attempts to model the contextual upkeep and drift over a temporal domain as stimuli are presented to account for variation observed in psychological experiments that are not at the moment well captured.
