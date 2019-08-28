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

# Capabilities of operations (simple and straightforward)
from compilers.wabbit.model import Integer, Bool, Float, Char

binary_ops = {
    (Integer.type, '+', Integer.type): Integer.type,
    (Integer.type, '*', Integer.type): Integer.type,

    (Integer.type, '-', Integer.type): Integer.type,
    (Integer.type, '<', Integer.type): Bool.type,
    (Integer.type, '>', Integer.type): Bool.type,

    (Float.type, '*', Float.type): Float.type,
    (Float.type, '+', Float.type): Float.type,
    # TODO: *, /, and for floats, ...
}

unary_ops = {
    # +operand (Positive)
    # -operand (Negation)
    # !operand (logical not)
    # ^operand (Grow memory)
    ('-', Integer.type): Integer.type,
    ('^', Integer.type): Integer.type,
    ('-', Float.type): Float.type,
    ('!', Bool.type): Bool.type,

}


type_casts = {
    # Casting to Integer:
    (Float.type, Integer.type): Integer.type,
    (Integer.type, Integer.type): Integer.type,

    # Casting to Float
    (Float.type, Float.type): Float.type,
    (Integer.type, Float.type): Float.type,

    # Casting to Bool
    (Integer.type, Bool.type): Bool.type,
    (Float.type, Bool.type): Bool.type,
    (Char.type, Bool.type): Bool.type,
    (Bool.type, Bool.type): Bool.type,
}

def check_binop(left_type, op, right_type):
    """ Check if a binary operator is supported. Return result type or None if unsupported """
    return binary_ops.get((left_type, op, right_type))


def check_unop(operator, operand):
    return unary_ops.get((operator, operand))


def check_typecast(from_type, to_type):
    return type_casts.get((from_type, to_type))