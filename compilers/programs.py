# programs.py
#
# *** Note: Only work on this file *AFTER* you have defined the data
# model in wabbit/model.py. ***
#
# Within the bowels of your compiler, you need to represent programs
# as data structures.   In this file, you need to manually encode
# some simple Wabbit programs using the data model you've developed.
#
# The purpose of these programs is two-fold:
#
#   1. Make sure you understand the data model of your compiler.
#   2. Have some program structures that you can use for later testing
#      and experimentation.
#
# This file is broken into sections. Follow the instructions for
# each part.  Parts of this file might be referenced in later
# parts of the project.  Plan to have a lot of discussion.
#

from compilers.wabbit.model import *

# ----------------------------------------------------------------------
# Simple Expressions:
#
# Encode:   int_expr      -> 2 + 3 * 4
# Encode:   float_expr    -> 2.0 + 3.0 * 4.0
#
# This one is given to you as an example.

int_expr = BinaryOperator('+',
                          Integer(2),
                          BinaryOperator('*', Integer(3), Integer(4)))

float_expr = BinaryOperator('+', Float(2.0),
                            BinaryOperator('*', Float(3.0), Float(4.0)))

# ----------------------------------------------------------------------
# Program 1: Printing
#
# Encode the following program which tests printing and simple expresions.
#
#    print 2 + 3 * -4;
#    print 2.0 - 3.0 / -4.0;
#

program1 = [
    Print(
        BinaryOperator(
            '+',
            Integer(2),
            BinaryOperator(
                '*',
                Integer(3),
                UnaryOperator('-', Integer(4))
            )
        )
    ),
    Print(
        BinaryOperator(
            '-',
            Float(2.0),
            BinaryOperator(
                '/',
                Float(3.0),
                UnaryOperator('-', Float(4.0))
            )
        )
    )
]

# ----------------------------------------------------------------------
# Program 2: Variable and constant declarations. 
#            Expressions and assignment.
#
# Encode the following statements.
#
#    const pi = 3.14159;
#    var tau float;
#    tau = 2.0 * pi;
#    print(tau);  # TODO: check if this should just be print (no brackets)

program2 = [
    Constant('pi', 3.14159),
    Variable('tau', None, Float.name),
    Assignment(
        Primitive('tau'),
        BinaryOperator('*', Float(2.0), Primitive('pi'))
    ),
    Print(Primitive('tau'))
]

# ----------------------------------------------------------------------
# Program 3: Conditionals.  This program prints out the minimum of
# two values.
#
#    var a int = 2;
#    var b int = 3;
#    if a < b {
#        print a;
#    } else {
#        print b;
#    }
#

program3 = [
    Variable('a', Integer(2), Integer.name),
    Variable('b', Integer(3), Integer.name),
    If(
        BinaryOperator('<', Primitive('a'), Primitive('b')),
        [Print(Primitive('a')), ],
        [Print(Primitive('b')), ],
    )
]

# ----------------------------------------------------------------------
# Program 4: Loops.  This program prints out the first 10 factorials.
#
#    const n = 10;
#    var x int = 1;
#    var fact int = 1;
#
#    while x < n {
#        fact = fact * x;
#        print fact;
#        x = x + 1;
#    }
#

program4 = [
    Constant('n', Integer(10)),
    Variable('x', Integer(10), Integer.name),
    Variable('fact', Integer(1), Integer.name),

    While(
        BinaryOperator('<', Primitive('x'), Primitive('n')),
        [
            Assignment(Primitive('fact'), BinaryOperator(
                '*',
                Primitive('fact'),
                Primitive('x')
            )),
            Print(Primitive('fact')),
            Assignment(Primitive('x'),
                       BinaryOperator('+',
                                      Primitive('x'),
                                      Integer(1)
                                      )
                       )
        ]
    )
]

# ----------------------------------------------------------------------
# Program 5: Functions (simple)
#
#    func square(x int) int {
#        return x*x;
#    }
#
#    print square(4);
#    print square(10);
#

program5 = [
    Function('square',
             [FunctionParameter('x', Integer.name)],
             Integer.name,
             [Return(BinaryOperator('*', Primitive('x'), Primitive('x'))), ]
             ),
    Print(FunctionCall('square', [4, ])),
    Print(FunctionCall('square', [10, ])),
]

# ----------------------------------------------------------------------
# Program 6: Functions (complex)
#
#    func fact(n int) int {
#        var x int = 1;
#        var result int = 1;
#        while x < n {
#            result = result * x;
#            x = x + 1;
#        }
#        return result;
#    }
#
#    print(fact(10))

program6 = [
    Function('fact',
             [FunctionParameter('n', Integer.name), ],
             Integer.name,
             [
                 Variable('x', 1, Integer.name),
                 Variable('result', 1, Integer.name),
                 While(
                     BinaryOperator('<', Primitive('x'), Primitive('n')),
                     [Assignment(Primitive('x'),
                                BinaryOperator('+',
                                               Primitive('x'),
                                               Integer(1))), ]
                 ),
                 Return(Primitive('result'))
             ],
             ),
    Print(FunctionCall('fact', [Integer(10)]))
]
