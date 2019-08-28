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

class Transpiler:
    def __init__(self):
        self.stack = []   # IR is for a 'stack machine'
        self.source = ""

    def translate(self, instructions):
        for opcode, *args in instructions:
            getattr(self, f'translate_{opcode}')(*args)

    def push(self, item):
        self.stack.append(item)

    def pop(self):
        return self.stack.pop()

    def translate_GLOBALI(self, name):
        # self.source += f'{name} = None\n'
        pass

    def translate_ADDI(self):
        right = self.pop()
        left = self.pop()
        self.push(f'({right} + {left})')

    def translate_STORE(self, name):
        self.source += f'{name} = {self.pop()}\n'

    def translate_PRINTI(self):
        self.source += f'print({self.   pop()})\n'

    def translate_MULI(self):
        right = self.pop()
        left = self.pop()
        self.push(f'({left} * {right})')

    def translate_LOAD(self, name):
        self.push(name)

    def translate_CONSTI(self, value):
        self.push(str(value))


transpiler = Transpiler()
transpiler.translate(code)
print(transpiler.source)

# Expressions represent values
# The stack
# Statements (assignment) manipulate