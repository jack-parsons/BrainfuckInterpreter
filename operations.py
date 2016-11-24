

def get_type(v):
    try:
        int(v)
        return "int"
    except (ValueError, TypeError):
        return "str"


def auto_binding(n, v, bf):
    next_index = "#0"+str(max([int(name[1:]) for name in n if get_type(name[1:]) == "int"]+[0]) + 1)
    ops["bind"](n, bf, next_index, v)
    return next_index


def nav_to_beg(namespace):
    return "[<]"


def nav_to_name(namespace, name):
    op = ""
    op += nav_to_beg(namespace)
    op += ">" * (namespace.index(name)+1)
    return op


def bind(n, bf, a, v):
    n.append(a)
    if v == "#":
        pass #do something to cope with registers
    bf[0] += "bind " + str(a) + " to " + str(v)
    return "NULL"


def add(n, bf, r1, r2):
    bf[0] += "add " + str(r1) + " to " + str(r2)
    return auto_binding(n, "#", bf)


def display(n, bf, r):
    bf[0] += "display " + str(r)
    return "NULL"


ops = {
    "bind": bind,
    "+": add,
    "disp": display,
}