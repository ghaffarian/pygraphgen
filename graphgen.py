""" ### In The Name of Allah ###

PyGraphGen: A Synthetic Graph Dataset Generator in Python

This program inputs some general parameters about the desired dataset
and generates a synthetic graph dataset using the DOT graph format.

Vertices are strings (the vertex-label).

Edge-labels are also strings, but edges are tuples: e = (v_src, e_lbl, v_dst)

Graphs are dictionaries with vertices as keys and set of edges as values:
g = {v1: {(v1, e1, v2)},
     v2: {(v2, e2, v3), (v2, e3, v4)},
     v3: {(v3, e4, v1)},
     v4: {(v4, e5, v1)}}
"""
import os
import sys
import random
from scipy.misc import comb  # scipy.special
from numpy.random import normal

# Program variables
OUTPUT_DIR        = 'graph-dataset/'
MIN_SUPPORT       = 0.1
DATASET_LEN       = 40
FREQUENTS_LEN     = 4
EDGE_LABELS_LEN   = 2
VERTEX_LABELS_LEN = 8
AVRG_GRAPH_SIZE   = 9
AVRG_FRQNT_SIZE   = 4
IS_DIRECTED       = True
ALLOW_LOOPS       = False


def print_help_exit(invalid_arg=None):
    """Print help information about program usage and options, then exit."""
    if invalid_arg is not None:
        print('INVALID ARGUMENT: ' + invalid_arg)
    print('\nUSAGE:\n   python3 graphgen.py [OPTIONS]\n')
    print('OPTIONS:')
    print('   -H:  print this HELP message;')
    print('   -O:  specify output directory path;')
    print('   -S:  specify min-support ratio for frequent patterns (subgraphs);')
    print('   -D:  specify number of graphs in the dataset;')
    print('   -L:  specify number of distinct frequent patterns (subgraphs);')
    print('   -E:  specify number of distinct edge labels;')
    print('   -V:  specify number of distinct vertex labels;')
    print('   -T:  specify average size of each graph (# of edges);')
    print('   -I:  specify average size of frequent subgraphs (# of edges);')
    print('   -P:  specify to allow loop edges in graphs;')
    print('   -U:  specify graphs as undirected;\n')
    sys.exit(0)


def parse_args():
    """Parse arguments to assign program parameters."""
    global OUTPUT_DIR
    global MIN_SUPPORT
    global DATASET_LEN
    global FREQUENTS_LEN
    global EDGE_LABELS_LEN
    global VERTEX_LABELS_LEN
    global AVRG_GRAPH_SIZE
    global AVRG_FRQNT_SIZE
    global IS_DIRECTED
    global ALLOW_LOOPS
    argc = len(sys.argv)
    if argc > 1:
        idx = 1
        while idx < argc:
            if sys.argv[idx].upper() == '-H':
                print_help_exit()
            elif sys.argv[idx].upper() == '-O':
                idx += 1
                if idx == argc:
                    print_help_exit()
                OUTPUT_DIR = sys.argv[idx]
                if not OUTPUT_DIR.endswith('/'):
                    OUTPUT_DIR += '/'
            elif sys.argv[idx].upper() == '-S':
                idx += 1
                if idx == argc:
                    print_help_exit()
                MIN_SUPPORT = float(sys.argv[idx])
            elif sys.argv[idx].upper() == '-D':
                idx += 1
                if idx == argc:
                    print_help_exit()
                DATASET_LEN = int(sys.argv[idx])
            elif sys.argv[idx].upper() == '-L':
                idx += 1
                if idx == argc:
                    print_help_exit()
                FREQUENTS_LEN = int(sys.argv[idx])
            elif sys.argv[idx].upper() == '-E':
                idx += 1
                if idx == argc:
                    print_help_exit()
                EDGE_LABELS_LEN = int(sys.argv[idx])
            elif sys.argv[idx].upper() == '-V':
                idx += 1
                if idx == argc:
                    print_help_exit()
                VERTEX_LABELS_LEN = int(sys.argv[idx])
            elif sys.argv[idx].upper() == '-T':
                idx += 1
                if idx == argc:
                    print_help_exit()
                AVRG_GRAPH_SIZE = int(sys.argv[idx])
            elif sys.argv[idx].upper() == '-I':
                idx += 1
                if idx == argc:
                    print_help_exit()
                AVRG_FRQNT_SIZE = int(sys.argv[idx])
            elif sys.argv[idx].upper() == '-U':
                IS_DIRECTED = False
            elif sys.argv[idx].upper() == '-P':
                ALLOW_LOOPS = True
            else:
                print_help_exit(sys.argv[idx])
            idx += 1
    else:
        print('NO ARGS! Working with default parameters:\n')


