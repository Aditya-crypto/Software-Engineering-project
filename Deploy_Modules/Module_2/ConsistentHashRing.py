from SubTree import SubTree as SubTree
class ConsistentHashRing():

    def __init__(self, value=None):
        self.head = None if value is None else SubTree(value)

    def add_node(self, value):
        if self.head is None:
            self.head = SubTree(value)
        else:
            self.head.add_child(value)

    def remove_node(self, value):
        if self.head is None:
            return

        self.head = self.head.remove_value(value)


    def find_best_match(self, value):
         key = hash(value)
         current_node = self.head
         best_match, best_match_key = None, float("inf")
         # if tree is empty, return None
         if not self.head:
             return None

         while current_node is not None:
             if current_node.key == key:
                 return current_node.value

                # if number is bigger, check if it is closer to our target value than the last number, and choose to update
                # accordingly
             if current_node.key > key:
                 best_match = current_node.value if abs(current_node.key - key) < abs(best_match_key - key) else best_match
                 best_match_key = hash(best_match)

                 current_node = current_node.left
                 continue

             if current_node.key < key:
                 current_node = current_node.right
                 continue

         # best_match can still be None if all values in the BST are smaller than the submitted value. In that case,
         # we always return the smallest value in the BST, in line with the principles behind consistent hashing.

         if best_match:
             return best_match
         else:
             # will always return the smallest value in the BST
             return self.head._find_minimum_subtree_child_value()

    # def print_call(self):
    #     self.head.print_bst()
