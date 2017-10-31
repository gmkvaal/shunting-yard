from typing import List
from collections import namedtuple

from .tokenizer import tokenizer


StateRet = namedtuple('StateRet', ['next_state', 'increment'])


def classify_token(token: dict, operator_stack: List[str], output_queue: List[str]) -> StateRet:
    """Classifies tokens

    Args:
        char: Currently read token.
        operator_stack: Stack of operators
        output_queue: Tokens in RPN order

    Returns:
        Tuple of: Next state, if increment

    """

    print(token['name'], [operator['name'] for operator in output_queue],
          [operator['name'] for operator in operator_stack])

    if token['type'] == 'NUMBER':
        output_queue.append(token)
        return StateRet(classify_token, True)

    if token['type'] == 'OPERATOR':
        return StateRet(operator, False)

    if token['type'] == 'FUNCTION':
        operator_stack.append(token)
        return StateRet(classify_token, True)

    if token['type'] == 'LEFT_PARENTHESIS':
        operator_stack.append(token)
        return StateRet(classify_token, True)

    if token['type'] == 'RIGHT_PARENTHESIS':
        return StateRet(right_parenthesis, False)

    if token['type'] == 'SKIP':
        return StateRet(classify_token, True)


def operator(token: dict, operator_stack: List[str], output_queue: List[str]) -> StateRet:
    """Called when a token is classified as an operator

    Appends to stack of the operator stack is empty, if the last token
    in the stack is a function, or if the token is right associative.
    Else, pops operators from the stack

    Args:
        char: Currently read token.
        operator_stack: Stack of operators
        output_queue: Tokens in RPN order

    Returns:
        Tuple of: Next state, if increment

    """

    del output_queue # Not used in this state

    if len(operator_stack) == 0 or operator_stack[-1]['precedence'] is None:
        operator_stack.append(token)
        return StateRet(classify_token, True)

    elif token['associativity'] == 'RIGHT':
        operator_stack.append(token)
        return StateRet(classify_token, True)

    else:
        return StateRet(pop_operators, False)


def pop_operators(token: dict, operator_stack: List[str], output_queue: List[str]) -> StateRet:
    """Pops operators from the stack

    Operators are popped from the operator stack to the output queue
    until reaching an operator with lower precedence or the stack is empty

    Args:
        char: Currently read token.
        operator_stack: Stack of operators
        output_queue: Tokens in RPN order

    Returns:
        Tuple of: Next state, if increment

    """
    if (len(operator_stack) > 0
            and operator_stack[-1]['precedence'] is not None
            and operator_stack[-1]['precedence'] >= token['precedence']
            and operator_stack[-1]['associativity'] == 'LEFT'):

        output_queue.append(operator_stack.pop())
        return StateRet(pop_operators, False)

    else:
        operator_stack.append(token)
        return StateRet(classify_token, True)


def right_parenthesis(token: dict, operator_stack: List[str], output_queue: List[str]) -> StateRet:
    """Called when a token is classified as a right parenthesis

    Operators are popped from the operator stack to the output queue
    until reaching a left parenthesis

    Args:
        char: Currently read token.
        operator_stack: Stack of operators
        output_queue: Tokens in RPN order

    Returns:
        Tuple of: Next state, if increment

    """

    del token # Not used in this state

    if operator_stack == []:
        raise Exception('Mismatching parentheses')

    elif operator_stack[-1]['type'] != 'LEFT_PARENTHESIS':
        output_queue.append(operator_stack.pop())
        return StateRet(right_parenthesis, False)

    else:
        operator_stack.pop()
        return StateRet(post_right_parenthesis, False)


def post_right_parenthesis(token: dict, operator_stack: List[str], output_queue: List[str]) -> StateRet:
    """Called after brackets are matched

    If a function is atop of the stack it is poped to the output queue

    Args:
        char: Currently read token.
        operator_stack: Stack of operators
        output_queue: Tokens in RPN order

    Returns:
        Tuple of: Next state, if increment

    """

    if len(operator_stack) > 0 and operator_stack[-1]['type'] == 'FUNCTION':
        output_queue.append(operator_stack.pop())

    return StateRet(classify_token, True)


def empty_operator_stack(operator_stack: List[str], output_queue: List[str]) -> None:
    """ Pops remaining operators from the operator stack to the output queue

    Args:
        char: Currently read token.
        operator_stack: Stack of operators
        output_queue: Tokens in RPN order
    """

    while len(operator_stack) > 0:
        output_queue.append(operator_stack.pop())


def shunting_yard(input_string: str) -> List[str]:
    """ Engine of shunting yard parser finite state machine algorithm

    Args:
        input_string: A mathematical expression

    Returns:
        A list of tokens ordered in Reverse Polish Notation

    """


    operator_stack = []
    output_queue = []
    token_list = tokenizer(input_string)

    state = classify_token

    idx = 0
    while True:
        token = token_list[idx]

        #print(token['name'], state.__name__, operator_stack)

        return_state = state(token, operator_stack, output_queue)

        if return_state.increment:
            idx += 1

        state = return_state.next_state

        if idx == len(token_list):

            empty_operator_stack(operator_stack, output_queue)

            break

    return output_queue



        
