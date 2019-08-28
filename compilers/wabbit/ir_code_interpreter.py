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

# compare with ceval.c in cython - not too dissimilar!
class Interpreter:
    def __init__(self):
        self.stack = []   # IR is for a 'stack machine'
        self.memory = {}  # Variables
        self.pc = 0       # Program counter, current instruction being executed

    def run(self, instructions):
        self.pc = 0
        while self.pc < len(instructions):
            opcode, *args = instructions[self.pc]  # Get the instruction
            self.pc += 1
            getattr(self, f'run_{opcode}')(*args)  # Run the instruction

    def push(self, item):
        self.stack.append(item)

    def pop(self):
        return self.stack.pop()

    def run_GLOBALI(self, name):
        """ Declares a new variable """
        self.memory[name] = None

    def run_ADDI(self):
        right = self.pop()
        left = self.pop()
        self.push(right + left)

    def run_STORE(self, name):
        """ Stack -> Memory """
        value = self.pop()
        self.memory[name] = value

    def run_PRINTI(self):
        """ Print what is on the top of the stack """
        print(self.stack.pop())

    def run_MULI(self):
        right = self.pop()
        left = self.pop()
        self.push(left * right)

    def run_LOAD(self, name):
        """ Memory -> Stack """
        self.push(self.memory[name])

    def run_CONSTI(self, const):
        """ Put a constant value on the stack"""
        self.push(const)


interp = Interpreter()
interp.run(code)