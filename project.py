import os
import csv
import math


class Node:
    def __init__(self, criterion: str, is_leaf: bool = False):
        self.__attribut = criterion
        self.__isleaf = is_leaf
        self.edges_ = []  # liste des arcs du noeud
        self.children = []
        
    def is_leaf(self) -> bool:
        return self.__isleaf
        
    def add_edge(self, label: str, child: 'Node') -> None:
        self.edges_.append(Edge(self, child, label))
    
    def add_children(self, child: 'Node') -> None:
        self.children.append(child)


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
    """
    Chargement du dataset
    :param path: chemin du fichier csv
    :return: liste des champignons
    """
    mushrooms = []
    boolean = {'Yes': True, 'No': False}

    with open(os.getcwd() + path) as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        header = next(reader)
        mushrooms.append(header)
        for row in reader:
            mushrooms.append(Mushroom(boolean[row[0]]))
            # print(row)
            for i in range(0, len(row)):
                mushrooms[-1].add_attribute(header[i], row[i])
    return mushrooms

def get_info_gain(header: list, mush: list[Mushroom], all_value: list, entr_edib: int) -> float:
    """
    Calcul de l'information gain
    :param header: liste des attributs
    :param mush: liste des champignons
    :param all_value: liste des valeurs possibles pour chaque attribut
    :param entr_edib: entropie des champignons comestibles
    :return: l'attribut qui maximise l'information gain
    """
    info_gain = []
    for i in range(1, len(header)):
        somme = 0
        for value in all_value[i]:
            mushroom_same_attribute = get_mushrooms_same_attribute(mush, header[i], value)
            prop_with_value = len(mushroom_same_attribute) / len(mush)
            entr_same_mush = calculate_entropy(mushroom_same_attribute)
            somme += prop_with_value * entr_same_mush
            # print(value, " ", mushroom_same_attribute)
        info_gain.append((header[i], entr_edib - somme))

    return max(info_gain, key=lambda x: x[1])

def get_all_values(mushrooms: list[Mushroom]) -> list[str]:
    """
    Récupération de toutes les valeurs possibles pour chaque attribut
    :param mushrooms: liste des champignons
    :return: liste des valeurs possibles pour chaque attribut
    """
    values = []
    mush = mushrooms[1:]
    for attribute in mushrooms[0]:
        values.append(get_all_values_from_attribute(mush, attribute))
    return values
    
def get_all_values_from_attribute(mushrooms: list[Mushroom], attribute: str) -> list[str]:
    """
    Récupération de toutes les valeurs possibles pour un attribut
    :param mushrooms: liste des champignons
    :param attribute: attribut
    :return: liste des valeurs possibles pour un attribut
    """
    values = set()
    for mushroom in mushrooms:
        values.add(mushroom.get_attribute(attribute))
    return values

def calculate_entropy(mushrooms: list[Mushroom]) -> float:
    prop = proportion_edible_mushrooms(mushrooms)

    if prop == 0 or prop == 1:
        return 0
    return prop * math.log(((1 - prop) / prop), 2) - math.log(1 - prop, 2)

def get_mushrooms_same_attribute(mushrooms: list[Mushroom], attribute: str, value: str) -> list[Mushroom]:
    mushrooms_with_attribute = []
    for mushroom in mushrooms:
        if mushroom.get_attribute(attribute) == value:
            mushrooms_with_attribute.append(mushroom)
    return mushrooms_with_attribute

def proportion_edible_mushrooms(mushrooms: list[Mushroom]) -> int:
    edible = 0
    for mushroom in mushrooms:
        if mushroom.edible:
            edible += 1
    return edible/len(mushrooms)

def build_decision_tree(mushrooms: list[Mushroom]) -> Node:
    header = mushrooms[0]
    mush = mushrooms[1:]
    all_value = get_all_values(mushrooms)
    entr_edib = calculate_entropy(mush)
    # print(entr_edib)
    info_gain = get_info_gain(header, mush, all_value, entr_edib)
    print(info_gain)

       

if __name__ == "__main__":
    mushrooms = load_dataset('/resources/lowmush.csv')
    tree = build_decision_tree(mushrooms)
    print('done')
