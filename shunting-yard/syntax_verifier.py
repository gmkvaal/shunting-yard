from tokenizer_FSM import tokenizer
from settings import MATH_SYMBOLS
from typing import List


def check_balanced_paranthesis(token_list):
    """Verifies matching number of left and right brackets"""

    if '(' in token_list:
        if token_list.count('(') != token_list.count(')'):
            raise Exception("Unmatching number of left and right paranthesis")


def check_last_token(token_list):
    """Verifies that last token is a right bracket or number"""

    pass


def check_correct_order_of_operators(token_list: List, idx: str):
    """ Called if token is a arithmetic operator. Checks that next is another artithmetic operator
        except + or -
    """

    if token_list[idx + 1] in MATH_SYMBOLS and token_list[idx + 1] not in ['+', '-']:
        raise Exception("Illegal order of operators: {}{}".format(
            token_list[idx], token_list[idx + 1]
        ))

    if token_list[idx - 1] in MATH_SYMBOLS:
        raise Exception("Illegal order of operators: {}{}".format(
            token_list[idx - 1], token_list[idx]
        ))


def check_plus_minus(token_list, sign_change_list, remove_list, idx):
    """ Fixing -- = +"""

    delta_idx = 0
    nmbr_minus = 0

    if token_list[idx + 1] in ['+', '-']:
        while token_list[idx + delta_idx] in ['+', '-']:
            if token_list[idx + delta_idx] == '-':
                nmbr_minus += 1

            delta_idx += 1

        if nmbr_minus % 2 != 0:
            sign_change_list.append(idx)

        for k in range(delta_idx-1):
            remove_list.append(idx + 1 + k)

        return delta_idx
    return 1


def correct_sign(tokens, sign_change_list):

    for idx in sign_change_list:
        if tokens[idx]['name'] == '+':
            tokens[idx]['name'] = '-'
        elif tokens[idx]['name'] == '-':
            tokens[idx]['name'] = '+'
        else:
            raise Exception('Attempting to perform sign change on'
                    'non additive operator: {}'.format(tokens[idx]['name']))


if __name__ == '__main__':

    input_string = '2**+---+2'
    tokens = tokenizer(input_string)

    sign_change_list = []
    remove_list = []

    token_list = [token['name'] for token in tokens]

    idx = 0;
    while True:
        delta_idx = 1

        if token_list[idx] in ['+', '-']:
            delta_idx = check_plus_minus(token_list, sign_change_list, remove_list, idx)

        if token_list[idx] in MATH_SYMBOLS and token_list[idx] not in ['+', '-']:
            check_correct_order_of_operators(token_list, idx)

        idx += delta_idx

        if idx == len(token_list):
            break

    if len(sign_change_list) > 0:
        correct_sign(tokens, sign_change_list)

    for idx in remove_list[::-1]:
        print(idx)
        tokens.pop(idx)

    token_list = [token['name'] for token in tokens]

    print(token_list)


    tokens_corrected = []








    #check_balanced_paranthesis(token_list)
