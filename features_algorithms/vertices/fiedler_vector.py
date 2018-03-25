import networkx as nx
import networkx.linalg.algebraicconnectivity as alg_connectivity

from features_infra.feature_calculators import NodeFeatureCalculator, FeatureMeta


class FiedlerVector(NodeFeatureCalculator):
    def _calculate(self, include: set):
        self._features = dict(zip(self._gnx, alg_connectivity.fiedler_vector(self._gnx)))

    def is_relevant(self):
        # Fiedler vector also works only on connected undirected graphs
        # so if gnx is not connected we shall expect an exception: networkx.exception.NetworkXError
        return (not self._gnx.is_directed()) and (nx.is_connected(self._gnx.to_undirected()))


feature_entry = {
    "fiedler_vector": FeatureMeta(FiedlerVector, {"fv"}),
}

if __name__ == "__main__":
    pass
