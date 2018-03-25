import networkx as nx

from features_infra.feature_calculators import NodeFeatureCalculator, FeatureMeta


class EccentricityCalculator(NodeFeatureCalculator):
    def _calculate(self, include: set):
        self._features = {node: nx.eccentricity(self._gnx, node) for node in self._gnx}

    def is_relevant(self):
        return True


feature_entry = {
    "eccentricity": FeatureMeta(EccentricityCalculator, {"ecc"}),
}

if __name__ == "__main__":
    pass
