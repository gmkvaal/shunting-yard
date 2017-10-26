from states import start_state
from token_classifier import append_token


def tokenizer(input_string):
    """Splits an input string into list of tokens by  finite state machine algorithm

    Args:
        input_string: String to be parsed.

    Returns:
        List of tokens.
    """

    stack = []
    output_list = []
    state = start_state

    idx = 0
    while True:
        char = input_string[idx]
        return_state = state(char, stack)

        # print(char, state.__name__, stack)

        if return_state.increment:
            idx += 1

        if return_state.done:

            # print('appending', stack)

            append_token(stack, state, output_list)
            stack = []

        if idx == len(input_string):
            if not return_state.done:
                if stack[-1].isdigit() or stack[-1] == ")":
                    append_token(stack, return_state.next_state, output_list)
                else:
                    raise Exception('Ending expression with non-digit nor right parenthesis')
            break

        state = return_state.next_state

    return output_list


if __name__ == '__main__':

    # input_string = "cos(2)"
    input_string = '2*-(---2--1)'

    print(tokenizer(input_string))

    print([token['name'] for token in tokenizer(input_string)])
