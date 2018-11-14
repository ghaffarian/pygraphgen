# PyGraphGen

***A Synthetic Graph Dataset Generator in Python.***

This tool is intended to generate synthetic graph-datasets to test frequent-subgraph-mining (FSM) implementations. The input parameters are designed similar to the dataset parameter settings described in the following paper:

 - Kuramochi and Karypis. "Frequent Subgraph Discovery." In Proceedings of IEEE International Conference on Data Mining (ICDM), pp. 313-320. IEEE, 2001.


## License

This software is licensed under the terms of the GPL-v3.0 license. Read the license to understand what it means.


## Requirements

 - Python-v3.4+
 - Numpy-v1.8+
 - Scipy-v0.13+


## Usage Guide

```
$ python3 graphgen.py -H

USAGE:
   python3 graphgen.py [OPTIONS]

OPTIONS:
   -H:  print this HELP message;
   -O:  specify output directory path;
   -S:  specify min-support ratio for frequent patterns (subgraphs);
   -D:  specify number of graphs in the dataset;
   -L:  specify number of distinct frequent patterns (subgraphs);
   -E:  specify number of distinct edge labels;
   -V:  specify number of distinct vertex labels;
   -T:  specify average size of each graph (# of edges);
   -I:  specify average size of frequent subgraphs (# of edges);
   -P:  specify to allow loop edges in graphs;
   -U:  specify graphs as undirected;

```


## Examples

The generated dataset in the following examples is written in the `graph-dataset` directory. In this directory, there will be another directory named `frequent-patterns` and several files with `.dot` extension. The `dot` files are the individual graphs of the dataset. The `frequent-patterns` directory also includes some `dot` files which are the generated frequent patterns inserted in various graphs of the dataset.

**Example-1: No Options (Default Parameters)**
```
$ python3 graphgen.py 

NO ARGS! Working with default parameters:

OUTPUT_DIR ...... = graph-dataset/
MIN_SUPPORT ..... = 0.10
DATASET_LEN ..... = 40
FREQUENTS_LEN ... = 4
EDGE_LABELS_LEN . = 2
VERTEX_LABELS_LEN = 8
AVRG_GRAPH_SIZE . = 9
AVRG_FRQNT_SIZE . = 4
IS_DIRECTED ..... = True
ALLOW_LOOPS ..... = False 

Pattern-#1 with 3 edges and support of 10.3%
inserted in 4 graphs : [2, 20, 24, 34] 

Pattern-#2 with 4 edges and support of 19.0%
inserted in 8 graphs : [9, 11, 12, 17, 25, 27, 29, 40] 

Pattern-#3 with 4 edges and support of 14.0%
inserted in 6 graphs : [1, 4, 19, 24, 26, 38] 

Pattern-#4 with 6 edges and support of 14.6%
inserted in 6 graphs : [1, 21, 24, 28, 37, 38] 

The following 20 graphs include at least one pattern:
[1, 2, 4, 9, 11, 12, 17, 19, 20, 21, 24, 25, 26, 27, 28, 29, 34, 37, 38, 40] 

Writing patterns to output files ...
Writing graph-dataset to output files ...
All done.
```

**Example-2: Larger Dataset of Undirected Graphs**
```
$ python3 graphgen.py  -S 0.2  -D 500  -L 12  -E 4  -V 12  -U

OUTPUT_DIR ...... = graph-dataset/
MIN_SUPPORT ..... = 0.20
DATASET_LEN ..... = 500
FREQUENTS_LEN ... = 12
EDGE_LABELS_LEN . = 4
VERTEX_LABELS_LEN = 12
AVRG_GRAPH_SIZE . = 9
AVRG_FRQNT_SIZE . = 4
IS_DIRECTED ..... = False
ALLOW_LOOPS ..... = False 

< --snip-- >
```
