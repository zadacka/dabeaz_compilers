from compilers.wabbit.check import check_program
from compilers.wabbit.ircode import generate_ircode
from compilers.wabbit.model import Print, BinaryOperator, Integer, UnaryOperator, Float
from compilers.wabbit.wasm import WasmEncoder, i32

# code = [
#     ('GLOBALI', 'x'),
#     ('CONSTI', 4),
#     ('STORE', 'x'),
#     ('GLOBALI', 'y'),
#     ('CONSTI', 5),
#     ('STORE', 'y'),
#     ('GLOBALI', 'd'),
#     ('LOAD', 'x'),
#     ('LOAD', 'x'),
#     ('MULI',),
#     ('LOAD', 'y'),
#     ('LOAD', 'y'),
#     ('MULI',),
#     ('ADDI',),
#     ('STORE', 'd'),
#     ('LOAD', 'd'),
#     ('PRINTI',)
# ]

program = [
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
]
check_program(program)  # side effect: fill in types (which we will need when generating IR code)
ircode = generate_ircode(program)

encoder = WasmEncoder()
encoder.encode_function("main", [], [], [i32], ircode)
with open('test_ir_out.wasm', 'wb') as file:
    file.write(encoder.encode_module())