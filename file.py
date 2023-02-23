from gui import GUI
import random

class Vertex():
    def __init__(self, value, paths={}, pos_x=0, pos_y=0, repelsion_force = 10):
        self.value = value
        self.paths = paths
        self.pos_x, self.pos_y = pos_x, pos_y
        self.position = (self.pos_x,self.pos_y)
        self.repelsion_force = repelsion_force
        self.pressed = False

class File_handler():
    def __init__(self, filename):
        self.filename = filename
        self.num_colors = 0
        self.vertex_list = []
        self.dict_graph = {}
        self.dict_colors = {
            "red": (255,0,0),
            "green": (0,255,0),
            "blue": (0,0,255),
            "yellow": (255,255,0),
            "magenta": (255,0,255),
            "cyan": (0,255,255),
            "camelot": (152, 53, 91),
            "default": (0,0,0)
        }

    def construct_graph_from_file(self):
        with open(self.filename,"r") as f:
            added_vertex = set()
            for line in f:
                line = line.strip()
                
                if line[0] == "#":
                    continue
                
                elif line[0:6].lower() == "colors":
                    self.num_colors = int(line[-1])
                
                elif line[0].isdigit():
                    from_n, to_n = int(line[0]), int(line[-1])

                    if from_n not in added_vertex:
                        self.vertex_list.append(self.create_vertex(from_n))
                        added_vertex.add(from_n)
                    if to_n not in added_vertex:
                        self.vertex_list.append(self.create_vertex(to_n))
                        added_vertex.add(to_n)

                    if self.is_exist(from_n, to_n):
                        continue
                    
                    if from_n in self.dict_graph:
                        self.dict_graph[from_n].add(to_n)
                    else:
                        self.dict_graph[from_n] = {to_n}

        return self.num_colors, self.add_paths()

    def generate_random_pos(self):
        random_x = random.randint(GUI.boundary[0] - 50,
                                  GUI.resolution[0] - GUI.boundary[0])
        random_y = random.randint(GUI.boundary[1],
                                  GUI.resolution[1] - GUI.boundary[1])
        return random_x, random_y

    def create_vertex(self,value):
        random_pos_x, random_pos_y = self.generate_random_pos()
        return Vertex(value,pos_x = random_pos_x,pos_y = random_pos_y)

    def is_exist(self, from_n, to_n):
        if to_n in self.dict_graph and from_n in self.dict_graph[to_n]:
                return True
        return False
    
    def add_paths(self):
        for vertex in self.vertex_list:
            if vertex.value in self.dict_graph:
                vertex.paths = self.dict_graph[vertex.value]
        return self.vertex_list

    def choose_colors(self):
        if self.num_colors>len(self.dict_colors)-1:
            raise Exception("More than 7 different colors are not supported")
        return random.sample(list(self.dict_colors.items())[::-1],self.num_colors)