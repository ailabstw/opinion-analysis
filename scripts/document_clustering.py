import json
import argparse
import pandas as pd
from typing import List
from cluster.graph_cluster import GraphCluster
from nlp.encoder import USEEncoder


def prepare_data(data_path: str):
    with open(data_path, 'r', encoding='utf-8') as data:
        articles = json.load(data)
        texts = [v['Content'] for v in articles]
    return texts

def texts_to_embeddings(texts: List[str]):
    encoder = USEEncoder()
    text_embeddings = encoder.encode(texts)
    return text_embeddings


def text_clustering(text_embeddings):
    graph_cluster = GraphCluster()
    clusters = graph_cluster.clustering(text_embeddings, 0.825, 0.7915)
    return clusters


def output_result(texts: List[str], clusters: List, output_path: str):
    cluster_df = {
        'text': [],
        'cluster': [],
    }

    for group_id, group in enumerate(clusters):
        for idx in group:
            cluster_df['text'].append(texts[idx])
            cluster_df['cluster'].append(group_id)
            
    cluster_df = pd.DataFrame(cluster_df)
    print(f"The clusering result is output to {output_path}")
    cluster_df.to_csv(output_path, index=False)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--dataset", type=str, default='toy_dataset/news.json', help="the path to dataset")
    parser.add_argument(
        "--output_path", type=str, default='outputs/news_cluster.csv', help="the output path for clustering result")

    args = parser.parse_args()
    
    texts = prepare_data(args.dataset)
    text_embeddings = texts_to_embeddings(texts)
    clusters = text_clustering(text_embeddings)
    output_result(texts, clusters, args.output_path)
