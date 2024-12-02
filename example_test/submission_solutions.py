
# Return the first five characters of string_input
# Assume that all inputs to first_five are longer than five characters
# Eg. first_five("Hello World") should return "Hello"
def first_five(string_input: str) -> str:
    return string_input[0:5]


# Return every odd indexed character of string_input
# Eg. odd_chars("Hello World") should return "el ol"
def odd_chars(string_input: str) -> str:
    string_output = ""
    for idx, char in enumerate(string_input):
        if idx % 2 == 1:
            string_output += char
    return string_output


# Return true if string_input is a palindrome
# Assume that string_input is not empty
# Note: check_palindrome should not be case sensitive
# Eg. check_palindrome("Helloolleh") should return True
def check_palindrome(string_input: str) -> bool:
    string_input = string_input.lower()
    reverse = string_input[::-1]
    for idx, char in enumerate(string_input):
        if string_input[idx] != reverse[idx]:
            return False
    return True

# Implement the following truth table
# | a | b | out |
# +---+---+-----+
# | T | T |  F  |
# | T | F |  T  |
# | F | T |  T  |
# | F | F |  F  |
# +---+---+-----+
def two_input_truth_table(a: bool, b: bool) -> bool:
    return a ^ b

# Implement the following truth table
# | a | b | c | out |
# +---+---+---+-----+
# | T | T | T |  T  |
# | T | T | F |  T  |
# | T | F | T |  F  |
# | T | F | F |  T  |
# | F | T | T |  F  |
# | F | T | F |  T  |
# | F | F | T |  F  |
# | F | F | F |  T  |
# +---+---+---+-----+

def three_input_truth_table(a: bool, b: bool, c: bool) -> bool:
    return not c or (a and b)

# Use the following Node definition to finish the next function
class Node:
    def __init__(self, val):
        self.next = None
        self.value = 0
    
# Return the value of the fifth element in the linked list
# If the list is shorter than 5 elments, return -1
# Eg. For the given linked list, fifth_node(head) should return 5
#      head
#       |
#       v
#       1 -> 2 -> 3 -> 4 -> 5 -> 6 -> 7

def fifth_node(head: Node) -> int:
    for i in range (4):
        if head == None:
            return -1
        head = head.next
    if head == None:
        return -1
    return head.value

# Write a recursive function that finds the i'th value of the sequence.
# Each element of the sequence is computed by adding up the three previous elements
# The first three elements of the sequence are 1,2, and 3.
# Note: Start counting from 0, so element 0 is 1.
def find_value(i: int) -> int:
    if i == 0:
        return 1
    elif i == 1:
        return 2
    elif i == 2:
        return 3
    else:
        return find_value(i-1) + find_value(i-2) + find_value(i-3)

