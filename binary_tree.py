#######################################################################
# Author:  Joao Nuno Carvalho                                         #
# Date:    24.02.2019                                                 #
# License: MIT Open source                                            #
# File:    binary_tree.py                                             #
# Description: This is a implementation of a binary tree in Python    #
#              and with the differente tree traversal algorithms      #
#              that are possible.                                     #
# Note: Inspired by countless sources of info on the net.             #
#######################################################################


import queue  # For bredth first traversal.


# Child tree node.
class Node:

    def __init__(self, data):
        self.data  = data
        self.left  = None
        self.right = None


class BinaryTree:

    TRAVERSAL_DEPTH_FIRST_PRE_ORDER  = 0
    TRAVERSAL_DEPTH_FIRST_IN_ORDER   = 1
    TRAVERSAL_DEPTH_FIRST_POST_ORDER = 2
    TRAVERSAL_BREADTH_FIRST_ORDER    = 3
    COUNT                              = 10


    def __init__(self):        
        self.root   = None
        self.length = 0


    def __len__(self):
        return self.length


    def is_empty(self):
        if self.length == 0:
            return True
        else:
            return False


    # Internal
    def _contains_recursive(self, curr_node, data):
        if curr_node == None:
            return False
        elif curr_node.data == data:
            return True
        elif data < curr_node.data:
            return self._contains_recursive(curr_node.left, data)
        else:
            return self._contains_recursive(curr_node.right, data)


    # Top level.
    def __contains__(self, data):
        return self._contains_recursive(self.root, data)


    # Internal
    def _insert_recursive(self, curr_node, data):
        if curr_node == None:
            self.length += 1
            return Node(data)
        elif data < curr_node.data:
            curr_node.left = self._insert_recursive(curr_node.left, data)
        elif curr_node.data < data:
            curr_node.right = self._insert_recursive(curr_node.right, data)
        return curr_node    


    # Top level.    
    def insert(self, data):
        self.root = self._insert_recursive(self.root, data)


    # Internal
    def _min_data(self, curr_node):
        if(curr_node.left() != None):
            return self._min_data(curr_node.left)
        else:
            return curr_node.data


    # Internal
    def _delete_recursive(self, curr_node, data):
        if curr_node == None:
            return None
        elif curr_node.data == data:
            # No child node.
            if (curr_node.left == None) and (curr_node.right == None):
                self.length -= 1
                return None
            # One child left.
            elif curr_node.right == None:
                self.length -= 1
                return curr_node.left
            # One child rigth.
            elif curr_node.left == None:
                self.length -= 1 
                return curr_node.right
            # Two children.
            else:
                self.length -= 1
                minData = self._min_data(curr_node.right)
                curr_node.data  = minData
                curr_node.right = self._delete_recursive(curr_node.right, minData)
                return curr_node
        elif data < curr_node.data: 
            curr_node.left = self._delete_recursive(curr_node.left, data)
            return curr_node
        else:
            curr_node.right = self._delete_recursive(curr_node.right, data)
            return curr_node


    # Top level
    def __delitem__(self, data):
        self.root = self._delete_recursive(self.root, data)


    # Internal
    def _traversal_depth_first_pre_order(self, curr_node, lst, apply_func=None):
        if curr_node == None:
            return
        else:
            if apply_func == None:
                lst.append(curr_node.data)
            else:
                apply_func(curr_node.data)
            self._traversal_depth_first_pre_order(curr_node.left, lst, apply_func)
            self._traversal_depth_first_pre_order(curr_node.right, lst, apply_func)


    # Internal
    def _traversal_depth_first_in_order(self, curr_node, lst, apply_func=None):
        if curr_node == None:
            return
        else:
            self._traversal_depth_first_in_order(curr_node.left, lst, apply_func)
            if apply_func == None:
                lst.append(curr_node.data)
            else:
                apply_func(curr_node.data)
            self._traversal_depth_first_in_order(curr_node.right, lst, apply_func)


    # Internal
    def _traversal_depth_first_post_order(self, curr_node, lst, apply_func=None):
        if curr_node == None:
            return
        else:
            self._traversal_depth_first_post_order(curr_node.left, lst, apply_func)
            self._traversal_depth_first_post_order(curr_node.right, lst, apply_func)
            if apply_func == None:
                lst.append(curr_node.data)
            else:
                apply_func(curr_node.data)


    # Internal
    def _traversal_breadth_first_order(self, curr_node, lst, apply_func=None):
        if self.root == None:
            return
        q = queue.Queue() 
        q.put(self.root)
        while(not q.empty()):
            curr_node = q.get()
            if apply_func == None:
                lst.append(curr_node.data)
            else:
                apply_func(curr_node.data)
            if curr_node.left != None:
                q.put(curr_node.left)
            if curr_node.right != None:
                q.put(curr_node.right)


    def _prepare_correct_func(self, order):
        retFunc = None
        if order == self.TRAVERSAL_DEPTH_FIRST_PRE_ORDER:
            retFunc = self._traversal_depth_first_pre_order
        elif order == self.TRAVERSAL_DEPTH_FIRST_IN_ORDER:
            retFunc = self._traversal_depth_first_in_order
        elif order == self.TRAVERSAL_DEPTH_FIRST_POST_ORDER:
            retFunc = self._traversal_depth_first_post_order
        elif order == self.TRAVERSAL_BREADTH_FIRST_ORDER:
            retFunc = self._traversal_breadth_first_order
        else:
            raise AttributeError("Order not recognised!")
        return retFunc


    # Top level.    
    def to_list(self, order = TRAVERSAL_DEPTH_FIRST_PRE_ORDER):
        lst = []
        curr_node = self.root
        runFunc = self._prepare_correct_func(order)
        runFunc(curr_node, lst, apply_func=None)
        return lst


    # Top level.    
    def apply_func(self, apply_func, order = TRAVERSAL_DEPTH_FIRST_PRE_ORDER):
        lst = []
        curr_node = self.root
        run_func = self._prepare_correct_func(order)
        run_func(curr_node, lst, apply_func)
        return lst

    def __iter__(self): # iterate over all keys
        # Note: This first version ineficient because it needs to create a list before iterating.
        for x in self.to_list(order=self.TRAVERSAL_DEPTH_FIRST_PRE_ORDER):
            yield x

        # Note: This second version eficient.
        #       It doesn't create a temporary list previous to execution.
        #       But it doesn't work!!! 
        #       Rat's and double rat's!
        
        # self.apply_func(apply_func=lambda elem: (yield elem), order=self.TRANSVERSAL_DEPTH_FIRST_PRE_ORDER)


    # Internal
    def _draw_tree_2D_recursive(self, curr_node, space): 
        if curr_node == None: 
            return
        # Increment space between levels. 
        space += self.COUNT 
        self._draw_tree_2D_recursive(curr_node.right, space)
        # Print spaces then the node data. 
        print("\n", end="") 
        for i in range(self.COUNT, space): 
            print(" ", end='') 
        print(curr_node.data) 
        self._draw_tree_2D_recursive(curr_node.left, space)
        

    # Top level
    def draw_tree_2D(self):
        # Initial space is zero.
        self._draw_tree_2D_recursive(self.root, space = 0)


    def _balance_tree_recursive(self, nodes_lst, start_index, end_index):
        # Stop condition.
        if start_index > end_index:
            return None
        # Get middle element.
        mid_index = (start_index + end_index) // 2
        curr_node = Node(nodes_lst[mid_index])
        # By using the index of inorder traversal the subtree nodes
        # to the left and to the righ are created.
        curr_node.left  = self._balance_tree_recursive(nodes_lst, start_index, mid_index-1)
        curr_node.right = self._balance_tree_recursive(nodes_lst, mid_index+1, end_index)
        return curr_node


    # Top level.
    # Balance an unbalanded tree.
    def balance_tree(self):
        nodes_lst = self.to_list()
        nodes_lst.sort()
        # Creates the balanced binary tree from nodes list.
        n = len(nodes_lst)
        self.root = self._balance_tree_recursive(nodes_lst, 0, n-1)



