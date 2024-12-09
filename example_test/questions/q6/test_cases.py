"""Demo Cases for problem 6"""

import unittest
from submission import fifth_node
from decorators import weight

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
    @weight(3)
    def test_fifth_node1(self):
        test_list = List()
        test_list.add(1)
        test_list.add(2)
        test_list.add(3)
        test_list.add(4)
        test_list.add(5)
        test_list.add(6)
        self.assertEqual(fifth_node(test_list.get_head()), 5)

    @weight(3)
    def test_fifth_node2(self):
        test_list = List()
        test_list.add(10)
        test_list.add(20)
        test_list.add(30)
        test_list.add(40)
        test_list.add(50)
        self.assertEqual(fifth_node(test_list.get_head()), 50)

    @weight(3)
    def test_fifth_node3(self):
        test_list = List()
        test_list.add(1)
        test_list.add(2)
        test_list.add(3)
        test_list.add(4)
        self.assertEqual(fifth_node(test_list.get_head()), -1)

    @weight(1)
    def test_fifth_node4(self):
        test_list = List()
        self.assertEqual(fifth_node(test_list.get_head()), -1)