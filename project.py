import os
import csv
import math

FILENAME = 'mushrooms.csv'

class Node:
    def __init__(self, criterion: str, is_leaf: bool = False):
        self.criterion_ = criterion
        self.__isleaf = is_leaf
        self.edges_ = []  # liste des arcs du noeud
        
    def is_leaf(self) -> bool:
        return self.__isleaf
        
    def add_edge(self, parent: 'Node', child: 'Node', label: str) -> None:
        self.edges_.append(Edge(self, child, label))
    
    def add_children(self, child: 'Node') -> None:
        self.children.append(child)

    @property
    def attribut(self):
        return self.criterion_  
    
    def copy(self) -> 'Node':
        node = Node(self.__attribut, self.__isleaf)
        for edge in self.edges_:
            node.add_edge(edge.parent_, edge.child_, edge.label_)

        return node


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

def get_header(path:str) -> list[str]:
    """
    Permet d'extraire tous les attributs (sauf edible) d'un fichier csv 
    :param path: chemin d'accès du fichier à extraire.
    :return: list avec les attributs.
    """
    with open(os.getcwd() + '/' + path) as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        header = next(reader)
    return header[1:]

def make_mushroom(attributes):
    ret = Mushroom(None)
    for k, v in attributes.items():
        ret.add_attribute(k, v)
    return ret

def load_dataset(path: str) -> list[Mushroom]:
    """
    Chargement du dataset.
    :param path: chemin du fichier csv.
    :return: liste des champignons.
    """
    mushrooms = []
    boolean = {'Yes': True, 'No': False}
    with open(os.getcwd() + '/' + path) as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        header = next(reader)
        
        for row in reader:
            mushrooms.append(Mushroom(boolean[row[0]]))
            # print(row)
            for i in range(0, len(row)):
                mushrooms[-1].add_attribute(header[i], row[i])
    return mushrooms

def get_info_gain(mush: list[Mushroom], all_value: list, entr_edib: int) -> float:
    """
    Calcul de l'information gain.
    :param mush: liste des champignons.
    :param all_value: liste des valeurs possibles pour chaque attribut.
    :param entr_edib: entropie des champignons comestibles.
    :return: l'attribut qui maximise l'information gain.
    """
    info_gain = []
    header = get_header(FILENAME)
    for i in range(len(header)):
        somme = 0
        for value in all_value[i]:
            mushroom_same_attribute = get_mushrooms_same_value(mush, header[i], value)
            prop_with_value = len(mushroom_same_attribute) / len(mush)
            entr_same_mush = calculate_entropy(mushroom_same_attribute)
            somme += prop_with_value * entr_same_mush
            # print(value, " ", mushroom_same_attribute)
        info_gain.append((header[i], entr_edib - somme))

    return info_gain

def get_all_values(mushrooms: list[Mushroom]) -> list[str]:
    """
    Récupération de toutes les valeurs possibles pour chaque attribut.
    :param mushrooms: liste des champignons.
    :return: liste des valeurs possibles pour chaque attribut.
    """
    values = []
    header = get_header('lowmush.csv')
    for attribute in header:
        values.append(get_all_values_from_attribute(mushrooms, attribute))
    return values
    
def get_all_values_from_attribute(mushrooms: list[Mushroom], attribute: str) -> list[str]:
    """
    Récupération de toutes les valeurs possibles pour un attribut.
    :param mushrooms: liste des champignons.
    :param attribute: attribut.
    :return: liste des valeurs possibles pour un attribut.
    """
    values = set()
    for mushroom in mushrooms:
        values.add(mushroom.get_attribute(attribute))
    return values

def calculate_entropy(mushrooms: list[Mushroom]) -> float:
    """
    Calcul l'entropy par rapport à une liste de champignon donnée.
    :param mushrooms: liste avec les champignons qu'il faut calculer.
    :return: le résultat du calcul (float).
    """
    prop = proportion_edible_mushrooms(mushrooms)

    if prop == 0 or prop == 1:
        return 0
    return prop * math.log(((1 - prop) / prop), 2) - math.log(1 - prop, 2)

