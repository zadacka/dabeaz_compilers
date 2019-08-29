from compilers.wabbit.check import check_program
from compilers.wabbit.ircode import generate_ircode
from compilers.wabbit.model import Print, BinaryOperator, Integer, UnaryOperator, Float
from compilers.wabbit.wasm import WasmEncoder, i32, f64

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
check_program(program)  # side effect: fill in types (which we will need when generating IR code)
ircode = generate_ircode(program)

encoder = WasmEncoder()

# Declare the runtime function
encoder.import_function("runtime", "_printi", [i32], [])
encoder.import_function("runtime", "_printf", [f64], [])

# Encode main(). Note: Return type changed to [].
encoder.encode_function("main", [], [], [], ircode)
with open('test_ir_out.wasm', 'wb') as file:
    file.write(encoder.encode_module())