def validate_params():
    """Validate program parameters.
    If any error is found, a suitable message is printed and program aborts.
    """
    error = False
    if EDGE_LABELS_LEN < 1 or EDGE_LABELS_LEN > 99:
        error = True
        print('ERROR: Number of edge-labels must be in the range: [1 .. 99]')
    if VERTEX_LABELS_LEN < 2 or VERTEX_LABELS_LEN > 999:
        error = True
        print('ERROR: Number of vertex-labels must be in the range: [2 .. 999]')
    if VERTEX_LABELS_LEN < EDGE_LABELS_LEN + 1:
        error = True
        print('ERROR: Number of vertex-labels must be greater than number of edge-labels!')
    if DATASET_LEN < 10 or DATASET_LEN > 100000:
        error = True
        print('ERROR: Total number of graphs must be in the range: [10 .. 100,000]')
    if MIN_SUPPORT < 0.01 or MIN_SUPPORT > 0.50:
        error = True
        print('ERROR: Min-support must be in the range: [0.01 .. 0.50]')
    if FREQUENTS_LEN > DATASET_LEN:
        error = True
        print('ERROR: Total number of frequent patterns cannot be larger than total number of graphs!')
    if AVRG_GRAPH_SIZE < 5 or AVRG_GRAPH_SIZE > 100:
        error = True
        print('ERROR: Average size of graphs must be in the range: [5 .. 100]')
    if AVRG_FRQNT_SIZE < 2 or AVRG_FRQNT_SIZE > 40:
        error = True
        print('ERROR: Average size of frequent patterns must be in the range: [2 .. 40]')
    if AVRG_FRQNT_SIZE >= AVRG_GRAPH_SIZE:
        error = True
        print('ERROR: Average size of frequent patterns must be less than average size of graphs!')
    if DATASET_LEN < MIN_SUPPORT * DATASET_LEN * FREQUENTS_LEN:
        error = True
        print('ERROR: Inconsistent values for: MIN-SUPPORT, DATASET-COUNT, FREQUENTS-COUNT!\n'
              '       DATASET_COUNT must be greater than: MIN-SUPPORT x DATASET-COUNT x FREQUENTS-COUNT')
    if FREQUENTS_LEN > 2 ** (VERTEX_LABELS_LEN * EDGE_LABELS_LEN):
        error = True
        print('ERROR: Total number of distinct frequent patterns cannot be larger than: ' +
              str(2 ** (VERTEX_LABELS_LEN * EDGE_LABELS_LEN)) +
              '\n       with the given number of distinct vertex and edge labels.')
    if error:
        sys.exit(1)


def print_program_params():
    """Print program parameters."""
    print('OUTPUT_DIR ...... =', OUTPUT_DIR)
    print('MIN_SUPPORT ..... =', '{:.2f}'.format(MIN_SUPPORT))
    print('DATASET_LEN ..... =', DATASET_LEN)
    print('FREQUENTS_LEN ... =', FREQUENTS_LEN)
    print('EDGE_LABELS_LEN . =', EDGE_LABELS_LEN)
    print('VERTEX_LABELS_LEN =', VERTEX_LABELS_LEN)
    print('AVRG_GRAPH_SIZE . =', AVRG_GRAPH_SIZE)
    print('AVRG_FRQNT_SIZE . =', AVRG_FRQNT_SIZE)
    print('IS_DIRECTED ..... =', IS_DIRECTED)
    print('ALLOW_LOOPS ..... =', ALLOW_LOOPS, '\n')


def random_choice(lst, n):
    """Returns n randomly chosen elements from the given collection.
    The selection can have duplicate elements,
    but consecutive elements will differ.
    """
    result = list()
    last_choice = random.choice(lst)
    result.append(last_choice)
    while len(result) < n:
        choice = random.choice(lst)
        if choice != last_choice:
            result.append(choice)
            last_choice = choice
    return result


def has_edge(graph, v1, v2):
    """Checks whether an edge exists between the given vertices."""
    if v1 in graph:
        for edge in graph[v1]:
            if edge[2] == v2:
                return True
    if v2 in graph:
        for edge in graph[v2]:
            if edge[2] == v1:
                return True
    return False


