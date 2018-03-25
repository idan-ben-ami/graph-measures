import networkx as nx

from features_infra.feature_calculators import NodeFeatureCalculator, FeatureMeta


class AverageNeighborDegreeCalculator(NodeFeatureCalculator):
    def is_relevant(self):
        return True

    def _calculate(self, include: set):
        self._features = nx.average_neighbor_degree(self._gnx)


feature_entry = {
    "average_neighbor_degree": FeatureMeta(AverageNeighborDegreeCalculator, {"avg_nd"}),
}


def generate_graph():
    g = nx.Graph()
    g.add_edges_from([
        (1, 2),
        (1, 4),
        (1, 5),
        (2, 3),
        (3, 4),
        (4, 8),
        (4, 5),
        (5, 6),
        (5, 7),
    ])
    return g


def test_feature():
    from loggers import PrintLogger
    logger = PrintLogger("Oved's logger")
    gnx = generate_graph()
    feature = AverageNeighborDegreeCalculator(gnx, logger=logger)
    feature.build()
    print("test finished")


if __name__ == "__main__":
    test_feature()