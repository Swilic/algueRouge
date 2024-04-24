import os
import csv
import math

class Node:
    def __init__(self, criterion: str, is_leaf: bool = False):
        self.__attribut = criterion
        self.__isleaf = is_leaf
        self.edges_ = []  # liste des arcs du noeud
        
    def is_leaf(self) -> bool:
        return self.__isleaf
        
    def add_edge(self, label: str, child: 'Node') -> None:
        self.edges_.append(Edge(self, child, label))


class Edge:
    def __init__(self, parent: Node, child: Node, label: str):
        self.parent_ = parent
        self.child_ = child
        self.label_ = label


class Mushroom:
    def __init__(self, edible: bool):
        self.__edible = edible
        self.__cara = {}

    # fonction permettant de determiner
    # si un champignon est comestible
    def is_edible(self) -> bool:
        return self.edible
    
    def add_attribute(self, name: str, value: str) -> None:
        self.__cara[name] = value
    
    def get_attribute(self, name: str) -> str:
        return self.__cara.get(name)
    
    @property
    def edible(self):
        return self.__edible
    
    @edible.setter
    def edible(self, b: bool):
        self.__edible = b


def load_dataset(path: str) -> list[Mushroom]:
    mushrooms = []
    boolean = {'Yes': True, 'No': False}

    with open(os.getcwd() + path) as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        header = next(reader)
        for row in reader:
            mushrooms.append(Mushroom(boolean[row[0]]))
            # print(row)
            for i in range(1, len(row)):
                mushrooms[-1].add_attribute(header[i], row[i])
    return mushrooms

def calculate_entropy(mushrooms: list[Mushroom]) -> float:
    edible = 0
    for mushroom in mushrooms:
        if mushroom.is_edible:
            edible += 1
    edible /= len(mushrooms)

    if edible == 0 or edible == 1:
        return 0
    return edible * math.log(edible, 2) * ((1 - edible) / edible) - math.log(1 - edible, 2)


if __name__ == "__main__":
    load_dataset('/resources/lowmush.csv')
    print('done')
