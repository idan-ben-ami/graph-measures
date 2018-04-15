import networkx as nx

from features_infra.feature_calculators import NodeFeatureCalculator, FeatureMeta


class KCoreCalculator(NodeFeatureCalculator):
    def is_relevant(self):
        return True

    def _calculate(self, include: set):
        self._features = nx.core_number(self._gnx)


feature_entry = {
    "k_core": FeatureMeta(KCoreCalculator, {"kc"}),
}

if __name__ == "__main__":
    from tests.specific_feature_test import test_specific_feature
    test_specific_feature(KCoreCalculator)
