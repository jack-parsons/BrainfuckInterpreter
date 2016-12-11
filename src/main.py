import string
from src.errors import *
import src.operations as operations


"""
Language that complies into Brainfuck
Every variable will be set out as follows:
0 [ref] [scratchpad] [type] [data] 0
"""


def indent(s, i):
    """
    Returns the depth of brackets surrounding a character at a given index
    """
    return sum([1 if c == "(" else 0 for c in s[:i+1]]) - sum([1 if c == ")" else 0 for c in s[:i]])


def split_atoms(s):
    # Remove whitespace before and after brackets
    s = s.strip(string.whitespace)

    # Find th minimum indentation level
    # Return 0 to signify that the string is an atom
    min_ind = min([indent(s, i) for i in range(len(s))])
    if not min_ind:
        return s

    # Split the string into atoms, only on the 'top' level indent
    atoms = []
    li = 1
    for i, char in enumerate(s):
        if indent(s, i) == min_ind and char not in "()" and char in string.whitespace:
            atoms.append(s[li:i].strip(string.whitespace))
            li = i
    return [split_atoms(ns) for ns in atoms + [s[li:-1].strip(string.whitespace)]]


def evaluate(s, n, bf):
    if type(s) == str:
        # Check that we are not evaluating an atom
        # Return the register where result is stored
        if operations.get_type(s) == "int":
            return s
        if operations.get_type(s) == "str":
            return s
    elif type(s[0]) == str:
        # If the type of the first element of the list is a string, it is an op
        # parse the binding name to the
        return operations.ops[s[0]](n, bf, *[evaluate(u, n, bf) for u in s[1:]])
    # If its not a command or atom, its a list.
    # TODO store result in a list (if BF)
    return [evaluate(ns, n, bf) for ns in s]


# def evaluate(s, n=list(), p=0):
#     if type(s) == str:
#         if s.find("(") >= 0:
#             sas = split_atoms(s)
#         else:
#             return s
#         if type(sas[0]) == str:
#             if sas[0] in operations.ops:
#                 return operations.ops[sas[0]](n, *[evaluate(u, n) for u in sas[1:]])
#         else:
#             return [evaluate(b, n) for b in sas]
#
#     if type(s[0]) == str:
#         if s[0] in operations.ops:
#             return operations.ops[s[0]](n, *[evaluate(u, n) for u in s[1:]])
#     else:
#         return [evaluate(b, n) for b in s]


def compute(s):
    try:
        bf = [">>"]
        n = []
        operations.ops["bind"](n, bf, "NULL", "NULL")
        evaluate(split_atoms(s), n, bf)
        bf[0] += operations.nav_to_reg(n, n.index("c"))
        return bf[0]
    except BSyntaxError as e:
        print(e)
print(compute("((bind a 5) (bind b 3) (bind c 12))"))
print(compute("((bind a 3) (bind b 5) (bind c 2) (+ a (+ b c)) (disp (+ a (+ a b))))"))
