# model.py
#
# This file defines a data model for Wabbit programs.  Basically, the
# data model is a large data structure that represents the contents of
# a program as objects, not text.  Sometimes this structure is known
# as an "abstract syntax tree" or AST.   However, it's not necessarily
# directly tied to the actual syntax of the language.  So, we'll prefer
# to think of it as a more generic data model instead.
#
# To do this, you need to identify the different "elements" that make 
# up a program and encode them into classes.  To do this, it may be
# useful to "underthink" the problem. To illustrate, suppose you
# wanted to encode the idea of "assigning a value."   Assignment involves
# a location (the left hand side) and a value like this:
#
#         location = expression;
#
# To represent this, make a class with just those parts:
#
#     class Assignment:
#         def __init__(self, location, expression):
#             self.location = location
#             self.expression = expression
#
# Now, what are "location" and "expression"?  Does it matter? Maybe
# not. All you know is that an assignment operator requires both of
# those parts.  DON'T OVERTHINK IT.  Further details will be filled in
# as the project evolves.
# 
# This file is broken up into sections that describe part of the
# Wabbit language specification in comments.   You'll need to adapt
# this to actual code.
#
# Starting out, I'd advise against making this file too fancy. Just
# use basic Python class definitions.  You can add usability improvements
# later.

# ----------------------------------------------------------------------
# Part 1. Statements.
#
# Wabbit programs consist of statements.  Statements are related to
# things like assignment, I/O (printing), control-flow, and other operations.
#

# TODO: inherit from this so we can see what things are expressions and validate
# accordingly

# TODO: Think: Statements, Expressions, Locations, Definitions
import builtins


class Expression:
    pass

class Assignment:
    """
    # 1.1 Assignment
    #     location = expression ;
    """
    def __init__(self, location, expression):
        self.location = location
        self.expression = expression

    def __repr__(self):
        return f'Assignment({self.location}, {self.expression})'

    def __str__(self):
        return f'{self.location} = {self.expression};'


class Print:
    """
    # 1.2 Printing
    #     print expression ;
    """
    def __init__(self, expression):
        self.expression = expression

    def __str__(self):
        return f'print {self.expression};'

class If:
    """
    # 1.3 Conditional
    #     if test { consequence} else { alternative }
    """
    def __init__(self, test, consequence, alternative):
        self.test = test
        self.consequence = consequence
        self.alternative = alternative

    def __str__(self):
        consequences = '\n  '.join([str(c) for c in self.consequence])

        alternatives = ""
        if self.alternative is not None:
            alternatives = ' else {\n  ' + '\n  '.join([str(a) for a in self.alternative]) + '\n}'

        return f"if {self.test} {{\n  {consequences}\n}}{alternatives} "


class While:
    """
    # 1.4 While Loop
    #  while test { body }
    """
    def __init__(self, test, body):
        self.test = test
        self.consequence = body

    def __str__(self):
        consequences = '\n  '.join([str(c) for c in self.consequence])
        return f"while {self.test} {{\n  {consequences}\n}}"


class Break:
    """
    # 1.5 Break and Continue
    #   while test {
    #       ...
    #       break;   // continue
    #   }
    """
    pass


class Continue:
    """ DB has this, but I didn't think it would be necessary ... think further """
    pass


class Return():
    """
    # 1.6 Return a value
    #  return expression ;
    """

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return f"return {self.value};"

# ----------------------------------------------------------------------
# Part 2. Definitions/Declarations
#
# Wabbit requires all variables and functions to be declared in 
# advance.  All definitions have a name that identifies it.  These names
# are defined within an environment that forms a so-called "scope."  
# For example, global scope or local scope. 
#


class Variable:
    """
    # 2.1 Variables.  Variables can be declared in a few different forms.
    #    const name = value;
    #    const name [type] = value;
    #    var name type [= value];
    #    var name [type] = value;
    # Constants are immutable.  If a value is present, the type can be
    # ommitted and inferred from the type of the value.
    """
    def __init__(self, name, value=None, type=None):
        assert value or type
        self._type_specified = type is not None
        self._value_specified = value is not None

        self.name = name
        self.type = type if self._type_specified else builtins.type(value).__name__
        self.value = value

    def __str__(self):
        type = f" {self.type}" if self._type_specified else ""
        value = f" = {self.value}" if self._value_specified else ""
        return f"variable {self.name}{type}{value};"


class Constant:
    def __init__(self, name, value, type=None):
        self._type_specified = type is not None
        self.name = name
        self.type = type if self._type_specified else builtins.type(value).__name__
        self.value = value

    def __str__(self):
        type = f" {self.type}" if self._type_specified else ""
        return f"const {self.name}{type} = {self.value};"