def add_edge(edge, graph):
    """Adds the given edge to the given graph.
    If the graph changes, returns True; otherwise False.
    """
    v_src = edge[0]
    v_dst = edge[2]
    if (not ALLOW_LOOPS) and v_src == v_dst:
        return False
    if has_edge(graph, v_src, v_dst):
        return False
    changed = False
    if v_src in graph:
        if edge not in graph[v_src]:
            graph[v_src].add(edge)
            changed = True
    else:
        changed = True
        graph[v_src] = {edge}
    if v_dst not in graph:
        graph[v_dst] = set()
        changed = True
    return changed


def edge_count(graph):
    """Returns the number of edges of the given graph."""
    count = 0
    for vrtx in graph.keys():
        count += len(graph[vrtx])
    return count


def add_graph(graph1, graph2):
    """Adds all edges of the first graph to the second graph."""
    for vrtx in graph1.keys():
        for edge in graph1[vrtx]:
            add_edge(edge, graph2)


def write_dot(graph, filepath):
    """Writes the given graph to the given file-path in DOT format."""
    graph_name = filepath[filepath.rfind('/') + 1: filepath.rfind('.')]
    with open(filepath, "w") as file:
        if IS_DIRECTED:
            file.write("digraph %s {\n" % graph_name)
        else:
            file.write("graph %s {\n" % graph_name)
        # write vertices
        file.write('  // graph-vertices\n')
        v_list = list(graph.keys())
        v_list.sort()
        vi = 0
        v_codes = dict()
        for vrtx in v_list:
            vi += 1
            v_codes[vrtx] = vi
            file.write('  v%d  [label=\"%s\"];\n' % (vi, vrtx))
        # write edges
        file.write('  // graph-edges\n')
        for vrtx in v_list:
            for edge in graph[vrtx]:
                if IS_DIRECTED:
                    file.write('  v%d -> v%d  [label=\"%s\"];\n' % (v_codes[edge[0]], v_codes[edge[2]], edge[1]))
                else:
                    file.write('  v%d -- v%d  [label=\"%s\"];\n' % (v_codes[edge[0]], v_codes[edge[2]], edge[1]))
        file.write('  // end-of-graph\n}\n')


# program start
parse_args()
validate_params()
print_program_params()

# check if output directory is empty
if os.path.exists(OUTPUT_DIR) and os.path.isdir(OUTPUT_DIR) and len(os.listdir(OUTPUT_DIR)) > 0:
    yes_list = ['y', 'yes', 'yeah', 'sure', 'fine']
    response = input('WARNING: output directory is NOT empty:\n%s\nDELETE CONTENTS? [y/n] ' % os.path.abspath(OUTPUT_DIR))
    if not response.lower() in yes_list:
        print('ABORT.')
        sys.exit(0)
    else:
        for path in os.listdir(OUTPUT_DIR):
            if os.path.isfile(path):
                os.remove(path)
        print(' ')

# create edge labels
edge_labels = list()
if EDGE_LABELS_LEN > 1:
    for ei in range(EDGE_LABELS_LEN):
        edge_labels.append('E' + ('{:0' + str(len(str(VERTEX_LABELS_LEN))) + 'd}').format(ei + 1))
else:
    edge_labels = [' ']

# create vertex labels
vertex_labels = list()
for vi in range(VERTEX_LABELS_LEN):
    vertex_labels.append('V' + ('{:0' + str(len(str(VERTEX_LABELS_LEN))) + 'd}').format(vi + 1))

# generate frequent subgraphs
mu = AVRG_FRQNT_SIZE
sigma = min(max(2, round(AVRG_FRQNT_SIZE / 4)), round((AVRG_GRAPH_SIZE - AVRG_FRQNT_SIZE) / 4))
frq_edge_counts = normal(mu, sigma, FREQUENTS_LEN)
frq_edge_counts = [min(max(2, int(round(cnt))), VERTEX_LABELS_LEN - 2) for cnt in frq_edge_counts]
frq_edge_counts.sort()
large_enough = comb(VERTEX_LABELS_LEN, AVRG_FRQNT_SIZE) > FREQUENTS_LEN
frq_subgraphs = list()
for pattern_len in frq_edge_counts:
    vertex_count = max(2, pattern_len + 1)
    if large_enough:
        pattern_vertices = random.sample(vertex_labels, vertex_count)
    else:
        pattern_vertices = random_choice(vertex_labels, vertex_count)
    pattern = dict()
    v = pattern_vertices.pop()
    u = pattern_vertices.pop()
    e = random.choice(edge_labels)
    add_edge((v, e, u), pattern)
    while len(pattern_vertices) > 0:
        u = pattern_vertices.pop()
        v = random.choice(list(pattern.keys()))
        e = random.choice(edge_labels)
        if not add_edge((v, e, u), pattern):
            pattern_vertices.append(u)
    frq_subgraphs.append(pattern)

