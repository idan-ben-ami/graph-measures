import string
from functools import partial
from itertools import product as cartesian

import networkx as nx
import numpy as np
from networkx.algorithms.shortest_paths import unweighted

from features_infra.feature_calculators import NodeFeatureCalculator, FeatureMeta
from loggers import PrintLogger


class NeighborHistogramCalculator(NodeFeatureCalculator):
    DUMPABLE = False

    def __init__(self, neighbor_order, *args, **kwargs):
        super(NeighborHistogramCalculator, self).__init__(*args, **kwargs)
        self._num_classes = len(self._gnx.graph["node_labels"])
        self._neighbor_order = neighbor_order

    def is_relevant(self):
        raise NotImplementedError()

    def _calculate(self, include: set):
        # Translating each label to a relevant index to save memory
        return {label: idx for idx, label in enumerate(self._gnx.graph["node_labels"])}


class DirectedNthNeighborNodeHistogramCalculator(NeighborHistogramCalculator):
    def __init__(self, *args, **kwargs):
        super(DirectedNthNeighborNodeHistogramCalculator, self).__init__(*args, **kwargs)
        counter = {i: 0 for i in range(self._num_classes)}
        self._print_name += "_%d" % (self._neighbor_order,)
        self._relation_types = ["".join(x) for x in cartesian(*(["io"] * self._neighbor_order))]
        self._features = {node: {rtype: counter.copy() for rtype in self._relation_types} for node in self._gnx}

    def is_relevant(self):
        return self._gnx.is_directed()

    def _get_node_neighbors_with_types(self, node):
        if self._gnx.is_directed():
            for in_edge in self._gnx.in_edges(node):
                yield ("i", in_edge[0])

        for out_edge in self._gnx.out_edges(node):
            yield ("o", out_edge[1])

    def _iter_nodes_of_order(self, node, order):
        if 0 >= order:
            yield [], node
            return
        for r_type, neighbor in self._get_node_neighbors_with_types(node):
            for r_type2, neighbor2 in self._iter_nodes_of_order(neighbor, order - 1):
                yield ([r_type] + r_type2, neighbor2)

    def _calculate(self, include: set):
        # Translating each label to a relevant index to save memory
        labels_map = super(DirectedNthNeighborNodeHistogramCalculator, self)._calculate(include)

        for node in self._gnx:
            history = {rtype: set() for rtype in self._relation_types}
            for r_type, neighbor in self._iter_nodes_of_order(node, self._neighbor_order):
                full_type = "".join(r_type)
                if node == neighbor or neighbor not in include or neighbor in history[full_type]:
                    continue
                history[full_type].add(neighbor)

                # in case the label is already the index of the label in the labels_map
                neighbor_color = self._gnx.node[neighbor]["label"]
                if neighbor_color in labels_map:
                    neighbor_color = labels_map[neighbor_color]
                self._features[node][full_type][neighbor_color] += 1

    def _get_feature(self, element):
        cur_feature = self._features[element]
        return np.array([[cur_feature[r_type][x] for x in range(self._num_classes)]
                         for r_type in self._relation_types]).flatten()


class UndirectedNthNeighborNodeHistogramCalculator(NeighborHistogramCalculator):
    def __init__(self, *args, **kwargs):
        super(UndirectedNthNeighborNodeHistogramCalculator, self).__init__(*args, **kwargs)
        counter = {i: 0 for i in range(self._num_classes)}
        self._neighbor_order = set(self._neighbor_order)
        self._print_name += "_%s" % ("-".join(map(str, self._neighbor_order)),)
        self._features = {node: {order: counter.copy() for order in self._neighbor_order} for node in self._gnx}

    def is_relevant(self):
        return not self._gnx.is_directed()

    def _calculate(self, include: set):
        # Translating each label to a relevant index to save memory

        labels_map = super(UndirectedNthNeighborNodeHistogramCalculator, self)._calculate(include)

        dists = unweighted.all_pairs_shortest_path_length(self._gnx, cutoff=max(self._neighbor_order))
        for i, (node, node_dists) in enumerate(dists):
            for neighbor, neigh_dist in node_dists.items():
                if node == neighbor or neigh_dist not in self._neighbor_order or neighbor not in include:
                    continue
                neighbor_color = self._gnx.node[neighbor]["label"]
                if neighbor_color in labels_map:
                    neighbor_color = labels_map[neighbor_color]
                self._features[node][neigh_dist][neighbor_color] += 1

    def _get_feature(self, element):
        # TODO: fix for several neighbor dists
        cur_feature = self._features[element]
        return np.array([cur_feature[x] for x in range(self._num_classes)])


def nth_neighbor_calculator(order, is_directed=True):
    if is_directed:
        return partial(DirectedNthNeighborNodeHistogramCalculator, order)
    return partial(UndirectedNthNeighborNodeHistogramCalculator, order)


feature_entry = {
    "first_neighbor_histogram": FeatureMeta(nth_neighbor_calculator(1), {"fnh", "first_neighbor"}),
    "second_neighbor_histogram": FeatureMeta(nth_neighbor_calculator(2), {"snh", "second_neighbor"}),
}


def build_sample_graph(edges, colors, color_list):
    dg = nx.DiGraph(labels=color_list)  # list(set(colors.values())))
    dg.add_edges_from(edges)
    for n in dg:
        dg.node[n]['label'] = colors[n]
    return dg


def test_neighbor_histogram():
    all_colors = ['red', 'blue', 'green', 'yellow']
    colors = {name: i for i, name in enumerate(all_colors)}
    node_colors = {x: all_colors[i % len(all_colors)] for i, x in enumerate(string.ascii_letters)}
    gnx = build_sample_graph([('a', 'b'), ('b', 'c'), ('a', 'd'), ('c', 'd'), ('e', 'f'), ('f', 'a')], node_colors,
                             all_colors)
    logger = PrintLogger()
    calc = NthNeighborNodeHistogramCalculator(2, gnx, logger=logger)
    calc.calculate()
    n = calc._to_ndarray()
    # (self, gnx, name, abbreviations, logger=None):
    # m = calculate_second_neighbor_vector(gnx, colors)
    print('bla')


if __name__ == "__main__":
    test_neighbor_histogram()
