import json
import argparse
from cluster.community_detection import InfomapWrapper


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--coef_matrix_path", type=str, default='outputs/coef_matrix.json', help="the path to coef_matrix")
    parser.add_argument(
        "--edge_threshold", type=float, default=0.05, help="the threshold for user similarity")
    parser.add_argument(
        "--output_path", type=str, default='user_group.csv', help="the path to output_csv")

    args = parser.parse_args()

    infomap_wrapper = InfomapWrapper()
    result = infomap_wrapper.run(args.coef_matrix_path, args.edge_threshold)
    result.to_csv(args.output_path, index=False)
    
