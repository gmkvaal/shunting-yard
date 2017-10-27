import math as pymath

pymath_operators = tuple(key for key in pymath.__dict__ if '_' not in key)
builtin_operators = ('min', 'max', 'abs')

OPERATOR_LIST = pymath_operators + builtin_operators
MATH_SYMBOLS = ('+', '-', '*', '**', '/', '//', '%', '(', ')')

OPERATOR_PRECEDENCE = {
                       '**': 1,
                       '-u': 2,
                       '*': 3,
                       '/': 3,
                       '%': 3,
                       '//': 3,
                       '+': 4,
                       '-': 4
                       }

OPERATOR_ASSOCIATIVITY = {
                          '**': 'RIGHT',
                          '-u': 'RIGHT',
                          '*': 'LEFT',
                          '/': 'LEFT',
                          '%': 'LEFT',
                          '//': 'LEFT',
                          '+': 'LEFT',
                          '-': 'LEFT',
                          }
