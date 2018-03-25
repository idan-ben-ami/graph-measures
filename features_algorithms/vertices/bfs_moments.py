from collections import Counter

import networkx as nx
import numpy as np

from features_infra.feature_calculators import NodeFeatureCalculator, FeatureMeta


class BfsMoments(NodeFeatureCalculator):
    def is_relevant(self):
        return True

    def _calculate(self, include: set):
        for node in self._gnx:
            # calculate BFS distances
            distances = nx.single_source_shortest_path_length(self._gnx, node)
            node_dist = Counter(distances.values())
            dist = node_dist.values()
            self._features[node] = [float(np.average(dist, weights=range(1, len(dist) + 1))), float(np.std(dist))]


feature_entry = {
    "bfs_moments": FeatureMeta(BfsMoments, {"bfs"}),
}

if __name__ == "__main__":
    pass
