import unittest

from tests.specific_feature_test import SpecificFeatureTest
from features_algorithms.vertices.attractor_basin import AttractorBasinCalculator
from features_algorithms.vertices.average_neighbor_degree import AverageNeighborDegreeCalculator
from features_algorithms.vertices.bfs_moments import BfsMomentsCalculator
from loggers import PrintLogger


class FeatureTests(SpecificFeatureTest):
    @unittest.skip("Not implemented yet")
    def test_attractor_basin(self):
        self._test_feature(AttractorBasinCalculator, True)
        self._test_feature(AttractorBasinCalculator, False)

    @unittest.skip("Not implemented yet")
    def test_average_neighbor_degree(self):
        self._test_feature(AverageNeighborDegreeCalculator, True)
        self._test_feature(AverageNeighborDegreeCalculator, False)

    @unittest.skip("Not implemented yet")
    def test_betweenness_centrality(self):
        self._test_feature(AverageNeighborDegreeCalculator, True)
        self._test_feature(AverageNeighborDegreeCalculator, False)

    @unittest.skip("Not implemented yet")
    def test_bfs_moments(self):
        self._test_feature(BfsMomentsCalculator, True)
        self._test_feature(BfsMomentsCalculator, False)

    @unittest.skip("Not implemented yet")
    def test_closeness_centrality(self):
        self._test_feature(BfsMomentsCalculator, True)
        self._test_feature(BfsMomentsCalculator, False)

    @unittest.skip("Not implemented yet")
    def test_communicability_betweenness_centrality(self):
        self._test_feature(BfsMomentsCalculator, True)
        self._test_feature(BfsMomentsCalculator, False)

    @unittest.skip("Not implemented yet")
    def test_eccentricity(self):
        self._test_feature(BfsMomentsCalculator, True)
        self._test_feature(BfsMomentsCalculator, False)

    @unittest.skip("Not implemented yet")
    def test_fiedler_vector(self):
        self._test_feature(BfsMomentsCalculator, True)
        self._test_feature(BfsMomentsCalculator, False)

    @unittest.skip("Not implemented yet")
    def test_flow(self):
        self._test_feature(BfsMomentsCalculator, True)
        self._test_feature(BfsMomentsCalculator, False)

    @unittest.skip("Not implemented yet")
    def test_general(self):
        self._test_feature(BfsMomentsCalculator, True)
        self._test_feature(BfsMomentsCalculator, False)

    @unittest.skip("Not implemented yet")
    def test_hierarchy_energy(self):
        self._test_feature(BfsMomentsCalculator, True)
        self._test_feature(BfsMomentsCalculator, False)

    @unittest.skip("Not implemented yet")
    def test_k_core(self):
        self._test_feature(BfsMomentsCalculator, True)
        self._test_feature(BfsMomentsCalculator, False)

    @unittest.skip("Not implemented yet")
    def test_load_centrality(self):
        self._test_feature(BfsMomentsCalculator, True)
        self._test_feature(BfsMomentsCalculator, False)

    @unittest.skip("Not implemented yet")
    def test_louvain(self):
        self._test_feature(BfsMomentsCalculator, True)
        self._test_feature(BfsMomentsCalculator, False)

    @unittest.skip("Not implemented yet")
    def test_motifs(self):
        self._test_feature(BfsMomentsCalculator, True)
        self._test_feature(BfsMomentsCalculator, False)

    def test_page_rank(self):
        self._test_feature(BfsMomentsCalculator, True)
        self._test_feature(BfsMomentsCalculator, False)


if __name__ == '__main__':
    logger = PrintLogger("TestMe")
    # unittest.main()
    suite = unittest.TestLoader().loadTestsFromTestCase(FeatureTests)
    unittest.TextTestRunner(verbosity=1).run(suite)
