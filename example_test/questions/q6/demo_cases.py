"""Demo Cases for problem 6"""

import unittest
from submission import fifth_node

class Node:
    def __init__(self, val):
        self.next = None
        self.value = val

class List:
    def __init__(self):
        self.head = None

    def get_head(self):
        return self.head

    def add(self, val):
        if self.head == None:
            self.head = Node(val)
        else:
            node = self.head
            while node.next != None:
                node = node.next
            node.next = Node(val)
        
class Test(unittest.TestCase):
    def test_fifth_node1(self):
        test_list = List()
        test_list.add(1)
        test_list.add(2)
        test_list.add(3)
        test_list.add(4)
        test_list.add(5)
        test_list.add(6)
        self.assertEqual(fifth_node(test_list.get_head()), 5)