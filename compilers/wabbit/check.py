# check.py
#
# This file will have the type-checking/validation 
# part of the compiler.  There are a number of things
# that need to be managed to make this work. First,
# you have to have some notion of "type" in your compiler.
# Second, you need to manage environments/scoping in order
# to handle the names of definitions (variables, functions, etc).
#
# A key to this part of the project is going to be test coverage.
# As you add code, think about how to add unit tests.
from compilers.wabbit.errors import error
from compilers.wabbit.model import *
from collections import ChainMap

# in each function:
# * the node is the instance of the class
# * the env is the environment / symbol table
from compilers.wabbit.typesys import check_binop, check_unop, check_typecast


def check_program(top, get_env=ChainMap):
    """The top level function that checks everything (creates the initial)"""
    env = get_env()
    check(top, env)


def check(node, env):
    """Check individual nodes/lists by dispatching the relevant check_<> method. """
    if isinstance(node, list):
        for n in node:
            check(n, env)
    elif isinstance(node, Expression):  # 3. Expression -> Node
                                        # 4. Location -> Expression -> Node
        check_expression(node, env)
    elif isinstance(node, Definition):  # 2. Definition -> Statement -> Node
        check_definition(node, env)
    elif isinstance(node, Statement):   # 1. Statement -> Node
        assert not isinstance(node, Definition), 'Definitions should be checked separately'
        check_statement(node, env)
    else:
        raise RuntimeError(f'{node} not checked!')  # should always do this

# Expression Checks
# =================


def check_expression(node, env):
    if isinstance(node, BinaryOperator):
        check_BinaryOperator(node, env)
    elif isinstance(node, UnaryOperator):
        check_UnaryOperator(node, env)
    elif isinstance(node, FunctionCall):
        check_FunctionCall(node, env)
    elif isinstance(node, TypeCast):
        check_TypeCast(node, env)
    elif isinstance(node, Location):  # covers multiple sub-types
        check_Location(node, env)
    elif isinstance(node, Literal):  # covers multiple sub-types
        check_Literal(node, env)
    elif isinstance(node, Fetch):
        check_Fetch(node, env)
    else:
        raise RuntimeError(f"Expression {node} not checked.")


def check_BinaryOperator(node, env):
    check(node.left, env)
    check(node.right, env)
    node.type = check_binop(node.left.type, node.operator, node.right.type)
    if node.type is None and (node.left.type and node.right.type):
        # if left and right have types then we are *not* in a cascading case
        error(f'Invalid binop: {node.left.type} {node.operator} {node.right.type}')


def check_UnaryOperator(node, env):
    node.type = check_unop(node.operator, node.operand.type)
    if node.type is None:
        error(f'Invalid unary operation: {node.operator}{node.operand}')


def check_TypeCast(node, env):
    check(node.value, env)
    node.type = check_typecast(node.value.type, node.target_type)


def check_FunctionCall(node, env):
    # Check function arguments
    check(node.args, env)

    # Check that the function is defined
    func = env.get(node.name)
    if func is None:
        error(f'Function {node.function_name} is not defined.')

    # Check that the function is a function
    if not isinstance(func, Function):
        error(f'Cannot call {node.name} as a function')
        return  # ... and no further checking is possible

    # Check that the function has all of the arguments that it needs
    if len(func.parameters) != len(node.args):
        error(f'Function is missing required arguments. Needs {func.parameters} got {node.args}')

    # Check that the function parameter types match the supplied argument types
    for n, (arg, param) in enumerate(zip(node.args, func.parameters), 1):
        if param.type != arg.type:
            error(f'Type error in argument {n}: {param.type} != {arg.type}')

    node.type = func.return_type


def check_Location(node, env):
    if isinstance(node, NamedLocation):
        check_NamedLocation(node, env)
    else:
        raise RuntimeError(f"Location {node} not checked.")

    # Assignment checks require that location checks add a mutability attribute
    assert hasattr(node, 'mutable')


def check_NamedLocation(node, env):
    declaration = env.get(node.name)
    if declaration is None:
        error(f'Location {node} was not declared')
        return  # cannot do further checking

    node.type = declaration.type
    node.mutable = not isinstance(declaration, (Constant, Function))


# Definition / Declaration Checks
# ===============================

def check_definition(node, env):
    if isinstance(node, Variable):
        check_Variable(node, env)
    elif isinstance(node, Constant):
        check_Constant(node, env)
    elif isinstance(node, Function):
        check_Function(node, env)
    elif isinstance(node, FunctionParameter):
        check_FunctionParameter(node, env)
    else:
        raise RuntimeError(f"Definition {node} not checked.")


def _checkVariableOrConst(node, env):
    if node.value is not None:
        check(node.value, env)

        if node.type_specified_when_declared:
            if node.value.type != node.type:
                error(f'Variable defined as type {node.type} does not match {node.value.type}')
        else:
            # infer type from value
            node.type = node.value.type

    if node.name in env:
        error(f'Duplicate definition of {node.name}')
    env[node.name] = node


def check_Variable(node, env):
    _checkVariableOrConst(node, env)


def check_Constant(node, env):
    _checkVariableOrConst(node, env)


def check_Function(node, env):
    if node.name in env.maps[0]:
        error(f'Duplicate definition of {node.name}.')
        # and do NOT overwrite it ... originally defined function stays
    else:
        env[node.name] = node

    local_env = env.new_child()
    check(node.parameters, local_env)
    check(node.statements, local_env)


def check_FunctionParameter(node, env):
    if node.name in env.maps[0]:
        error(f'Duplicate definition of {node.name}')
    env[node.name] = node


# Statement Checks
# ================

def check_statement(node, env):
    if isinstance(node, Assignment):
        check_Assignment(node, env)
    elif isinstance(node, Print):
        check_Print(node, env)
    elif isinstance(node, If):
        check_If(node, env)
    elif isinstance(node, While):
        check_While(node, env)
    elif isinstance(node, Break):
        check_Break(node, env)
    elif isinstance(node, Continue):
        check_Continue(node, env)
    elif isinstance(node, Return):
        check_Return(node, env)
    else:
        raise RuntimeError(f"Statement {node} not checked.")


def check_Assignment(node, env):
    check(node.location, env)
    check(node.expression, env)

    # What I expect
    if node.location.type != node.expression.type:
        error(f'Type error on assignment: {node.location.type} != {node.expression.type}')

    # Mutability: let's make assignment responsible for this
    if not node.location.mutable:  # Wishful Thinking Programming!
        error(f"Cannot assign to immutable location: {node.location}")


def check_Print(node, env):
    check(node.expression, env)


def check_If(node, env):
    check(node.test, env)
    if node.test.type != Bool.type:
        error('If test did not evaluate to a Boolean!')
    check(node.consequence, env.new_child())  # Make a new scope (from ChainMap)
    check(node.alternative, env.new_child())


def check_While(node, env):
    check(node.test, env)
    if node.test.type != Bool.type:
        error('If test did not evaluate to a Boolean!')
    check(node.consequence, env.new_child())


def check_Break(node, env):
    # How to check if in loop?
    pass


def check_Continue(node, env):
    # How to check if in loop?
    pass


def check_Return(node, env):
    # How to check if in function?
    check(node.value, env)


def check_Literal(node, env):
    pass


def check_Fetch(node, env):
    pass
