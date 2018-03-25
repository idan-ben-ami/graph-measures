import networkx as nx

from features_infra.feature_calculators import NodeFeatureCalculator, FeatureMeta


class TopologyCalculator(NodeFeatureCalculator):
    def is_relevant(self):
        return False

    def _calculate(self, include: set):
        self._features = nx.simple_cycles(self._gnx)


feature_entry = {
    "topology": FeatureMeta(TopologyCalculator, {}),
}

if __name__ == "__main__":
    pass