def get_mushrooms_same_value(mushrooms: list[Mushroom], attribute: str, value: str) -> list[Mushroom]:
    """
    Regroupe dans une liste tous les champignons avec la même valeur sur un attribut.
    :param mushrooms: liste avec les champignons.
    :param attribute: l'attribut pour laquelle on veut regarder la valeur.
    :param value: la valeur de l'attribut.
    :return: liste avec les champignons de même valeur.
    """
    mushrooms_with_value = []
    for mushroom in mushrooms:
        if mushroom.get_attribute(attribute) == value:
            mushrooms_with_value.append(mushroom)
    return mushrooms_with_value

def proportion_edible_mushrooms(mushrooms: list[Mushroom]) -> int:
    """
    Calcule la proportion de champignons comestibles dans une liste donnée.

    :param mushrooms: Une liste avec les champignons.

    :returns: La proportion de champignons comestibles sous forme décimale.
    """
    edible = 0
    for mushroom in mushrooms:
        if mushroom.edible:
            edible += 1
    return edible/len(mushrooms)

def link_info_value(info_gain: list[tuple[str, float]], all_value: list[str]) -> list[tuple[str, float]]:
    """
    Associe chaque attribut avec son information gain.
    :param info_gain: liste des informations gain.
    :param all_value: liste des valeurs possibles pour chaque attribut.
    :return: liste des attributs avec leur information gain.
    """
    linked_info = []
    for i in range(len(info_gain)):
        if info_gain[i][1] == 0:
            continue
        linked_info.append((all_value[i], info_gain[i]))
    linked_info.sort(key=lambda x: x[1][1], reverse=True)
    return linked_info

def display(node: Node, depth: int = 0) -> None:
    """
    Affiche l'arbre de décision.
    :param node: noeud de l'arbre.
    :param depth: profondeur de l'arbre.
    """
    if node.is_leaf():
        if node.attribut == 'Edible':
            print('  ' * depth, 'Edible')
        else:
            print('  ' * depth, 'Not edible')
    else:
        print('  ' * depth, node.attribut)
        for edge in node.edges_:
            print('  ' * (depth + 1), edge.label_)
            display(edge.child_, depth + 2)

def build_decision_tree(mushrooms: list[Mushroom]) -> Node:
    entr_edib = calculate_entropy(mushrooms)
    if entr_edib == 0:
        if mushrooms[0].edible:
            return Node('Edible', True)
        else:
            return Node('No', True)

    all_value = get_all_values(mushrooms)    

    info_gain = get_info_gain(mushrooms, all_value, entr_edib)
    info_gain.sort(key=lambda x: x[1], reverse=True)
    max_info = info_gain[0][0]
    node = Node(max_info)

    all_value = get_all_values_from_attribute(mushrooms, max_info)
    for value in all_value:
        mushrooms_same_value = get_mushrooms_same_value(mushrooms, max_info, value)
        if len(mushrooms_same_value) == 0:
            continue
        child_node = build_decision_tree(mushrooms_same_value)
        node.add_edge(node, child_node, value)
    
    return node

def is_edible(node: Node, m: 'Mushroom') -> bool:
    """
    Permet de déterminer si un champignon est comestible.
    :param node: noeud de l'arbre.
    :param m: champignon.
    :return: True si comestible, False sinon.
    """
    if node.is_leaf():
        return node.attribut == 'Edible'
    
    for edge in node.edges_:
        if m.get_attribute(node.attribut) == edge.label_:
            return is_edible(edge.child_, m)
    return False


if __name__ == "__main__":
    mushrooms = load_dataset(FILENAME)
    tree = build_decision_tree(mushrooms)
    print(is_edible(tree, make_mushroom({'odor': 'Almond'})))
    # display(tree)
    print('done')
