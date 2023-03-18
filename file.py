from gui import GUI
import random

# The Vertex class for the vertices of the graph. 
# It is for helping us to represent it in the GUI of the program 
class Vertex():
    def __init__(self, value, paths={}, pos_x=0, pos_y=0, repelsion_force = 10):
        self.value = value
        self.paths = paths
        self.pos_x, self.pos_y = pos_x, pos_y
        self.position = (self.pos_x,self.pos_y)
        self.repelsion_force = repelsion_force
        self.pressed = False
        self.color = 'default'

# The File_to_Graph class for reading the file and 
# constructing the graph and other appropriate variables from that file
class File_to_Graph():
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
            #initializing the set of added vertices
            added_vertex = set()
            for line in f:
                line = line.strip()
                
                # if it is comment we just continue to the next line
                if line[0] == "#":
                    continue

                # if first 6 character is colors then fetch the number of color
                elif line[0:6].lower() == "colors":
                    self.num_colors = int(line.split('=')[1].strip())
                
                # if first character is integer it means we can start to construct the graph
                elif line[0].isdigit():
                    # fetching the values from the line 
                    from_n, to_n = line.strip().split(',')
                    from_n, to_n = int(from_n), int(to_n)

                    # checking that if variable already added or not
                    # if not we are creating and adding that object to the list
                    # using the create_vertex method, and then we are adding the
                    # value to the added_vertex set
                    if from_n not in added_vertex:
                        self.vertex_list.append(self.create_vertex(from_n))
                        added_vertex.add(from_n)
                    if to_n not in added_vertex:
                        self.vertex_list.append(self.create_vertex(to_n))
                        added_vertex.add(to_n)

                    # if these path is already exist in dictionary we can continue
                    if self.is_exist(from_n, to_n):
                        continue
                    
                        # if first variable is already in dictionary, then we can add the new neighbor
                        # else we create the new key and set pair and initialize it
                        # we do it for both cases because our graph is undirected
                    if from_n in self.dict_graph:
                        self.dict_graph[from_n].add(to_n)
                    else:
                        self.dict_graph[from_n] = {to_n}
                   
                    # if second variable is already in dictionary, then we can add the new neighbor
                    # else we create the new key and set pair and initialize it
                    if to_n in self.dict_graph:
                        self.dict_graph[to_n].add(from_n)
                    else:
                        self.dict_graph[to_n] = {from_n}

        # returning the vertex classes, dictionary of the graph and color dictionary as tuple
        return self.add_paths(), self.dict_graph, self.choose_colors()

    # The method for creating the vertex object with random position on window
    def create_vertex(self,value):
        random_pos_x, random_pos_y = self.generate_random_pos()
        return Vertex(value,pos_x = random_pos_x,pos_y = random_pos_y)

    # The helper method for generating the random position for displaying the vertex
    def generate_random_pos(self):
        random_x = random.randint(GUI.boundary[0] - 50,
                                  GUI.resolution[0] - GUI.boundary[0])
        random_y = random.randint(GUI.boundary[1],
                                  GUI.resolution[1] - GUI.boundary[1])
        return random_x, random_y
    
    # The method for checking that if path is already exist in dictionary or not
    def is_exist(self, from_n, to_n):
        if to_n in self.dict_graph and from_n in self.dict_graph[to_n]:
                return True
        return False
    
    # The method for fetching the neighbors of the vertex from dictionary
    # and assigning it to the path variable of the object of that vertex
    def add_paths(self):
        for vertex in self.vertex_list:
            if vertex.value in self.dict_graph:
                vertex.paths = self.dict_graph[vertex.value]
        return self.vertex_list

    # The method for choosing the random colors from whole color dictionary.
    # The program supports maximum 7 number of color 
    # that is why in the begining of the program we check that
    def choose_colors(self):
        if self.num_colors>len(self.dict_colors)-1:
            raise Exception("More than 7 different colors are not supported")
        
        choosen_dict_colors = dict(random.sample(list(self.dict_colors.items())[:-1],self.num_colors))
        choosen_dict_colors['default'] = (0,0,0)
        
        return choosen_dict_colors
    
