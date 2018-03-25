import networkx as nx

from features_infra.feature_calculators import NodeFeatureCalculator, FeatureMeta


class ClosenessCentralityCalculator(NodeFeatureCalculator):
    def _calculate(self, include: set):
        self._features = nx.closeness_centrality(self._gnx)

    def is_relevant(self):
        return True


feature_entry = {
    "closeness_centrality": FeatureMeta(ClosenessCentralityCalculator, {"closeness"}),
}

if __name__ == "__main__":
    pass
