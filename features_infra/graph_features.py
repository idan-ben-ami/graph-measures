import os
import pickle

from multiprocessing import Process, Queue

from loggers import PrintLogger, EmptyLogger

import networkx as nx
import numpy as np
from scipy import sparse
from operator import itemgetter as at


class Worker(Process):
    def __init__(self, queue, calculators, include, logger=None):
        super(Worker, self).__init__()
        if logger is None:
            logger = EmptyLogger()

        self._queue = queue
        self._calculators = calculators
        self._logger = logger
        self._include = include

    def run(self):
        self._logger.info('Worker started')
        # do some initialization here

        self._logger.info('Computing things!')
        for feature_name in iter(self._queue.get, None):
            self._calculators[feature_name].build(include=self._include)


# object that calculates & holds a list of features of a graph.
class GraphFeatures(dict):
    def __init__(self, gnx, features, dir_path=".", logger=None):
        self._gnx = gnx
        self._base_dir = dir_path
        self._logger = EmptyLogger() if logger is None else logger
        self._matrix = None

        self._abbreviations = {abbr: name for name, meta in features.items() for abbr in meta.abbr_set}

        # building the feature calculators data structure
        super(GraphFeatures, self).__init__({name: meta.calculator(gnx, logger=logger)
                                             for name, meta in features.items()})
        #  if meta.abbr_set.union({name}).intersection(features)})

    def _build_serially(self, include, force_build: bool = False):
        for name, feature in self.items():
            if force_build or not os.path.exists(self._feature_path(name)):
                feature.build(include=include)
            else:
                self._load_feature(name)
                # obj = pickle.load(open(file_path, "rb"))
                # obj.logger = self._logger
                # self[name] = obj

    # a single process means it is calculated serially
    def build(self, num_processes: int = 1, include: set = None):  # , exclude: set=None):
        # if exclude is None:
        #     exclude = set()
        if include is None:
            include = set()

        if 1 == num_processes:
            return self._build_serially(include)

        request_queue = Queue()
        workers = [Worker(request_queue, self, include, logger=self._logger) for _ in range(num_processes)]
        # Starting all workers
        for worker in workers:
            worker.start()

        # Feeding the queue with all the features
        for feature_name in self:
            request_queue.put(feature_name)

        # Sentinel objects to allow clean shutdown: 1 per worker.
        for _ in range(num_processes):
            request_queue.put(None)

        # Joining all workers
        for worker in workers:
            worker.join()

    def _load_feature(self, name):
        obj = pickle.load(open(self._feature_path(name), "rb"))
        obj.logger = self._logger
        self[name] = obj
        return self[name]

    def __getattr__(self, name):
        if name not in self:
            if name in self._abbreviations:
                name = self._abbreviations[name]
            else:
                return super(GraphFeatures, self).__getattribute__(name)

        # if obj is already calculated - return it
        obj = self[name]
        if obj.is_loaded:
            return obj

        # if obj is not calculated, check if it exist on the file system
        # if it doesn't - calculate it, if it does - load it and return it
        if not os.path.exists(self._feature_path(name)):
            obj.build()
            return obj

        return self._load_feature(name)

    @property
    def features(self):
        return set(self)

    def _feature_path(self, name, dir_path=None):
        if dir_path is None:
            dir_path = self._base_dir
        return os.path.join(dir_path, name + ".pkl")

    def dump(self, dir_path=None):
        if dir_path is None:
            dir_path = self._base_dir

        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

        for name, feature in self.items():
            if not feature.is_loaded:
                continue
            feature.clean()  # in order not to save unnecessary data
            pickle.dump(feature, open(self._feature_path(name, dir_path), "wb"))

    # Should be implemented by request (_matrix is a cache)
    # def to_matrix(self):
    #     raise NotImplementedError()

    def sparse_matrix(self, entries_order: list=None, add_ones=False, dtype=None):
        if self._matrix is not None:
            return self._matrix

        if entries_order is None:
            entries_order = sorted(self._gnx)

        # Consider caching the matrix creation (if it takes long time)
        sorted_features = map(at(1), sorted(self.items(), key=at(0)))
        # matrix = np.concatenate([feature.sparse_matrix() for feature in sorted_features], axis=1)  # 0: below, 1: near
        mx = sparse.hstack([feature.sparse_matrix(entries_order) for feature in sorted_features], dtype=dtype)
        if add_ones:
            mx = sparse.hstack([mx, np.ones((mx.shape[0], 1))], dtype=dtype)
        self._matrix = mx
        return mx
        # return sparse.csr_matrix(matrix, dtype=np.float32)


# class GraphNodeFeatures(GraphFeatures):
#     def sparse_matrix(self, entries_order: list=None, **kwargs):
#         if entries_order is None:
#             entries_order = sorted(self._gnx)
#         return super(GraphNodeFeatures, self).sparse_matrix(entries_order=entries_order, **kwargs)
#
#
# class GraphEdgeFeatures(GraphFeatures):
#     def sparse_matrix(self, entries_order: list=None, **kwargs):
#         if entries_order is None:
#             entries_order = sorted(self._gnx.edges())
#         return super(GraphEdgeFeatures, self).sparse_matrix(entries_order=entries_order, **kwargs)


if __name__ == "__main__":
    from feature_meta import ALL_FEATURES

    ftrs = GraphFeatures(nx.DiGraph(), ALL_FEATURES)
    print("Bla")
