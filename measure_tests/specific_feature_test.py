import unittest

import logging
import networkx as nx

from loggers import PrintLogger, EmptyLogger
from measure_tests.test_graph import TestData

iterable_types = [list, tuple]
num_types = [int, float]


def compare_type(res1, res2):
    return (type(res1) == type(res2)) or \
           (type(res1) in iterable_types and type(res2) in iterable_types) or \
           (type(res1) in num_types and type(res2) in num_types)


def are_results_equal(res1, res2):
    if res1 == res2:
        return True
    if not compare_type(res1, res2):
        return False
    if type(res1) in num_types:
        ngidits = 5
        if round(res1, ngidits) != round(res2, ngidits):
            return False
    elif isinstance(res1, dict):
        if res1.keys() != res2.keys():
            return False
        for key, val1 in res1.items():
            if not are_results_equal(val1, res2[key]):
                return False
    elif type(res1) in iterable_types:
        if len(res1) != len(res2):
            return False
        for val1, val2 in zip(res1, res2):
            if not are_results_equal(val1, val2):
                return False
    else:
        assert False, "Unknown type"
    return True


def get_di_graph():
    gnx = nx.DiGraph()
    gnx.add_edges_from([(12, 1), (1, 12), (2, 3), (3, 4), (5, 2), (2, 6), (4, 7),
                        (4, 8), (9, 6), (7, 10), (11, 7), (10, 11), (10, 13), (10, 14),
                        (14, 10), (15, 12), (12, 16), (16, 12), (16, 15)])
    # gnx.add_edges_from([(1, 2), (2, 4), (3, 1), (3, 4)])
    return gnx


def get_graph():
    gnx = nx.Graph()
    gnx.add_edges_from([(1, 2), (2, 3), (3, 4), (3, 7), (4, 8), (5, 6), (7, 8),
                        (5, 10), (7, 10), (7, 11), (11, 12), (10, 13), (9, 14),
                        (11, 15), (15, 16)])
    return gnx


def filter_gnx(gnx, is_max_connected=False):
    if not is_max_connected:
        return gnx
    if gnx.is_directed():
        subgraphs = nx.weakly_connected_component_subgraphs(gnx)
    else:
        subgraphs = nx.connected_component_subgraphs(gnx)
    return max(subgraphs, key=len)


class SpecificFeatureTest(unittest.TestCase):
    logger = EmptyLogger()

    @classmethod
    def setUpClass(cls):
        cls._test_data = TestData(logger=cls.logger)

    def _test_feature(self, feature_cls, is_directed, is_max_connected=True):
        gnx = get_di_graph() if is_directed else get_graph()
        gnx = filter_gnx(gnx, is_max_connected)
        feature = feature_cls(gnx, logger=self.logger)
        res = feature.build()

        prev_res = self._test_data.load_feature(feature_cls, is_directed)
        if prev_res is not None or feature.is_relevant():
            self.assertTrue(are_results_equal(res, prev_res))


# def test_specific_feature(feature_cls):
#     self._test_feature(feature_cls, True)
#     self._test_feature(feature_cls, False)


if __name__ == '__main__':
    unittest.main()


# def _test_feature1(self, feature_cls, is_directed):
#     gnx = self._test_data.get_graph(is_directed=is_directed)
#     feature = feature_cls(gnx)
#     test_res = feature.build()
#     test_res = {item: [val] if not isinstance(val, list) else val for item, val in test_res.items()}
#
#     true_res = self._test_data.load_feature(feature_cls, is_directed=is_directed)
#     common = set(test_res).intersection(true_res)
#     for item in common:
#         for x, y in zip(test_res[item], true_res[item]):
#             self.assertAlmostEqual(x, y, 5)
#
#     test_diff = set(test_res).difference(true_res)
#     true_diff = set(true_res).difference(test_res)
