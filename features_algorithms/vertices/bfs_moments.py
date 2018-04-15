from collections import Counter

import networkx as nx
import numpy as np

from features_infra.feature_calculators import NodeFeatureCalculator, FeatureMeta


class BfsMomentsCalculator(NodeFeatureCalculator):
    def is_relevant(self):
        return True

    def _calculate(self, include: set):
        for node in self._gnx:
            # calculate BFS distances
            distances = nx.single_source_shortest_path_length(self._gnx, node)
            node_dist = Counter(distances.values())
            dists, weights = zip(*node_dist.items())
            self._features[node] = [float(np.average(weights, weights=dists)), float(np.std(weights))]


feature_entry = {
    "bfs_moments": FeatureMeta(BfsMomentsCalculator, {"bfs"}),
}


if __name__ == "__main__":
    from tests.specific_feature_test import test_specific_feature
    test_specific_feature(BfsMomentsCalculator)
