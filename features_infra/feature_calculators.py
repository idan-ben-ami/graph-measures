import re
from itertools import chain

import numpy as np
from scipy import sparse
from datetime import datetime

from loggers import EmptyLogger
from collections import namedtuple


def time_log(func):
    def wrapper(self, *args, **kwargs):
        start_time = datetime.now()
        self._logger.debug("Start %s at %s" % (self._print_name, start_time,))
        res = func(self, *args, **kwargs)
        cur_time = datetime.now()
        self._logger.debug("Finish %s at %s" % (self._print_name, cur_time - start_time,))
        self._is_loaded = True  # Very bad place to put it - choose somewhere else
        return res

    return wrapper


class FeatureCalculator:
    def __init__(self, gnx, logger=None):
        # super(FeatureCalculator, self).__init__()
        self._is_loaded = False
        self._features = {}
        # self._abbr_set = abbr_set
        self._logger = EmptyLogger() if logger is None else logger
        self._gnx = gnx
        self._print_name = self._get_print_name()

    is_loaded = property(lambda self: self._is_loaded, None, None, "Whether the features were calculated")

    def is_relevant(self):
        raise NotImplementedError()

    def clean(self):
        self._gnx = None
        self._logger = None

    def _get_print_name(self):
        split_name = re.findall("[A-Z][^A-Z]*", type(self).__name__)
        if "calculator" == split_name[-1].lower():
            split_name = split_name[:-1]
        return "_".join(map(lambda x: x.lower(), split_name))

    @time_log
    def build(self, include: set = None):
        # Don't calculate it!
        if not self.is_relevant():
            self._is_loaded = True
            return

        if include is None:
            include = set()
        self._calculate(include)
        self._is_loaded = True

    def _calculate(self, include):
        raise NotImplementedError()

    def _get_feature(self, element):
        raise NotImplementedError()

    def _params_order(self, input_order: list = None):
        raise NotImplementedError()

    def sparse_matrix(self, params_order: list = None):
        mx = np.matrix([self._get_feature(element) for element in self._params_order(params_order)]).astype(np.float32)
        return sparse.csr_matrix(mx)

    # def __getattr__(self, item):
    #     if item in self._features:
    #         return self._features[item]
    #     return self.__getattribute__(item)

    def __repr__(self):
        status = "loaded" if self.is_loaded else "not loaded"
        if not self.is_relevant():
            status = "irrelevant"
        return "<Feature %s: %s>" % (self._print_name, status,)


# TODO: Think how to access node & edge from features. assume node/edge can be a more complicated objects

# noinspection PyAbstractClass
class NodeFeatureCalculator(FeatureCalculator):
    # def __init__(self, *args, **kwargs):
    #     super(NodeFeatureCalculator, self).__init__(*args, **kwargs)
    #     self._features = {str(node): None for node in self._gnx}

    def _params_order(self, input_order: list = None):
        if input_order is None:
            return sorted(self._gnx)
        return input_order

    def _get_feature(self, element) -> np.ndarray:
        return np.array(self._features[element])

    def edge_based_node_feature(self):
        nodes_dict = self._features
        edge_dict = {}
        for edge in self._gnx.edges():
            n1_val = np.array(nodes_dict[edge[0]])
            n2_val = np.array(nodes_dict[edge[1]])

            edge_dict[edge] = list(chain(*zip(n1_val - n2_val, np.mean([n1_val, n2_val], axis=0))))
        return edge_dict

    def feature(self, element):
        return self._get_feature(element)


# noinspection PyAbstractClass
class EdgeFeatureCalculator(FeatureCalculator):
    # def __init__(self, *args, **kwargs):
    #     super(EdgeFeatureCalculator, self).__init__(*args, **kwargs)
    #     self._features = {str(edge): None for edge in self._gnx.edges()}

    def _params_order(self, input_order: list = None):
        if input_order is None:
            return sorted(self._gnx.edges())
        return input_order

    def _get_feature(self, element) -> np.ndarray:
        return np.array(self._features[element])


# class AttractorBasinCalculator(NodeFeatureCalculator):
#     @time_log
#     def calculate(self):
#         # TODO
#         for node in self._gnx:
#             self._calculae_node_feature(node)


FeatureMeta = namedtuple("FeatureMeta", ("calculator", "abbr_set"))
