from compilers.programs import Constant, Variable, Float, Assignment, NamedLocation, BinaryOperator, Print, program1, \
    Integer, If
from compilers.wabbit.check import check_program
from compilers.wabbit.ircode import generate_ircode
from compilers.wabbit.wasm import WasmEncoder, i32, f64

program = [
    Variable('a', Integer(2), Integer.type),
    Variable('b', Integer(3), Integer.type),
    If(
        BinaryOperator('<', NamedLocation('a'), NamedLocation('b')),
        [Print(NamedLocation('a')), ],
        [Print(NamedLocation('b')), ],
    )
]

check_program(program)  # side effect: fill in types (which we will need when generating IR code)
ircode = generate_ircode(program)

for line in ircode:
    print(line)

encoder = WasmEncoder()

# Declare the runtime function
encoder.import_function("runtime", "_printi", [i32], [])
encoder.import_function("runtime", "_printf", [f64], [])

# Encode main(). Note: Return type changed to [].
encoder.encode_function("main", [], [], [], ircode)
with open('test_ir_out.wasm', 'wb') as file:
    file.write(encoder.encode_module())

for line in encoder._wcode:
    print(line)