###############
# Unit test's #
###############

def test_01(res_lst):
    # Test 01
    print("\nRunning test 01....\n")
    ok = True    
    tree_01 = BinaryTree()
    if tree_01.is_empty() == False:
        ok = False
        print("Error: In test 01 isEmpty().")
    tree_01.insert(1)
    if tree_01.is_empty() == True:
        ok = False
        print("Error: In test 01 isEmpty().")
    print("BinaryTree: ", tree_01.to_list())
    res_lst.append(ok)
    if ok == True:
        print("...Test 01 PASSED.")    


def test_02(res_lst):
    # Test 02
    print("\nRunning test 02....\n")
    ok = True
    tree_02 = BinaryTree()
    for i in [0,1,2,3,4]:
        tree_02.insert(i)
    if len(tree_02) != 5:
        ok = False 
        print("Error: In test 02 insert() or len().")
    if not (0 in tree_02 and
            1 in tree_02 and
            2 in tree_02 and
            3 in tree_02 and
            4 in tree_02 ) or not ( all( x in tree_02 for x in [0, 1, 2, 3, 4] ) ):
        ok = False 
        print("Error: In test 02 insert() or contains().")
    print("BinaryTree: ", tree_02.to_list())
    res_lst.append(ok)
    if ok == True:
        print("...Test 02 PASSED.")    


