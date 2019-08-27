# typesys.py
'''
Type System
===========
This file implements basic features of the type system.  There is a
lot of flexibility possible here, but the best strategy might be to
not overthink the problem.  At least not at first.  Here are the
minimal basic requirements:

1. Types have identity (e.g., minimally a name such as 'int', 'float', 'char')
2. Types have to be comparable. (e.g., int != float).
3. Types support different operators (e.g., +, -, *, /, etc.)

One way to achieve all of these goals is to start off with some kind
of table-driven approach.  It's not the most sophisticated thing, but
it will work as a starting point.  You can come back and refactor the
type system later.
'''

INT = 'int'
FLOAT = 'float'
CHAR = 'char'
BOOL = 'bool'

# Capabilities of operations (simple and straightforward)
binary_ops = {
    (INT, '+', INT): INT,
    (INT, '-', INT): INT,
    (INT, '<', INT): BOOL,
    (INT, '>', INT): BOOL,
}
