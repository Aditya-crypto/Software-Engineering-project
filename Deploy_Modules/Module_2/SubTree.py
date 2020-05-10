class SubTree(object):

    def __init__(self, value, left=None, right=None):
        self.value, self.key = value, hash(value)
        self.left, self.right = left, right

    def add_child(self, value):
        key = hash(value)

        if key == self.key:
           return

        if key > self.key:

            if self.right is None:
                self.right = SubTree(value)
            else:
                self.right.add_child(value)

        if key < self.key:

            if self.left is None:
                self.left = SubTree(value)
            else:
                self.left.add_child(value)


    def _find_minimum_subtree_child_value(self):
        current_node = self

        while current_node.left is not None:
            current_node = current_node.left

        return current_node.value


    def _find_in_order_successor(self):
        if self.right is None:
            return None

        return self.right._find_minimum_subtree_child_value()


    def remove_value(self, value):
        key = hash(value)

        if key == self.key:
            # if leaf node, remove oneself
            if self.left is None and self.right is None:
                return None

            # the following two cases return whichever child node is
            # extant for a one-child parent.

            if self.left is None and self.right is not None:
                return self.right

            if self.right is None and self.left is not None:
                return self.left

            # case where neither left or right child is empty
            if self.right is not None and self.left is not None:
                # copy the value of the first in-order successor,
                # then delete the first in-order successor node.
                self.value = self._find_in_order_successor()
                self.right = self.right.remove_value(self.value)
                return self
        else:
             if self.left is not None:
                 self.left = self.left.remove_value(value)
             if self.right is not None:
                 self.right = self.right.remove_value(value)
             return self


    # def print_bst(self):
    #     if(self is None):
    #         return
    #     print(self.key)
    #     self.left.print_bst()
    #     self.right.print_bst()
