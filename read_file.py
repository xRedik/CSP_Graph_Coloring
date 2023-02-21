import sys
import os

def read_file(filename):
    dict_graph = {}
    with open(filename,"r") as f:
        for line in f:
            line = line.strip()
            
            if line[0] == "#":
                continue
            
            elif line[0:6].lower() == "colors":
                num_colors = int(line[-1])
            
            elif line[0].isdigit():
                from_n, to_n = int(line[0]), int(line[-1])
                if is_exist(dict_graph, from_n, to_n):
                    continue
                if from_n in dict_graph:
                    dict_graph[from_n].add(to_n)
                else:
                    dict_graph[from_n] = {to_n}

    return num_colors, dict_graph

def is_exist(dict_graph, from_n, to_n):
    if to_n in dict_graph and from_n in dict_graph[to_n]:
            return True
    return False

def main():
    num_colors, dict_graph = read_file("input_text.txt")
    print(num_colors, dict_graph)
    #csp(num_colors,dict_graph)

if __name__ == "__main__":
    main()
