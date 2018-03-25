import networkx as nx

from features_infra.feature_calculators import NodeFeatureCalculator, FeatureMeta


class PageRankCalculator(NodeFeatureCalculator):
    def __init__(self, alpha=0.9, *args, **kwargs):
        super(PageRankCalculator, self).__init__(*args, **kwargs)
        self._alpha = alpha

    def is_relevant(self):
        # TODO: is relevant for all types of graphs? (directed/ undirected)
        return True

    def _calculate(self, include: set):
        self._features = nx.pagerank(self._gnx, alpha=self._alpha)


feature_entry = {
    "page_rank": FeatureMeta(PageRankCalculator, {"pr"}),
}


# TODO
def test_feature():
    pass


if __name__ == "__main__":
    test_feature()
