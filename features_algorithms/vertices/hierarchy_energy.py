import numpy as np
from features_infra.feature_calculators import NodeFeatureCalculator, FeatureMeta


class HierarchyEnergyCalculator(NodeFeatureCalculator):
    def is_relevant(self):
        return True

    def _calculate(self, include: set):
        pass

    def hierarchy_energy(self):
        hierarchy_energy_list, vet_index = self._calculate_hierarchy_energy_index()
        self._features = dict(zip(vet_index, hierarchy_energy_list))

    def _calculate_hierarchy_energy_index(self):
        vet_index, g = self._build_graph_matrix()
        l, y, tol, r, d = self._initialize_vars_from_laplacian_matrix(g)
    # calculation of hierarchy Energy
        while np.linalg.norm(r) > tol:
            gamma = np.dot(r.T, r)
            alpha = np.divide(gamma, np.dot(d.T, np.dot(l, d)))
            y = np.add(y, alpha*d)
            r = np.subtract(r, alpha*np.dot(l, d))
            beta = np.divide((np.dot(r.T, r)), gamma)
            d = np.add(r, beta*d)
        else:
            return y, vet_index

    def _build_graph_matrix(self):
        a = []
        vet_index = self._gnx.nodes()
        for i in vet_index:
            temp = []
            for j in self._gnx:
                if self._gnx.has_edge(i,j):
                    temp.append(1)
                else:
                    temp.append(0)
            a.append(temp)
        graph_matrix = np.squeeze(a)
        return vet_index, graph_matrix

    def _initialize_vars_from_laplacian_matrix(self, g):
        # creating laplacian matrix
        w = g+g.T
        d = np.diag(sum(w))
        l = d - w
        id = (np.sum(g, 0))
        od = (np.sum(g, 1))
        # initialize_vars
        b = np.subtract((np.array([od])).T, (np.array([id])).T)
        tol = 0.001
        n = np.size(g, 1)
        y = np.random.rand(n, 1)
        y = np.subtract(y, (1 / n) * sum(y))
        k = np.dot(l, y)
        r = np.subtract(b, k)
        d = r
        return l, y, tol, r, d


feature_entry = {
    "hierarchy_energy": FeatureMeta(HierarchyEnergyCalculator, {"hierarchy"}),
}

if __name__ == "__main__":
    pass
