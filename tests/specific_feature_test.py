import unittest

from tests.test_graph import TestData


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


def test_specific_feature(feature_cls):
    pass


if __name__ == '__main__':
    unittest.main()
