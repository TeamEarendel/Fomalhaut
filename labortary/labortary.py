import _io

print(type(open(".gitkeep", "r")) == _io.TextIOWrapper)
