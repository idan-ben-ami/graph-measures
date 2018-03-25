from collections import Counter

import networkx as nx
from networkx.algorithms.shortest_paths import weighted

from features_infra.feature_calculators import NodeFeatureCalculator, FeatureMeta


class AttractorBasinCalculator(NodeFeatureCalculator):
    def __init__(self, *args, alpha=2, **kwargs):
        super(AttractorBasinCalculator, self).__init__(*args, **kwargs)
        self._alpha = alpha

    def is_relevant(self):
        return self._gnx.is_directed()

    def _calculate(self, include: set):
        # arrange the details for the calculations
        attractor_basin_details = self._initialize_attraction_basin_dist()
        self._calc_final_attraction_basin(attractor_basin_details)

    def _initialize_attraction_basin_dist(self):
        attractor_basin_in_dist = {}
        attractor_basin_out_dist = {}

        # for each node we are calculating the the out and in distances for the other nodes in the graph
        dists = weighted.all_pairs_dijkstra_path_length(self._gnx, len(self._gnx), weight='weight')
        for node in self._gnx:
            if node not in dists:
                continue

            node_dists = dists[node]
            count_out_dist = Counter([node_dists.get(d) for d in nx.descendants(self._gnx, node)])
            count_in_dist = Counter([node_dists.get(d) for d in nx.ancestors(self._gnx, node)])
            count_out_dist.pop(None, None)
            count_in_dist.pop(None, None)

            attractor_basin_out_dist[node] = count_out_dist
            attractor_basin_in_dist[node] = count_in_dist

        # calculate "avg_out" and "avg_in" for each distance from the details of all the nodes
        avg_out = self._calc_avg_for_dist(len(self._gnx), attractor_basin_out_dist)
        avg_in = self._calc_avg_for_dist(len(self._gnx), attractor_basin_in_dist)
        return [attractor_basin_out_dist, avg_out, attractor_basin_in_dist, avg_in]

    def _calculate(self, incluse: set):
        attractor_basin_out_dist, avg_out, attractor_basin_in_dist, avg_in = \
            self._initialize_attraction_basin_dist()

        # running on all the nodes and calculate the value of 'attraction_basin'
        for node in self._gnx:
            self._features[node] = -1

            out_dist = attractor_basin_out_dist.get(node, {})
            in_dist = attractor_basin_in_dist(node, {})

            denominator = sum((dist / avg_out[m]) * (self._alpha ** (-m)) for m, dist in out_dist.items())
            if 0 != denominator:
                numerator = sum((dist / avg_in[m]) * (self._alpha ** (-m)) for m, dist in in_dist.items())
                self._features[node] = numerator / denominator

    @staticmethod
    def _calc_avg_for_dist(num_nodes, count_dist):
        # arange the details in "count_dist" to be with unique distance in the array "all_dist_count"
        all_dist_count = {}
        for counter in count_dist.values():
            for dist, occurrences in counter.items():
                all_dist_count[dist] = all_dist_count.get(dist, 0) + occurrences

        # calculating for each distance the average
        return {dist: float(count) / num_nodes for dist, count in all_dist_count.items()}


feature_entry = {
    "attractor_basin": FeatureMeta(AttractorBasinCalculator, {"ab"}),
}


if __name__ == "__main__":
    pass
