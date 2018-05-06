import os

import functools
import pandas as pd
import networkx as nx

from loggers import EmptyLogger


class TestData:
    def __init__(self, logger=None):
        if logger is None:
            logger = EmptyLogger()
        self._logger = logger
        self._data_dir = os.path.dirname(os.path.realpath(__file__))
        df1 = pd.read_csv(os.path.join(self._data_dir, "test_undirected"))
        self._ugnx = nx.from_pandas_edgelist(df1, "n1", "n2", ["weight"], create_using=nx.Graph())

        df2 = pd.read_csv(os.path.join(self._data_dir, "test_directed"))
        self._gnx = nx.from_pandas_edgelist(df2, "n1", "n2", ["weight"], create_using=nx.DiGraph())

    def get_graph(self, is_directed):
        return self._gnx if is_directed else self._ugnx

    @staticmethod
    def _specific_feature_processing(feature_name, res):
        if "motifs" in feature_name:
            for key, val in res.items():
                fixed = {i: int(x) for i, x in enumerate(val[1:])}
                fixed[None] = int(val[0])
                res[key] = fixed
        if feature_name in ["louvain"]:
            for key, val in res.items():
                res[key] = int(val)
        return res

    @staticmethod
    def feature_name(feature):
        if isinstance(feature, functools.partial):
            return feature.func.print_name(*feature.args, **feature.keywords)
        return feature.print_name()

    def load_feature(self, feature, is_directed):
        base_dir = os.path.join(self._data_dir, "%sdirected" % ("" if is_directed else "un"))
        feature_name = self.feature_name(feature)
        feature_path = os.path.join(base_dir, feature_name + ".txt")
        if not os.path.exists(feature_path):
            self._logger.info("Feature %s - %s doesn't exists" % (feature_name, "directed" if is_directed else "undirected"))
            return None
        df = pd.read_csv(feature_path, header=None)
        res = {int(row[0]): list(map(float, row[1:])) if df.shape[1] > 2 else float(row[1]) for _, row in df.iterrows()}
        return self._specific_feature_processing(feature_name, res)
