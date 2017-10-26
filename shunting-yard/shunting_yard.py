from parser_FSM import tokenizer
from typing import List
from collections import namedtuple


StateRet = namedtuple('StateRet', ['next_state', 'increment'])


def classify_token(token: dict, operator_stack: List[str], output_queue: List[str]) -> StateRet:

    if token['type'] == 'NUMBER':
        output_queue.append(token)
        return StateRet(classify_token, False)

    if token['type'] == 'OPERATOR':
        return StateRet(operator, False)

    if token['type'] == 'LEFT_BRACKET':
        return StateRet(operator, False)

    if token['type'] == 'RIGHT_BRACKET':
        return StateRet(operator, False)


def number(token: dict, operator_stack: List[str], output_queue: List[str]) -> StateRet:

    return StateRet(num_pre_dot_state, True)


def operator(token: dict, operator_stack: List[str], output_queue: List[str]) -> StateRet:

    if len(operator_stack) == 0:
        operator_stack.append(token)
        return StateRet(classify_token, True)

    else:
        return StateRet(pop_operators, False)


def pop_operators(token: dict, operator_stack: List[str], output_queue: List[str]) -> StateRet:

    if (len(operator_stack) > 0
           and operator_stack[-1]['precedence'] >= token['precedence']
           and operator_stack[-1]['assiciativity'] == 'LEFT'):

        output_queue(operator_stack.pop())
        return StateRet(pop_operators, False)

    else:
        operator_stack.append(token)
        return StateRet(classify_token, False)





    else:
        return StateRet(pop_operators, False)

    pass


def left_bracket(token: dict, operator_stack: List[str], output_queue: List[str]) -> StateRet:

    pass


def left_bracket(token: dict, operator_stack: List[str], output_queue: List[str]) -> StateRet:

    pass


def shunting_yard(input_string):

    operator_stack = []
    output_queue = []

    input_string = '2+2'

    token_list = tokenizer(input_string)

    idx = 0
    while True:

        token_dict = token_list[idx]
        token = token_dict['name']

        print(token_dict)

        idx += 1
        if idx == len(token_list):
            break


if __name__ == '__main__':

    pass


        
