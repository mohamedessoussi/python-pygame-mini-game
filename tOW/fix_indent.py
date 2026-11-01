lines = open("pyg.py", "r", encoding="utf-8").readlines()
# Lines 18 and 19 in file correspond to indices 17 and 18
# Indentation on these lines is causing SyntaxError
print(f"Line 18 before: {repr(lines[17])}")
print(f"Line 19 before: {repr(lines[18])}")
lines[17] = lines[17].lstrip()
lines[18] = lines[18].lstrip()
print(f"Line 18 after: {repr(lines[17])}")
print(f"Line 19 after: {repr(lines[18])}")
with open("pyg.py", "w", encoding="utf-8") as f:
    f.writelines(lines)
