import json
import pandas as pd

from infomap import Infomap
from collections import defaultdict


class InfomapWrapper:

    def run(self, adj_matrix_path, edge_threshold, output_path=None):
        adj_matrix = self.load_adj_matrix(adj_matrix_path)
        infomap_obj = self.run_infomap(adj_matrix, edge_threshold)
        group_df = self.format_result(infomap_obj)
        if output_path is not None:
            group_df.to_csv(output_path, index=False)
        return group_df

    def load_adj_matrix(self, path: str, type_convert_func=float):
        with open(path, 'r', encoding='utf-8') as data:
            matrix = json.load(data)
        return matrix

    def run_infomap(self, adj_matrix, edge_threshold):
        infomap_obj = Infomap("--two-level")
        for user_1 in adj_matrix:
            for user_2 in adj_matrix[user_1]:
                if adj_matrix[user_1][user_2] > edge_threshold:
                    infomap_obj.add_link(user_1, user_2)
                    infomap_obj.add_link(user_2, user_1)
        infomap_obj.run()
        return infomap_obj

    def format_result(self, infomap_obj):
        group_df = {
            'node_id': [],
            'group_id': []
        }
        for node in infomap_obj.tree:
            if node.is_leaf:
                group_df['node_id'].append(node.node_id)
                group_df['group_id'].append(node.module_id)
        return group_df
