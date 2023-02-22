from node_class import Node
import gui_config
import random

def create_node(value):
    random_pos_x, random_pos_y = generate_random_pos()
    return Node(value,pos_x = random_pos_x,pos_y = random_pos_y)

def is_exist(dict_graph, from_n, to_n):
    if to_n in dict_graph and from_n in dict_graph[to_n]:
            return True
    return False

def generate_random_pos():
    random_x = random.randint(gui_config.X_boundary - 50,
                            gui_config.resolution[0] - gui_config.X_boundary)
    random_y = random.randint(gui_config.Y_boundary,
                            gui_config.resolution[1] - gui_config.Y_boundary)
    return random_x, random_y

def read_file(filename):
    dict_graph = {}

    with open(filename,"r") as f:
        node_class_lists = []
        added_vertex = set()
        for line in f:
            line = line.strip()
            
            if line[0] == "#":
                continue
            
            elif line[0:6].lower() == "colors":
                num_colors = int(line[-1])
            
            elif line[0].isdigit():
                from_n, to_n = int(line[0]), int(line[-1])

                if from_n not in added_vertex:
                    node_class_lists.append(create_node(from_n))
                    added_vertex.add(from_n)
                if to_n not in added_vertex:
                    node_class_lists.append(create_node(to_n))
                    added_vertex.add(to_n)

                if is_exist(dict_graph, from_n, to_n):
                    continue
                
                if from_n in dict_graph:
                    dict_graph[from_n].add(to_n)
                else:
                    dict_graph[from_n] = {to_n}

    return num_colors, add_paths(node_class_lists,dict_graph)

def add_paths(node_class_lists,dict_graph):
    for node in node_class_lists:
        if node.value in dict_graph:
            node.paths = dict_graph[node.value]
    return node_class_lists

def choose_colors(num_colors):
    dict_colors = {
        "red": (255,0,0),
        "green": (0,255,0),
        "blue": (0,0,255),
        "yellow": (255,255,0),
        "magenta": (255,0,255),
        "cyan": (0,255,255),
        "camelot": (152, 53, 91),
        "default": (0,0,0)
    }
    if num_colors>len(dict_colors)-1:
        raise Exception("More than 7 different colors are not supported")
    return random.sample(list(dict_colors.items())[::-1],num_colors)