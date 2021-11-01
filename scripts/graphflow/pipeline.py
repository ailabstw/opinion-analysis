import os
import pickle

from tqdm import tqdm
from datetime import datetime, timedelta
from collections import defaultdict

from graphflow.database import DataHandler
from graphflow.graph import GraphBuilder
from graphflow.data_wrapper import CorrAnalysisPipelineOutput
from graphflow.logger import get_logger


class CorrAnalysisPipeline:

    def __init__(self):
        self.logger = get_logger(name='CorrAnalysis')

    def run(self, post_to_users, min_comments_num=10):
        valid_users = self.get_valid_users(post_to_users, min_comments_num)
        self.logger.info(f"# valid users: {len(valid_users)}")

        graph_builder = GraphBuilder()
        self.logger.info("Building the Corr Matrix.")
        graph_builder.build_corr_matrix(post_to_users,
                                        valid_users=valid_users)

        self.logger.info("Building the Coef Matrix.")
        graph_builder.calculate_pairwise_correlation()

        result = CorrAnalysisPipelineOutput(
            graph_builder.corr_matrix,
            graph_builder.coef_matrix
        )
        return result

    def get_valid_users(self, post_to_users, min_comments_num=10):
        # filter out the users who post less than `min_comments_num` comments.
        user_comment_ctr = defaultdict(int)
        for post_id, users in post_to_users.items():
            users = list(set(users))
            for user in users:
                user_comment_ctr[user] += 1
        valid_users = {user for user, count in user_comment_ctr.items()
                       if count >= min_comments_num}
        return valid_users
