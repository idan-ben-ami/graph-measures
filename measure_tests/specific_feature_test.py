import unittest

import networkx as nx

from measure_tests.test_graph import TestData


class SpecificFeatureTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls._test_data = TestData()

    def _test_feature(self, feature_cls, is_directed):
        gnx = self._test_data.get_graph(is_directed=is_directed)
        feature = feature_cls(gnx)
        test_res = feature.build()
        test_res = {item: [val] if not isinstance(val, list) else val for item, val in test_res.items()}

        true_res = self._test_data.load_feature(feature_cls, is_directed=is_directed)
        common = set(test_res).intersection(true_res)
        for item in common:
            for x, y in zip(test_res[item], true_res[item]):
                self.assertAlmostEqual(x, y, 5)

        test_diff = set(test_res).difference(true_res)
        true_diff = set(true_res).difference(test_res)

        # for i in range(1, 17):
        #     tst = "miss"
        #     tru = "miss"
        #     if str(i) in test_res:
        #         tst = test_res[str(i)]
        #     if str(i) in true_result:
        #         tru = true_result[str(i)]
        #     print("node " + str(i) + "\ttrue: " + str(tru) + "\t||\ttest: " + str(tst) + "\n")


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


def calculate_test_feature(calculator, is_max_connected=False):
    from loggers import PrintLogger
    logger = PrintLogger("TestLogger")
    res = {}
    for g_type, gnx in [("directed", get_di_graph()), ("undirected", get_graph())]:
        gnx = filter_gnx(gnx, is_max_connected)
        feat = calculator(gnx, logger=logger)
        res[g_type] = feat.build()
    return res


def are_results_equal(res1, res2):
    if type(res1) != type(res2):
        return False
    if res1 == res2:
        return True
    if isinstance(res1, float) or isinstance(res1, int):
        ngidits = 5
        if round(res1, ngidits) != round(res2, ngidits):
            return False
    elif isinstance(res1, dict):
        if res1.keys() != res2.keys():
            return False
        for key, val1 in res1.items():
            if not are_results_equal(val1, res2[key]):
                return False
    elif isinstance(res1, list) or isinstance(res1, tuple):
        if len(res1) != len(res2):
            return False
        for val1, val2 in zip(res1, res2):
            if not are_results_equal(val1, val2):
                return False
    else:
        assert False, "Unknown type"

    return True


def test_specific_feature(feature_cls, is_max_connected=False):
    res = calculate_test_feature(feature_cls, is_max_connected=is_max_connected)
    test_data = TestData()
    prev_res = {g_type: test_data.load_feature(feature_cls, g_type == "directed")
                for g_type in ["directed", "undirected"]}
    if prev_res["directed"] is not None:
        directed_equal = are_results_equal(res['directed'], prev_res['directed'])
        print("Directed graph are %sequal" % ("" if directed_equal else "not "))
    if prev_res["undirected"] is not None:
        undirected_equal = are_results_equal(res['undirected'], prev_res['undirected'])
        print("UnDirected graph are %sequal" % ("" if undirected_equal else "not "))
    # if directed_equal and undirected_equal:
    #     print(" *** Both directed and undirected are equal! *** ")
    print("Finished")


if __name__ == '__main__':
    unittest.main()