# initialize dataset with empty graphs
dataset = list()
for i in range(DATASET_LEN):
    dataset.append(dict())

# add frequent patterns to dataset
counter = 1
graphs_with_pattern = set()
for pattern in frq_subgraphs:
    sup = random.uniform(0.0, 0.1) + MIN_SUPPORT
    selection = random.sample(range(DATASET_LEN), round(DATASET_LEN * sup))
    selection.sort()
    print('Pattern-#%d with %d edges and support of %.1f%%' % (counter, frq_edge_counts[counter - 1], sup * 100))
    print('inserted in %d graphs :' % len(selection), [i+1 for i in selection], '\n')
    for indx in selection:
        add_graph(pattern, dataset[indx])
    graphs_with_pattern.update(selection)
    counter += 1

# print final set of graphs with patterns
print('The following %d graphs include at least one pattern:' % len(graphs_with_pattern))
graphs_with_pattern = list(graphs_with_pattern)
graphs_with_pattern.sort()
print([i+1 for i in graphs_with_pattern], '\n')

# calculate average graph size
avrg_graph_size = 0
for graph in dataset:
    avrg_graph_size += edge_count(graph)
avrg_graph_size /= DATASET_LEN

# find remaining empty graphs in the dataset
empty_graphs_indx = list()
for idx in range(DATASET_LEN):
    if edge_count(dataset[idx]) == 0:
        empty_graphs_indx.append(idx)

# populate empty graphs
mu = AVRG_GRAPH_SIZE
sigma = min(max(2, round((AVRG_GRAPH_SIZE - avrg_graph_size) / 4)), round(AVRG_GRAPH_SIZE / 4))
graph_edge_counts = normal(mu, sigma, len(empty_graphs_indx))
graph_edge_counts = [min(max(2, int(round(cnt))), VERTEX_LABELS_LEN - 2) for cnt in graph_edge_counts]
for idx in range(len(empty_graphs_indx)):
    empty_idx = empty_graphs_indx[idx]
    additions = 0
    while additions == 0:
        v = random.choice(vertex_labels)
        u = random.choice(vertex_labels)
        e = random.choice(edge_labels)
        if add_edge((v, e, u), dataset[empty_idx]):
            additions += 1
    while additions < graph_edge_counts[idx]:
        v_src = random.choice(list(dataset[empty_idx].keys()))
        v_dst = random.choice(vertex_labels)
        e_lbl = random.choice(edge_labels)
        if add_edge((v_src, e_lbl, v_dst), dataset[empty_idx]):
            additions += 1

# calculate new average graph size
avrg_graph_size = 0
for graph in dataset:
    avrg_graph_size += edge_count(graph)
avrg_graph_size /= DATASET_LEN

# if actual average graph size differs from required average size ...
if round(AVRG_GRAPH_SIZE - avrg_graph_size) > 1:
    # then add enough random edges to random graphs in the dataset
    edges_to_add = round(AVRG_GRAPH_SIZE - avrg_graph_size) * DATASET_LEN
    additions = 0
    while additions < edges_to_add:
        graph = random.choice(dataset)
        v_src = random.choice(list(graph.keys()))
        v_dst = random.choice(vertex_labels)
        e_lbl = random.choice(edge_labels)
        if add_edge((v_src, e_lbl, v_dst), graph):
            additions += 1

# create output directories
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR + 'frequent-patterns/', exist_ok=True)

# write frequent subgraphs to files
print('Writing patterns to output files ...')
counter = 1
for graph in frq_subgraphs:
    counter_str = ('{:0' + str(len(str(FREQUENTS_LEN))) + 'd}').format(counter)
    filename = 'pattern_' + counter_str + '.dot'
    write_dot(graph, OUTPUT_DIR + 'frequent-patterns/' + filename)
    counter += 1

# write dataset graphs to files
print('Writing graph-dataset to output files ...')
counter = 1
for graph in dataset:
    counter_str = ('{:0' + str(len(str(DATASET_LEN))) + 'd}').format(counter)
    filename = 'graph_' + counter_str + '.dot'
    write_dot(graph, OUTPUT_DIR + filename)
    counter += 1

print('All done.')
