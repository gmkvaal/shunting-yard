from parser_FSM import tokenizer
from typing import List
from collections import namedtuple


StateRet = namedtuple('StateRet', ['next_state', 'increment'])


def classify_token(token: dict, operator_stack: List[str], output_queue: List[str]) -> StateRet:

    if token['type'] == 'NUMBER':
        output_queue.append(token)
        return StateRet(classify_token, True)

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
           and operator_stack[-1]['associativity'] == 'LEFT'):

        output_queue.append(operator_stack.pop())
        return StateRet(pop_operators, True)

    else:
        operator_stack.append(token)
        return StateRet(classify_token, True)


def left_bracket(token: dict, operator_stack: List[str], output_queue: List[str]) -> StateRet:

    pass


def left_bracket(token: dict, operator_stack: List[str], output_queue: List[str]) -> StateRet:

    pass


def empty_operator_stack(operator_stack: List[str], output_queue: List[str]) -> None:
    """ Pops remaining operators from the operator stack to the output queue"""

    while len(operator_stack) > 0:
        output_queue.append(operator_stack.pop())


def shunting_yard(input_string):

    operator_stack = []
    output_queue = []
    token_list = tokenizer(input_string)

    state = classify_token

    idx = 0
    while True:
        token = token_list[idx]
        return_state = state(token, operator_stack, output_queue)

        if return_state.increment:
            idx += 1

        state = return_state.next_state

        if idx == len(token_list):

            empty_operator_stack(operator_stack, output_queue)

            break

    print([token['name'] for token in output_queue])

if __name__ == '__main__':

    input_string = '3/4*2'
    shunting_yard(input_string)

        
