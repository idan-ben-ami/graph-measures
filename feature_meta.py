from features_algorithms.vertices.attractor_basin import AttractorBasinCalculator
from features_algorithms.vertices.average_neighbor_degree import AverageNeighborDegreeCalculator
from features_algorithms.vertices.betweenness_centrality import BetweennessCentralityCalculator
from features_algorithms.vertices.bfs_moments import BfsMoments
from features_algorithms.vertices.closeness_centrality import ClosenessCentralityCalculator
from features_algorithms.vertices.communicability_betweenness_centrality import \
    CommunicabilityBetweennessCentralityCalculator
from features_algorithms.vertices.eccentricity import EccentricityCalculator
from features_algorithms.vertices.fiedler_vector import FiedlerVector
from features_algorithms.vertices.flow import FlowCalculator
from features_algorithms.vertices.general import GeneralCalculator
from features_algorithms.vertices.hierarchy_energy import HierarchyEnergyCalculator
from features_algorithms.vertices.k_core import KCoreCalculator
from features_algorithms.vertices.load_centrality import LoadCentralityCalculator
from features_algorithms.vertices.louvain import LouvainCalculator
from features_algorithms.vertices.neighbor_nodes_histogram import nth_neighbor_calculator
from features_algorithms.vertices.page_rank import PageRankCalculator
from features_algorithms.vertices.topology import TopologyCalculator
from features_infra.feature_calculators import FeatureMeta, FeatureCalculator

NODE_FEATURES = {
    "attractor_basin": FeatureMeta(AttractorBasinCalculator, {"ab"}),
    "average_neighbor_degree": FeatureMeta(AverageNeighborDegreeCalculator, {"avg_nd"}),
    "betweenness_centrality": FeatureMeta(BetweennessCentralityCalculator, {"betweenness"}),
    "bfs_moments": FeatureMeta(BfsMoments, {"bfs"}),
    "closeness_centrality": FeatureMeta(ClosenessCentralityCalculator, {"closeness"}),
    "communicability_betweenness_centrality": FeatureMeta(CommunicabilityBetweennessCentralityCalculator,
                                                          {"communicability"}),
    "eccentricity": FeatureMeta(EccentricityCalculator, {"ecc"}),
    "fiedler_vector": FeatureMeta(FiedlerVector, {"fv"}),
    "flow": FeatureMeta(FlowCalculator, {}),
    "general": FeatureMeta(GeneralCalculator, {"gen"}),
    "hierarchy_energy": FeatureMeta(HierarchyEnergyCalculator, {"hierarchy"}),
    "k_core": FeatureMeta(KCoreCalculator, {"kc"}),
    "load_centrality": FeatureMeta(LoadCentralityCalculator, {"load_c"}),
    "louvain": FeatureMeta(LouvainCalculator, {"lov"}),
    "page_rank": FeatureMeta(PageRankCalculator, {"pr"}),
    "topology": FeatureMeta(TopologyCalculator, {}),
    "first_neighbor_histogram": FeatureMeta(nth_neighbor_calculator(1), {"fnh", "first_neighbor"}),
    "second_neighbor_histogram": FeatureMeta(nth_neighbor_calculator(2), {"snh", "second_neighbor"}),
}

EDGE_FEATURES = {
    "feat_name": FeatureMeta(FeatureCalculator, {"abbr1", "abbr2"}),
}

GRAPH_FEATURES = {
    "feat_name": FeatureMeta(FeatureCalculator, {"abbr1", "abbr2"}),
}

ALL_FEATURES = {
    "node": NODE_FEATURES,
    "edges": EDGE_FEATURES,
    "graph": GRAPH_FEATURES,
}

# DIRECTED_GRAPH_NODE_FEATURES = {
#     "feat_name": FeatureMeta(FeatureCalculator, {"abbr1", "abbr2"}),
# }
