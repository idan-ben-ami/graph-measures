from features_infra.feature_calculators import NodeFeatureCalculator, FeatureMeta


class GeneralCalculator(NodeFeatureCalculator):
    def is_relevant(self):
        return True

    def _calculate(self, include: set):
        if self._gnx.is_directed():
            self._features = {node: (out_deg, in_deg) for
                              (node, out_deg), (_, in_deg) in zip(self._gnx.out_degree(), self._gnx.in_degree())}
        else:
            self._features = {node: deg for node, deg in self._gnx.degree()}


feature_entry = {
    "general": FeatureMeta(GeneralCalculator, {"gen"}),
}


if __name__ == "__main__":
    from tests.specific_feature_test import test_specific_feature
    test_specific_feature(GeneralCalculator)
