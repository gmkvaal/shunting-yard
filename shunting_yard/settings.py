import math as pymath

pymath_operators = tuple(key for key in pymath.__dict__ if '_' not in key)
builtin_operators = ('min', 'max', 'abs')
unaries = ('-u',)

FUNCTION_LIST = pymath_operators + builtin_operators
MATH_SYMBOLS = ('+', '-', '*', '**', '/', '//', '%', '(', ')') + unaries

OPERATOR_PRECEDENCE = {
                       '**': 1,
                       '-u': 2,
                       '+': 2,
                       '-': 2,
                       '*': 3,
                       '/': 3,
                       '%': 3,
                       '//': 3
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
