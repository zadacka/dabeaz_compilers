from time import sleep

from compilers.wabbit.check import check_program
from compilers.wabbit.ircode import generate_ircode
from compilers.wabbit.parse import Parser
from compilers.wabbit.tokenizer import tokenize
from compilers.wabbit.wasm import WasmEncoder, i32, f64

with open('../Tests/inttest.wb') as f:
    input_wabbit_code = f.read()

for token in tokenize(input_wabbit_code):
    print(token)
sleep(0.2)
tokens = tokenize(input_wabbit_code)
parsed_tokens = Parser(tokens).parse_statements()
check_program(parsed_tokens)
ircode = generate_ircode(parsed_tokens)

encoder = WasmEncoder()
# Declare the runtime function
encoder.import_function("runtime", "_printi", [i32], [])
encoder.import_function("runtime", "_printf", [f64], [])
encoder.encode_function("main", [], [], [], ircode)
with open('test_ir_out.wasm', 'wb') as file:
    file.write(encoder.encode_module())

