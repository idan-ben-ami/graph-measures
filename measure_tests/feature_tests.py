import unittest

from features_algorithms.vertices.betweenness_centrality import BetweennessCentralityCalculator
from features_algorithms.vertices.closeness_centrality import ClosenessCentralityCalculator
from features_algorithms.vertices.communicability_betweenness_centrality import \
    CommunicabilityBetweennessCentralityCalculator
from features_algorithms.vertices.eccentricity import EccentricityCalculator
from features_algorithms.vertices.fiedler_vector import FiedlerVectorCalculator
from features_algorithms.vertices.flow import FlowCalculator
from features_algorithms.vertices.general import GeneralCalculator
from features_algorithms.vertices.hierarchy_energy import HierarchyEnergyCalculator
from features_algorithms.vertices.k_core import KCoreCalculator
from features_algorithms.vertices.load_centrality import LoadCentralityCalculator
from features_algorithms.vertices.louvain import LouvainCalculator
from features_algorithms.vertices.motifs import nth_edges_motif
from features_algorithms.vertices.page_rank import PageRankCalculator
from measure_tests.specific_feature_test import SpecificFeatureTest
from features_algorithms.vertices.attractor_basin import AttractorBasinCalculator
from features_algorithms.vertices.average_neighbor_degree import AverageNeighborDegreeCalculator
from features_algorithms.vertices.bfs_moments import BfsMomentsCalculator
from loggers import PrintLogger


class FeatureTests(SpecificFeatureTest):
    def test_attractor_basin(self):
        self._test_feature(AttractorBasinCalculator, True)
        self._test_feature(AttractorBasinCalculator, False)

    def test_average_neighbor_degree(self):
        self._test_feature(AverageNeighborDegreeCalculator, True)
        self._test_feature(AverageNeighborDegreeCalculator, False)

    def test_betweenness_centrality(self):
        self._test_feature(BetweennessCentralityCalculator, True)
        self._test_feature(BetweennessCentralityCalculator, False)

    def test_bfs_moments(self):
        self._test_feature(BfsMomentsCalculator, True)
        self._test_feature(BfsMomentsCalculator, False)

    @unittest.skip("Not implemented yet")
    def test_closeness_centrality(self):
        self._test_feature(ClosenessCentralityCalculator, True)
        self._test_feature(ClosenessCentralityCalculator, False)

    @unittest.skip("Not implemented yet")
    def test_communicability_betweenness_centrality(self):
        self._test_feature(CommunicabilityBetweennessCentralityCalculator, True)
        self._test_feature(CommunicabilityBetweennessCentralityCalculator, False)

    def test_eccentricity(self):
        # For some reason the directed previous data wasn't calculated
        # self._test_feature(EccentricityCalculator, True)
        self._test_feature(EccentricityCalculator, False)

    def test_fiedler_vector(self):
        self._test_feature(FiedlerVectorCalculator, True)
        self._test_feature(FiedlerVectorCalculator, False)

    @unittest.skip("Not implemented yet")
    def test_flow(self):
        self._test_feature(FlowCalculator, True)
        self._test_feature(FlowCalculator, False)

    def test_general(self):
        self._test_feature(GeneralCalculator, True)
        self._test_feature(GeneralCalculator, False)

    @unittest.skip("Not implemented yet")
    def test_hierarchy_energy(self):
        self._test_feature(HierarchyEnergyCalculator, True)
        self._test_feature(HierarchyEnergyCalculator, False)

    def test_k_core(self):
        self._test_feature(KCoreCalculator, True)
        self._test_feature(KCoreCalculator, False)

    def test_load_centrality(self):
        self._test_feature(LoadCentralityCalculator, True)
        self._test_feature(LoadCentralityCalculator, False)

    @unittest.skip("Not implemented yet")
    def test_louvain(self):
        self._test_feature(LouvainCalculator, True)
        self._test_feature(LouvainCalculator, False)

    @unittest.skip("Not implemented yet")
    def test_motifs(self):
        self._test_feature(nth_edges_motif(3), True)
        self._test_feature(nth_edges_motif(3), False)

    def test_page_rank(self):
        self._test_feature(PageRankCalculator, True)
        self._test_feature(PageRankCalculator, False)


if __name__ == '__main__':
    FeatureTests.logger = PrintLogger("TestMe")
    suite = unittest.TestLoader().loadTestsFromTestCase(FeatureTests)
    unittest.TextTestRunner(verbosity=1).run(suite)
