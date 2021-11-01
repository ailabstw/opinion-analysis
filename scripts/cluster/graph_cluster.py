import numpy as np
import networkx as nx
import scipy.sparse as sp

from collections import deque, defaultdict
from itertools import chain
from scipy.sparse import csr_matrix
from sklearn.metrics.pairwise import cosine_similarity
from typing import Dict, List, Iterable


class GraphCluster:

    def clustering(self,
                   content_embs: List[List],
                   sim_threshold: float,
                   coverage_threshold: float):

        N = len(content_embs)
        ids = [i for i in range(N)]
        sim = cosine_similarity(content_embs)
        R = (sim > sim_threshold).astype(np.float)
        R = csr_matrix(R)

        # merge relevant nodes.
        for thres in [0.99, coverage_threshold, 0.99, 0.99]:
            R = self._merge(R, thres)
            edge_num = np.sum(R)
            if edge_num == N * N:
                raise CompletedGraphError()

        # assign each node to the largest cluster.
        cluster_list = [[j for j in R[i].nonzero()[1]] for i in range(N)]
        node_cluster_dict = defaultdict(set)
        for cid, cluster in enumerate(cluster_list):
            for j in cluster:
                node_cluster_dict[j].add(cid)
        hard_labeling_result = {i: max(node_cluster_dict[i], key=lambda cid: len(
            cluster_list[cid])) for i in range(N)}
        cluster_dict = defaultdict(list)
        for i, cid in hard_labeling_result.items():
            cluster_dict[cid].append(i)
        ret = sorted(cluster_dict.values(), key=len, reverse=True)

        # ref to ids
        ret = [[ids[i] for i in sorted(cluster)] for cluster in ret]
        return ret

    def _merge(self, R, coverage_threshold):

        N = R.shape[0]
        coverage = R.dot(R.T) / np.sum(R, axis=1)
        graph = {src: set() for src in range(N)}
        for src in range(N):
            for dst in (coverage[src, :] > coverage_threshold).nonzero()[1]:
                graph[src].add(dst)
                graph[dst].add(src)
        graph = {k: list(sorted(v)) for k, v in graph.items()}
        U = []
        path_list = []
        merged = set()
        for src in range(N):
            if src not in merged:
                path = self._bfs(graph, src)
                u = csr_matrix(np.clip(np.sum(R[path, :], axis=0), 0, 1))
                path_list.append(path)
                U.append(u)
                merged = set.union(merged, set(path))

        u_idx = list(chain(*[[i] * len(path)
                     for i, path in enumerate(path_list)]))
        sorted_idx = [u_idx[i] for i in np.argsort(list(chain(*path_list)))]
        X = sp.vstack(U)
        ret = csr_matrix(X[sorted_idx, :])
        return ret

    def _bfs(self, graph, vertex):
        path = set()
        path.add(vertex)
        q = deque()
        q.append(vertex)
        while len(q) > 0:
            v = q.popleft()
            for w in graph[v]:
                if w not in path:
                    path.add(w)
                    q.append(w)
        return list(path)


class GraphMerger:

    def merge(self, group_to_neigbhors: Dict[str, List]):
        graph = nx.Graph()
        for group, neighbors in group_to_neigbhors.items():
            for neighbor in neighbors:
                graph.add_edge(group, neighbor)
                graph.add_edge(neighbor, group)

        cliques = [c for c in self.find_cliques(graph)]
        return cliques

    def find_clique_cover(self, cliques):
        cliques = sorted(cliques, key=lambda v: len(v), reverse=True)

        duplicated = set()
        cliques_cover = []

        for clique in cliques:
            sub_component = []
            for node in clique:
                if node not in duplicated:
                    duplicated.add(node)
                    sub_component.append(node)
            if sub_component:
                cliques_cover.append(sub_component)
        return cliques_cover


class CompletedGraphError(Exception):
    pass
