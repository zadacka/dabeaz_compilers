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


def encode_name(name):
    """
    Encode a text name as a UTF-8 vector
    """
    return encode_vector(name.encode('utf-8'))


assert encode_unsigned(624485) == bytes([0xe5, 0x8e, 0x26])
assert encode_unsigned(127) == bytes([0x7f])
assert encode_signed(-624485) == bytes([0x9b, 0xf1, 0x59])
assert encode_signed(127) == bytes([0xff, 0x00])

INSTRUCTION_NOOP = b'\x01'

INSTRUCTION_END = b'\x0b'
INSTRUCTION_GLOBAL_SET = b'\x24'
INSTRUCTION_GLOBAL_GET = b'\x23'

INSTRUCTION_i32_CONST = b'\x41'

# wtype - WASM value types:
i32 = b'\x7f'  # Wabbit uses 32 bit ints.
i64 = b'\x7e'
f32 = b'\x7d'
f64 = b'\x7c'

class WasmEncoder:
    def encode(self, code):
        self.globals = {}       # the names
        self.globals_defn = []  # the reality / storage (a vector)

        self.wcode = b''  # Wasm instruction code that we are generating
        for op, *opargs in code:
            getattr(self, f'encode_{op}')(*opargs)

        # Put a block terminator on the code
        self.wcode += INSTRUCTION_END

    def encode_CONSTI(self, value):
        self.wcode += INSTRUCTION_i32_CONST + encode_signed(value)

    def encode_ADDI(self):
        self.wcode += b'\x6a'  # i32.add

    def encode_MULI(self):
        self.wcode += b'\x6c'  # i32.mul

    def encode_PRINTI(self):
        # TO-DO
        pass

    def encode_GLOBALI(self, name):
        # \x01 -> mutability of 'mutable'
        # \x41 -> 'const', this is actually part of the initial value

        # Initial value = 0
        defn = i32 + INSTRUCTION_NOOP + INSTRUCTION_i32_CONST + encode_signed(0) + INSTRUCTION_END
        self.globals_defn.append(defn)
        self.globals[name] = len(self.globals_defn) - 1  # index of our global

    def encode_STORE(self, name):
        index = self.globals[name]
        self.wcode += INSTRUCTION_GLOBAL_SET + encode_unsigned(index)

    def encode_LOAD(self, name):
        index = self.globals[name]
        self.wcode += INSTRUCTION_GLOBAL_GET + encode_unsigned(index)


encoder = WasmEncoder()
encoder.encode(code)
print(encoder.wcode)
