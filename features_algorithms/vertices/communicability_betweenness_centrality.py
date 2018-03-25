import networkx as nx

from features_infra.feature_calculators import NodeFeatureCalculator, FeatureMeta


class CommunicabilityBetweennessCentralityCalculator(NodeFeatureCalculator):
    def _calculate(self, include: set):
        self._features = nx.communicability_betweenness_centrality(self._gnx)

    def is_relevant(self):
        return True


feature_entry = {
    "communicability_betweenness_centrality": FeatureMeta(CommunicabilityBetweennessCentralityCalculator,
                                                          {"communicability"}),
}

if __name__ == "__main__":
    pass
