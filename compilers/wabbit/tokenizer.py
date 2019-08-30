# tokenizer.py
r'''
The role of a tokenizer is to turn raw text into recognized symbols 
known as tokens.

The tokenizer for Wabbit is required to recognize the following
symbols.  The suggested name of the token is on the left. The matching
text is on the right.

Identifiers:
    ID      : Text starting with a letter or '_', followed by any number
              number of letters, digits, or underscores.
              Examples:  'abc' 'ABC' 'abc123' '_abc' 'a_b_c'

Literals:
    INTEGER :  123   (decimal)

    FLOAT   : 1.234
              .1234
              1234.

    CHAR    : 'a'     (a single character - byte)
              '\xhh'  (byte value)
              '\n'    (newline)
              '\''    (literal single quote)

Comments:  To be ignored
     //             Skips the rest of the line
     /* ... */      Skips a block (no nesting allowed)

Errors: Your lexer may optionally recognize and report the following
error messages:

     lineno: Illegal char 'c'         
     lineno: Unterminated character constant    
     lineno: Unterminated comment

'''

import re


class Token:
    def __init__(self, type, value):
        self.type = type  # what it is
        self.value = value  # text

    def __repr__(self):
        return f'Token({self.type}, {self.value})'


RESERVED_KEYWORDS = {
    'const': Token('CONST', 'const'),
    'var': Token('VAR', 'var'),
    'print': Token('PRINT', 'print'),
    'return': Token('RETURN', 'return'),
    'break': Token('BREAK', 'break'),
    'continue': Token('CONTINUE', 'continue'),
    'if': Token('IF', 'if'),
    'else': Token('ELSE', 'else'),
    'while': Token('WHILE', 'while'),
    'func': Token('FUNC', 'func'),
    'import': Token('IMPORT', 'import'),
    'true': Token('TRUE', 'true'),
    'false': Token('FALSE', 'false'),
}

known_tokens = {
    # Operators:
    '+': Token('PLUS', '+'),
    '-': Token('MINUS', '-'),
    '*': Token('TIMES', '*'),
    '/': Token('DIVIDE', '/'),
    '<': Token('LT', '<'),
    '<=': Token('LE', '<='),
    '>': Token('GT', '>'),
    '>=': Token('GE', '>='),
    '==': Token('EQ', '=='),
    '!=': Token('NE', '!='),
    '&&': Token('LAND', '&&'),
    '||': Token('LOR', '||'),
    '!': Token('LNOT', '!'),
    '^': Token('GROW', '^'),

    # Miscellaneous Symbols
    '=': Token('ASSIGN', '='),
    ';': Token('SEMI', ';'),
    '(': Token('LPAREN', '('),
    ')': Token('RPAREN', ')'),
    '{': Token('LBRACE', '{'),
    '}': Token('RBRACE', '}'),
    ',': Token('COMMA', ','),
    '`': Token('DEREF', '`')  # Backtick

}

FLOAT_OR_INT_REGEX = re.compile(r"""
            ^         # Start of pattern: don't swallow characters before number!
            \.*       # Floats may start with a decimal point
            [0-9]+    # Then any number of numeric characters
            \.*       # Then maybe a decmial point
            [0-9]*    # Then maybe some more characters
            """, re.VERBOSE)


def tokenize(text):
    index = 0
    while index < len(text):
        # Produce a token

        # Skip white space
        if text[index] in ' \t\n':
            index += 1
            continue

        # Skip Comments
        elif text[index:index + 2] == '/*':
            end = text.find('*/', index + 2)
            if end >= 0:
                index = end + 2
            else:
                print("Unterminated Comment")
                index = len(text)

        # Get names and keywords
        elif re.match(r'[a-zA-Z][a-zA-Z0-9]*', text[index:]):
            m = re.match(r'[a-zA-Z][a-zA-Z0-9]*', text[index:]).group(0)
            if m in RESERVED_KEYWORDS:
                yield RESERVED_KEYWORDS[m]
            else:
                yield Token('NAME', m)
            index += len(m)

        elif FLOAT_OR_INT_REGEX.search(text[index:]):
            match = FLOAT_OR_INT_REGEX.search(text[index:]).group(0)
            decimal_points_found = match.count('.')
            if decimal_points_found == 0:
                yield Token('INT', match)
            elif decimal_points_found == 1:
                yield Token('FLOAT', match)
            else:
                print(f'Bad number found: {match}. Not an Int or a Float')
            index += len(match)

        elif text[index:index + 2] in known_tokens:
            yield known_tokens[text[index:index + 2]]
            index += 2
        elif text[index] in known_tokens:
            yield known_tokens[text[index]]
            index += 1

        else:
            print(f'!! Unknown Token: {text[index]} !!')
            index += 1


if __name__ == '__main__':
    with open('../Tests/mandel.wb') as f:
        for tok in tokenize(f.read()):
            print(tok)
