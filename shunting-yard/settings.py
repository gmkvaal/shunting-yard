import math as pymath

pymath_operators = (key for key in pymath.__dict__ if '_' not in key)
builtin_operators = ('min', 'max', 'abs')

OPERATOR_LIST = []
for operator in pymath_operators:
    OPERATOR_LIST.append(operator)

for operator in builtin_operators:
    OPERATOR_LIST.append(operator)

OPERATOR_LIST = tuple(OPERATOR_LIST)
MATH_SYMBOLS = ('+', '-', '*', '**', '/', '//', '%', '(', ')')