def test_03(res_lst):
    # Test 03
    print("\nRunning test 03....\n")
    ok = True    
    tree_03 = BinaryTree()
    for i in [0,1,2,3,4]:
        tree_03.insert(i)
    print("BinaryTree: ", tree_03.to_list())
    tree_03.draw_tree_2D()
    len_00 = len(tree_03)
    del tree_03[1]
    print("BinaryTree: ", tree_03.to_list())
    tree_03.draw_tree_2D()
    len_01 = len(tree_03)
    del tree_03[4]
    print("BinaryTree: ", tree_03.to_list())
    tree_03.draw_tree_2D()
    len_02 = len(tree_03)
    del tree_03[3]
    print("BinaryTree: ", tree_03.to_list())
    tree_03.draw_tree_2D()
    len_03 = len(tree_03)
    del tree_03[2]
    print("BinaryTree: ", tree_03.to_list())
    tree_03.draw_tree_2D()
    len_04 = len(tree_03)
    del tree_03[0]
    print("BinaryTree: ", tree_03.to_list())
    tree_03.draw_tree_2D()
    len_05 = len(tree_03)
    print(len_05)

    if (len_00 != (len_01 + 1)) or (len_00 != (len_02 + 2)) or (len_00 != (len_03 + 3)) or (len_00 != (len_04 + 4)) or (len_00 != (len_05 + 5)):
        ok = False
        print("Error: In test 03 del().")

    res_lst.append(ok)
    if ok == True:
        print("...Test 03 PASSED.")    


def test_04(res_lst):
    # Test 04
    print("\nRunning test 04....\n")
    ok = True
    tree_04 = BinaryTree()
    for i in [0,3,2,1,4]:
        tree_04.insert(i)
    print("BinaryTree: ", tree_04.to_list())    
    tree_04.draw_tree_2D()

    lst = tree_04.to_list(order = BinaryTree.TRAVERSAL_DEPTH_FIRST_PRE_ORDER)
    target_lst = [0, 3, 2, 1, 4]
    if lst != target_lst:
        ok = False
        print("Error: In test 04 to_list() TRAVERSAL_DEPTH_FIRST_PRE_ORDER.")
        print("to_list()       : ", lst)
        print("to_list() target: ", target_lst)

    lst = tree_04.to_list(order = BinaryTree.TRAVERSAL_DEPTH_FIRST_IN_ORDER)
    target_lst = [0, 1, 2, 3, 4]
    if lst != target_lst:
        ok = False
        print("Error: In test 04 to_list() TRAVERSAL_DEPTH_FIRST_IN_ORDER.")
        print("to_list()       : ", lst)
        print("to_list() target: ", target_lst)

    lst = tree_04.to_list(order = BinaryTree.TRAVERSAL_DEPTH_FIRST_POST_ORDER)
    target_lst = [1, 2, 4, 3, 0]
    if lst != target_lst:
        ok = False
        print("Error: In test 04 to_list() TRAVERSAL_DEPTH_FIRST_POST_ORDER.")
        print("to_list()       : ", lst)
        print("to_list() target: ", target_lst)

    lst = tree_04.to_list(order = BinaryTree.TRAVERSAL_BREADTH_FIRST_ORDER)
    target_lst = [0, 3, 2, 4, 1]
    if lst != target_lst:
        ok = False
        print("Error: In test 04 to_list() TRAVERSAL_BREADTH_FIRST_ORDER.")
        print("to_list()       : ", lst)
        print("to_list() target: ", target_lst)

    res_lst.append(ok)
    if ok == True:
        print("...Test 04 PASSED.")    


