# wasm.py
#
# This file emits Wasm code from IR code.  To do this, you must first
# work through the Wasm encoding example found in Docs/codegen.html.
# Take the code from that example and copy it in here.  You will then
# adapt it to work with Wabbit.
#
# Specific changes/extensions you will need to address:
#
# 1. Floating point operations.
# 2. Comparisons and relations.
# 3. Support for local variables (load/store).
# 4. Control flow (if, while, etc.)
# 5. Additional runtime functions (_printf, _printb).
# 6. Memory management (eventually)
#
# Most of the hard work of encoding should have been completed in the
# Docs/codegen.html example.  You'll mostly be adding support for more
# opcodes and patching things up to bridge IR Code with the Wasm
# encoder.  



import struct

code = [
    ('GLOBALI', 'x'),
    ('CONSTI', 4),
    ('STORE', 'x'),
    ('GLOBALI', 'y'),
    ('CONSTI', 5),
    ('STORE', 'y'),
    ('GLOBALI', 'd'),
    ('LOAD', 'x'),
    ('LOAD', 'x'),
    ('MULI',),
    ('LOAD', 'y'),
    ('LOAD', 'y'),
    ('MULI',),
    ('ADDI',),
    ('STORE', 'd'),
    ('LOAD', 'd'),
    ('PRINTI',)
]


# Challenge: Compile to Wasm and load it in the browser
# What if you had a tiny stack machine with a CPU and four datatypes

# A C extension to Python is like a 'new opcode'
# ... but this is more basic. It doesn't have any IO
# ... it is just like a mini-CPU embedded in JavaScript
# You could have a Python Byte Array, run your code (doing stuff)
# ... and then, *presto* you have gone and populated the bytearray with stuff!

def encode_unsigned(value):
    """
    Produce an LEB128 encoded unsigned integer.
    """
    parts = []
    while value:
        parts.append((value & 0x7f) | 0x80)
        value >>= 7
    if not parts:
        parts.append(0)
    parts[-1] &= 0x7f
    return bytes(parts)


def encode_signed(value):
    """
    Produce a LEB128 encoded signed integer.
    """
    parts = []
    if value < 0:
        # Sign extend the value up to a multiple of 7 bits
        value = (1 << (value.bit_length() + (7 - value.bit_length() % 7))) + value
        negative = True
    else:
        negative = False
    while value:
        parts.append((value & 0x7f) | 0x80)
        value >>= 7
    if not parts or (not negative and parts[-1] & 0x40):
        parts.append(0)
    parts[-1] &= 0x7f
    return bytes(parts)


def encode_f64(value):
    """
    Encode a 64-bit float point as little endian
    """
    return struct.pack('<d', value)


def encode_vector(items):
    """
    A size-prefixed collection of objects.  If items is already
    bytes, it is prepended by a length and returned.  If items
    is a list of byte-strings, the length of the list is prepended
    to byte-string formed by concatenating all of the items.
    """
    if isinstance(items, bytes):
        return encode_unsigned(len(items)) + items
    else:
        return encode_unsigned(len(items)) + b''.join(items)


def encode_signature(argtypes, rettypes):
    return b'\x60' + encode_vector(argtypes) + encode_vector(rettypes)


def encode_section(sectnum, contents):
    return bytes([sectnum]) + encode_unsigned(len(contents)) + contents

def encode_name(name):
    """
    Encode a text name as a UTF-8 vector
    """
    return encode_vector(name.encode('utf-8'))


assert encode_unsigned(624485) == bytes([0xe5, 0x8e, 0x26])
assert encode_unsigned(127) == bytes([0x7f])
assert encode_signed(-624485) == bytes([0x9b, 0xf1, 0x59])
assert encode_signed(127) == bytes([0xff, 0x00])

INSTRUCTION_NOOP = b'\x01'  # Check: may mean something else as a type?!

INSTRUCTION_END = b'\x0b'
INSTRUCTION_GLOBAL_SET = b'\x24'
INSTRUCTION_GLOBAL_GET = b'\x23'

INSTRUCTION_i32_CONST = b'\x41'

INSTRUCTION_i32_MUL = b'\x6c'
INSTRUCTION_i32_ADD = b'\x6a'


# wtype - WASM value types:
i32 = b'\x7f'  # Wabbit uses 32 bit ints.
i64 = b'\x7e'
f32 = b'\x7d'
f64 = b'\x7c'

class WasmEncoder:
    def __init__(self):
        # Globals
        self.globals = {}       # the names
        self.global_defns = []  # the reality / storage (a vector)

        # Function information
        self.signatures = []   # A vector of the signatures
        self.functions = {}    # A map of names -> signature index
        self.func_code = []    # A vector of function code objects
        self.exports = []      # Functions for the outside world

    def encode_function(self, name, parmnames, parmtypes, rettypes, code):
        sig = encode_signature(parmtypes, rettypes)
        self.signatures.append(sig)
        self.functions[name] = len(self.signatures) - 1
        self.exports.append(encode_name(name) + b'\x00'
                            + encode_unsigned(self.functions[name]))

        self.locals = {}       # A map of local variable names into definition index
        self.local_defns = []  # Additional local variables created in body
        for n, pname in enumerate(parmnames):
            self.locals[pname] = n

        self.wcode = b''  # Wasm instruction code that we are generating
        for op, *opargs in code:
            getattr(self, f'encode_{op}')(*opargs)

        # Put a block terminator on the code
        self.wcode += INSTRUCTION_END

        fcode = encode_vector(self.local_defns) + self.wcode
        encoded_size_of_fcode = encode_unsigned(len(fcode))
        self.func_code.append(encoded_size_of_fcode + fcode)

    def encode_module(self):
        module = b'\x00asm\x01\x00\x00\x00'
        module += encode_section(1, encode_vector(self.signatures))
        vec = [encode_unsigned(v) for v in self.functions.values()]
        module += encode_section(3, encode_vector(vec))
        module += encode_section(6, encode_vector(self.global_defns))
        module += encode_section(7, encode_vector(self.exports))
        module += encode_section(10, encode_vector(self.func_code))
        return module

    def encode_CONSTI(self, value):
        self.wcode += INSTRUCTION_i32_CONST + encode_signed(value)

    def encode_ADDI(self):
        self.wcode += INSTRUCTION_i32_ADD  # i32.add

    def encode_MULI(self):
        self.wcode += INSTRUCTION_i32_MUL  # i32.mul

    def encode_PRINTI(self):
        # TO-DO
        pass

    def encode_LOCALI(self):
        # Create a local variable
        # Will add to self.local_defns
        # Will add name entry to self.locals
        pass

    def encode_GLOBALI(self, name):
        # \x01 -> mutability of 'mutable'
        # \x41 -> 'const', this is actually part of the initial value

        # Initial value = 0
        defn = i32 + INSTRUCTION_NOOP + INSTRUCTION_i32_CONST + encode_signed(0) + INSTRUCTION_END
        self.global_defns.append(defn)
        self.globals[name] = len(self.global_defns) - 1  # index of our global

    def encode_STORE(self, name):
        index = self.globals[name]
        self.wcode += INSTRUCTION_GLOBAL_SET + encode_unsigned(index)

    def encode_LOAD(self, name):
        index = self.globals[name]
        self.wcode += INSTRUCTION_GLOBAL_GET + encode_unsigned(index)


encoder = WasmEncoder()
encoder.encode_function("main", [], [], [i32], code)
with open('out.wasm', 'wb') as file:
    file.write(encoder.encode_module())
