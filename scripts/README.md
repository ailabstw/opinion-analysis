# Public Opinion Analysis

This repository contains a set of tools we used for public opinion analysis, espeically for the following three tasks:

1. Document Clustering: given a list of documents, we would gather the documents with relevant topics to the same group.
2. Co-occurene Matrix Construction: given a list of users who have commented to the same post, we would determine the phi-coefficient for each user pair and build it as a co-occurene matrix.
3. Community Detection: given a social network, we would partition the network to several nonoverlapping components.

## Examples

To demostarte how to use the tools, we release a [toy-dataset](https://drive.google.com/file/d/1YGCrWOFRoq_fJ7mndOYBO8NXtTJCFGv3/view?usp=sharing) which consists of news-related posts sampled from PTT Gossiping Board, 2021. If you want to adapt the tool on your own dataset, feel free to update the function `prepare_data` or implement a custom data interface.

### Document Clustering

```
python document_clustering.py --dataset path_to_toy_dataset --output_path path_to_output_file
```

### Co-occurrence Matrix Construction

```
python build_matrix.py --dataset path_to_toy_dataset --output_path path_to_output_file
```

### Community Detection

```
python user_grouping.py --coef_matrix_path path_to_coef_matrix --output_path path_to_output_file
```