def test_05(res_lst):
    # Test 05
    print("\nRunning test 05....\n")
    ok = True
    tree_05 = BinaryTree()
    for i in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 14]:
        tree_05.insert(i)
    print("BinaryTree: ", tree_05.to_list())    
    tree_05.draw_tree_2D()

    lstInitial = tree_05.to_list(order = BinaryTree.TRAVERSAL_BREADTH_FIRST_ORDER)
    tree_05.balance_tree()
    tree_05.draw_tree_2D()
    lst_after_being_balanced = tree_05.to_list(order = BinaryTree.TRAVERSAL_BREADTH_FIRST_ORDER)
    
    target_lst = [7, 3, 11, 1, 5, 9, 13, 0, 2, 4, 6, 8, 10, 12, 14]
    if (lstInitial != lst_after_being_balanced) and (lst_after_being_balanced != target_lst):
        ok = False
        print("Error: In test 05 balance_tree() TRAVERSAL_BREADTH_FIRST_ORDER.")
        print("to_list()       : ", lst_after_being_balanced)
        print("to_list() target: ", target_lst)

    res_lst.append(ok)
    if ok == True:
        print("...Test 05 PASSED.")    


# A clouser - This is a hack to have access to an object inside a function by only calling a function.
def my_func(my_list_object):
  return lambda elem : my_list_object.append(elem)


def test_06(res_lst):
    # Test 06
    print("\nRunning test 06....\n")
    ok = True
    tree_06 = BinaryTree()
    for i in [0,3,2,1,4]:
        tree_06.insert(i)
    print("BinaryTree: ", tree_06.to_list())    
    tree_06.draw_tree_2D()
    lst_01 = tree_06.to_list(order = BinaryTree.TRAVERSAL_DEPTH_FIRST_PRE_ORDER)
    print("to_list() target: ", lst_01)
    # This uses the clousure hack, to generate a list by calling the append method of a list like a function.
    lst_from_outside = []
    apply_func_my_obj = my_func(lst_from_outside)
    tree_06.apply_func(apply_func=apply_func_my_obj, order = BinaryTree.TRAVERSAL_DEPTH_FIRST_PRE_ORDER)
    print("apply_func():     ", lst_from_outside, " lst_from_outside")
    # Only print's to the screen.
    print("begin apply_func() print...")
    apply_func_my_func = print
    tree_06.apply_func(apply_func=apply_func_my_func, order = BinaryTree.TRAVERSAL_DEPTH_FIRST_PRE_ORDER)
    print("...end apply_func() print.")
    if lst_01 != lst_from_outside:
        ok = False
        print("Error: In test 06 apply_func() TRAVERSAL_DEPTH_FIRST_PRE_ORDER.")
        print("apply_func():     ", lst_from_outside)
        print("to_list() target: ", lst_01)

    res_lst.append(ok)
    if ok == True:
        print("...Test 06 PASSED.")
            

def test_07(res_lst):
    # Test 07
    print("\nRunning test 07....\n")
    ok = True
    tree_07 = BinaryTree()
    for i in [0,3,2,1,4]:
        tree_07.insert(i)
    print("BinaryTree: ", tree_07.to_list())    
    lst_01 = tree_07.to_list(order = BinaryTree.TRAVERSAL_DEPTH_FIRST_PRE_ORDER)
    print("to_list() target:              ", lst_01)
    
    lst_02 = []
    for elem in tree_07:
        lst_02.append(elem)
    print("For __iter__():                ", lst_02)

    lst_03 = [elem for elem in tree_07]
    print("List comprehension __iter__(): ", lst_03)
    
    if lst_01 != lst_02 and lst_01 != lst_03:
        ok = False
        print("Error: In test 07 __iter__() TRAVERSAL_DEPTH_FIRST_PRE_ORDER.")

    res_lst.append(ok)
    if ok == True:
        print("...Test 07 PASSED.")


def runTests():
    res = []
    
    test_01(res)
    test_02(res)
    test_03(res)
    test_04(res)
    test_05(res)
    test_06(res)
    test_07(res)
    
    if all(res):
        print("\n** PASSED ALL TESTS! **")


if __name__ == "__main__":
    print("Start running tests to BinaryTree....\n\n")
    runTests()
    print("\n...Finished running tests to BinaryTree....")


# Google Python Naming Conventions:
#   module_name, package_name, ClassName, method_name, ExceptionName, function_name,
#   GLOBAL_CONSTANT_NAME, global_var_name, instance_var_name, function_parameter_name, local_var_name

