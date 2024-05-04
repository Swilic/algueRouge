import unittest
from project import *

class TestMushroomDataLoading(unittest.TestCase):
    def setUp(self):
        self.mushrooms = load_dataset('mushrooms.csv')

    def test_load_dataset(self):
        
        m1 = self.mushrooms[0]
        self.assertFalse(m1.is_edible(), "Le premier champignon devrait être non comestible.")
        self.assertEqual(m1.get_attribute('cap-shape'), 'Convex')
        self.assertEqual(m1.get_attribute('odor'), 'Pungent')

        m2 = self.mushrooms[1]
        self.assertTrue(m2.is_edible(), "Le deuxième champignon devrait être comestible.")
        self.assertEqual(m2.get_attribute('cap-color'), 'Yellow')
        self.assertEqual(m2.get_attribute('odor'), 'Almond')

        m3 = self.mushrooms[2]
        self.assertTrue(m3.is_edible(), "Le troisième champignon devrait être comestible.")
        self.assertEqual(m3.get_attribute('cap-shape'), 'Bell')
        self.assertEqual(m3.get_attribute('odor'), 'Anise')

    def test_len_mushrooms(self): # Vérifier que tous les champignons sont bien chargés
        self.assertEqual(len(self.mushrooms), 8124, "Il devrait y avoir 8124 champignons dans le dataset.")  

    def test_len_attributes_mush(self): # Vérifier que tous les attributs sont bien chargés, et que edible est pas pris en compte 
        self.assertEqual(len(self.mushrooms[5]._Mushroom__cara), 22, "Il devrait y avoir 22 attributs pour chaque champignon.")
        self.assertEqual(len(self.mushrooms[12]._Mushroom__cara), 22, "Il devrait y avoir 22 attributs pour chaque champignon.")  

def make_mushroom(attributes):
    ret = Mushroom(None)
    for k, v in attributes.items():
        ret.add_attribute(k, v)
    return ret

class TestBuildTree(unittest.TestCase):
    def setUp(self):
        self.test_tree_root = build_decision_tree(load_dataset('mushrooms.csv'))

    def test_tree_main_attribute(self):
        self.assertEqual(self.test_tree_root.criterion_, 'odor', "Le premier critère de division doit être 'odor'")
        nos = ['Pungent', 'Creosote', 'Foul', 'Fishy', 'Spicy', 'Musty']
        odors = {edge.label_: edge.child_ for edge in self.test_tree_root.edges_}
        for odor in nos:
            self.assertTrue(
                odors[odor].is_leaf() and odors[odor].criterion_ == 'No',
                f'Les champignons avec une odeur \'{odor}\' doivent être non-comestibles'
            )
    def test_tree_prediction(self):
        root = self.test_tree_root
        self.assertTrue(is_edible(root, make_mushroom({'odor': 'Almond'})))
        self.assertFalse(is_edible(root, make_mushroom({'odor': 'None', 'spore-print-color': 'Green'})))
    
    def test_tree_depth(self): 
        def depth(node):
            if node.is_leaf():
                return 1
            for edge in node.edges_:
                return 1 + depth(edge.child_)
        self.assertLessEqual(depth(self.test_tree_root), 5, "La profondeur de l'arbre doit être inférieure ou égale à 5")

    def test_tree_nodes(self): # Vérifier la bonne division des noeuds
            acceptable = ['odor', 'spore-print-color', 'gill-size', 'habitat', 'cap-color']
            def check_node(node):
                if node.is_leaf():
                    return
                self.assertIn(node.criterion_, acceptable, f"Le critère de division {node.criterion_} ne doit pas être utilisé")
                for edge in node.edges_:
                    check_node(edge.child_)

class Testbuildrule(unittest.TestCase):
    def setUp(self):
        self.test_tree_root = build_decision_tree(load_dataset('mushrooms.csv'))
        self.test_rule = decision_to_rule(tree_to_rule_list(self.test_tree_root))
    
    def test_rule_parenthesis(self):
        parenthesis = {'}': '{', ']': '[', ')': '('}
        stack = []
        for c in self.test_rule:
            if c in parenthesis.values():
                stack.append(c)
            elif parenthesis.get(c) is not None:
                self.assertEqual(stack.pop(-1), parenthesis[c], "Les parenthèses ne sont pas bien équilibrées")
        
        self.assertEqual(len(stack), 0, "Les parenthèses ne sont pas bien équilibrées")





if __name__ == '__main__':
    unittest.main()
