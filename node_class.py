class Node():
    def __init__(self, value, paths={}, pos_x=0,pos_y=0,repel = 10):
        self.value = value
        self.paths = paths
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.position = (self.pos_x,self.pos_y)
        self.repel = repel
        self.clicked = False
