import os
import pickle

import numpy as np

from tqdm import tqdm
from collections import defaultdict
from typing import List, Dict, Optional
from graphflow.logger import get_logger


class GraphBuilder(object):

    def __init__(self):
        self.logger = get_logger("GraphFlow")
        self.corr_matrix = defaultdict(dict)
        self.coef_matrix = defaultdict(dict)
        self.graph = defaultdict(dict)
        self.num_articles = 0
        self.user_article_nums = defaultdict(int)

    def build_graph(self, edge_threshold: float):
        dropped_node = []

        for user_1 in self.coef_matrix:
            valid_neighbors = defaultdict(dict)
            for user_2 in self.coef_matrix[user_1]:
                corr = self.coef_matrix[user_1][user_2]
                if corr > edge_threshold:
                    valid_neighbors[user_2] = corr
            if len(valid_neighbors):
                self.graph[user_1] = valid_neighbors
            else:
                dropped_node.append(user_1)
        self.logger.info(
            "[build_graph] # dropped nodes: {}".format(len(dropped_node)))
        return self.graph, dropped_node

    def build_corr_matrix(self, post_to_users: Dict[str, List[str]],
                              valid_users: Optional[set] = None):
        """Constuct a co-occurrence matrix of the given users.

        Args:
            post_to_users (Dict[str, List[str]]):
                - key: ptt_post_id
                - value: list of users who comment under the corresponding post.
            valid_users (Optional[set], optional):
                a whitelist of usernames. if valid_users is given, we would only build the co-occurrence matrix for user in valid_users.
        """
        self.num_articles = len(post_to_users)
        for post_id, users in tqdm(post_to_users.items()):
            if valid_users is not None:
                users = [u for u in users if u in valid_users]
            users = list(set(users))

            for u in users:
                self.user_article_nums[u] += 1

            # build pairwise co-occourance counting
            for i in range(len(users)):
                for j in range(i+1, len(users)):
                    if users[j] not in self.corr_matrix[users[i]]:
                        self.corr_matrix[users[i]][users[j]] = 0
                    if users[i] not in self.corr_matrix[users[j]]:
                        self.corr_matrix[users[j]][users[i]] = 0

                    self.corr_matrix[users[i]][users[j]] += 1
                    self.corr_matrix[users[j]][users[i]] += 1

    def calculate_pairwise_correlation(self):
        self.logger.info("Building coefficient matrix.")
        for node_i in tqdm(self.corr_matrix):
            for node_j in self.corr_matrix[node_i]:
                coef = self.calculcate_node_correlation(node_i, node_j)
                self.coef_matrix[node_i][node_j] = coef
                self.coef_matrix[node_j][node_i] = coef
        return self.coef_matrix

    def calculcate_node_correlation(self, node_i, node_j):
        """The calculation of Phi-coefficient"""
        node_i_count = self.user_article_nums[node_i]
        node_j_count = self.user_article_nums[node_j]
        all_count = self.num_articles

        i_j_count = self.corr_matrix[node_i][node_j]
        i_nj_count = node_i_count - i_j_count
        ni_j_count = node_j_count - i_j_count
        ni_nj_count = all_count - node_i_count - node_j_count + i_j_count

        fraction = ((i_j_count * ni_nj_count) - (i_nj_count * ni_j_count))
        denominator = np.sqrt(node_i_count * node_j_count *
                              (ni_nj_count + ni_j_count) * (ni_nj_count + i_nj_count))
        coef = fraction / denominator
        return coef
