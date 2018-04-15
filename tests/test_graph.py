import os
import pandas as pd
import networkx as nx


class TestData:
    def __init__(self):
        self._data_dir = "tests"
        df1 = pd.read_csv(os.path.join(self._data_dir, "test_undirected"))
        self._ugnx = nx.from_pandas_edgelist(df1, "n1", "n2", ["weight"], create_using=nx.Graph())

        df2 = pd.read_csv(os.path.join(self._data_dir, "test_directed"))
        self._gnx = nx.from_pandas_edgelist(df2, "n1", "n2", ["weight"], create_using=nx.DiGraph())

    def get_graph(self, is_directed):
        return self._gnx if is_directed else self._ugnx

    def load_feature(self, feature, is_directed):
        base_dir = os.path.join(self._data_dir, "%sdirected" % ("" if is_directed else "un"))

        df = pd.read_csv(os.path.join(base_dir, feature.print_name() + ".txt"), header=None)
        return {int(row[0]): list(row[1:]) for _, row in df.iterrows()}
