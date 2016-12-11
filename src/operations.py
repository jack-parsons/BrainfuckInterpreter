
types = {
    "int": 1,
}


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


def nav_to_beg():
    return "<[[<]<]"


def nav_to_end():
    return "[[>]>]<"


def nav_to_reg(namespace, r):
    return nav_to_beg() + ">>[[>]<" + "-"*(r+1) + "[" + "+"*(r+1) + ">]>]<" + "+"*(r+1) + "[<]"


def get_val(v):
    if get_type(v) == "int":
        return int(v)


def bind(n, bf, a, v):
    if v == "#" or v == "NULL":
        if a not in n:
            n.append(a)
        # do something to cope with registers
    elif a not in n:
        n.append(a)
        bf[0] += nav_to_end() + ">" + "+"*types[get_type(v)] + ">" +\
                 "-"*(get_val(v)+2) + ">->" + "+"*(n.index(a)+1)
    #bf[0] += "bind " + str(a) + " to " + str(v)
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