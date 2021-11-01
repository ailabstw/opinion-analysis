import json
import argparse
from typing import List
from graphflow.pipeline import CorrAnalysisPipeline


def prepare_data(data_path: str):
    with open(data_path, 'r', encoding='utf-8') as data:
        posts = json.load(data)
        post_to_users = {}
        for post in posts:
            if len(post['Responses']) != 0:
                users = [r['User'] for r in post['Responses']]
                post_id = post['Article_id']
                post_to_users[post_id] = users
    return post_to_users

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--dataset", type=str, default='toy_dataset/ptt_samples.json', help="the path to dataset")
    parser.add_argument(
        "--output_path", type=str, default='outputs/coef_matrix.json', help="the output path for coef_matrix")

    args = parser.parse_args()

    # perpare the user list
    post_to_users = prepare_data(args.dataset)
    
    # construct the corr_matrix and phi_coef_matrix
    corr_analysis_pipeline = CorrAnalysisPipeline()
    result = corr_analysis_pipeline.run(post_to_users, min_comments_num=3)
    
    # dump the result
    with open(args.output_path, "w", encoding='utf-8') as out:
        json.dump(result.coef_matrix, out)
    