class Function:
    """
    # 2.2 Function definitions.
    #    func name(parameters) return_type { statements }
    # An external functions can be imported from using the special statement:
    #    import func name(parameters) return_type;
    """
    def __init__(self, name, parameters, return_type, statements):
        self.name = name
        self.parameters = parameters
        self.return_type = return_type
        self.statements = statements

    def __str__(self):
        parameters = ', '.join([str(p) for p in self.parameters])
        statements = '\n  '.join([str(s) for s in self.statements])
        return f"""\
{self.name} ({parameters}) {self.return_type} {{
  {statements}
}}"""


class FunctionParemeter:
    """
    # 2.3 Function Parameters
    #
    #       func square(x int) int { return x*x; }
    #
    # A function parameter (e.g., "x int") is a special kind of
    # variable. It has a name and type like a variable, but it is declared
    # as part of the function definition itself, not as a separate "var"
    # declaration.
    """
    def __init__(self, name, type):
        self.name = name
        self.type = type

    def __str__(self):
        return f"{self.name} {self.type}"
# ----------------------------------------------------------------------
# Part 3: Expressions.
#
# Expressions represent things that evaluate to a concrete value.
#
# Wabbit defines the following expressions and operators
#
# 3.1 Literals


#
class Integer:
    """
    #        23            (Integer literal)
    """
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return f"{self.value}"


class Float:
    """
    #        4.5           (Float literal)
    """
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return f"{self.value}"

class Bool:
    """
    #        true,false    (Bool literal)
    """
    def __init__(self, value):
        self.value = value


class Char:
    """
    #        'c'           (Character literal - A single character)
    """
    def __init__(self, value):
        self.value = value


class BinaryOperator:
    """
    # 3.2 Binary Operators
    #        left + right        (Addition)
    #        left - right        (Subtraction)
    #        left * right        (Multiplication)
    #        left / right        (Division)
    #        left < right        (Less than)
    #        left <= right       (Less than or equal)
    #        left > right        (Greater than)
    #        left >= right       (Greater than or equal)
    #        left == right       (Equal to)
    #        left != right       (Not equal)
    #        left && right       (Logical and)
    #        left || right       (Logical or)
    """
    def __init__(self, operator, left, right):
        self.operator = operator
        self.left = left
        self.right = right

    def __str__(self):
        return f"{self.left} {self.operator} {self.right}"


class UnaryOperator:
    """
    # 3.3 Unary Operators
    #        +operand       (Positive)
    #        -operand       (Negation)
    #        !operand       (logical not)
    #        ^operand       (Grow memory)
    """
    def __init__(self, operator, operand):
        self.operator = operator
        self.operand = operand

    def __str__(self):
        return f"{self.operator}{self.operand}"


class Fetch:
    """
    # 3.4 Reading from a location  (see below)
    #        location
    """
    def __init__(self, location):
        self.location = location


class TypeCast:
    """
    # 3.5 Type-casts
    #         int(expr)
    #         float(expr)
    """
    def __init__(self, target_type, value):
        self.target_type = target_type
        self.value = value

    def __str__(self):
        return f"{self.target_type}({self.value})"

class FunctionCall:
    """
    # 3.6 Function/Procedure Call
    #        func(arg1, arg2, ..., argn)
    """
    def __init__(self, function_name, args):
        self.function_name = function_name
        self.args = args

    def __str__(self):
        return f"{self.function_name}({' ,'.join([str(a) for a in self.args])})"

# ----------------------------------------------------------------------
# Part 4 : Locations
#
# A location represents a place where a value is stored.  The tricky
# thing about locations is that they are used in two different ways.
# First, a location could appear on the left-hand-side of an assignment
# like this:
#
#      location = expression;     // Stores a value into location
#
# However, a location could also appear as part of an expression:
#
#      print location + 10;       // Reads a value from location
#
# A location is not necessarily a simple variable name.  For example,
# consider the following example in Python:
#
#       >>> a = [1,2,3,4]
#       >>> a[2] = 10            # Store in location "a[2]"
#       >>> print(a[2])          # Read from location "a[2]"
#
# Wabbit has two types of locations:
#


class Primitive:
    """
    # 4.1 Primitive.  A bare variable name such as "abc"
    #
    #       abc = 123;
    #       print abc;
    #
    #     Any name used must refer to an existing definition of
    #     a variable.  For example, "abc" in this example must have
    #     a corresponding declaration such as
    #
    #           var abc int;
    """
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

class MemoryAddress:
    """
    # 4.2 Memory Addresses. An integer prefixed by backtick (`)
    #
    #       `address = 123;
    #       print `address + 10;
    """
    def __init__(self, address):
        self.address = address

    def __str__(self):
        return f"`{self.address}"
#
# Note: Historically, understanding the nature of locations has been
# one of the most difficult parts of the compiler project.  Expect
# much further discussion around this topic.  I strongly suggest
# deferring work on addresses until much later in the project.
