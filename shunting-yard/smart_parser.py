
def digit_or_dot(a):
    if a.isdigit():
        return True
    if a == '.':
        return True
    else:
        return False


class SmartParser:

    def __init__(self, input_string):

        self.input_string = input_string
        self.math_sym_list = ('+', '-', '*', '/', '**', '(', ')')
        self.function_list = ('sin', 'cos')
        self.output_list = []

    def append_type_to_output_list(self, name, value, token_type):

        self.output_list.append({'name': str(name),
                                    'value': value,
                                    'type': token_type
                                    }
                                    )

    def tokenize(self):

        temp_symbol = None

        i = 0
        len_str = len(self.input_string)

        while i < len_str:
            # If digit or dot, read until no longer, then append.
            if digit_or_dot(self.input_string[i]):
                j = 0
                while i+j < len_str and digit_or_dot(self.input_string[i+j]):

                    from typing import Any, Tuple, List

                    from collections import namedtuple

                    StateRet = namedtuple('StateRet', ['next_state', 'done', 'increment'])

                    def start(c: str, stack: List[str]) -> StateRet:
                        """
                        Returns:
                            Tuple of next state, if the stack is ready, if the read head should increment
                        """
                        if c in {'+', '-'}:
                            stack.append(c)
                            return StateRet(start, True, True)
                        elif c in {'1', '2', '3', '4', '5', '6', '7', '8', '9', '0'}:
                            stack.append(c)
                            return StateRet(num_state, False, True)
                        else:
                            raise ValueError()

                    def num_state(c: str, stack: List[str]) -> StateRet:
                        if c in {'1', '2', '3', '4', '5', '6', '7', '8', '9', '0'}:
                            stack.append(c)
                            return StateRet(num_state, False, True)
                        elif c in {'+', '-'}:
                            return StateRet(start, True, False)
                        else:
                            raise ValueError()

                    if __name__ == '__main__':
                        inp = input('>>> ')

                        inp_ptr = 0
                        state = start
                        stack = []

                        while True:
                            c = inp[inp_ptr]

                            state_return = state(c, stack)
                            state = state_return.next_state

                            if state_return.increment:
                                inp_ptr += 1

                            if state_return.done or len(inp) == inp_ptr:
                                print(''.join(stack))
                                stack = []
                                if len(inp) == inp_ptr:
                                    break
                    if temp_symbol is None:
                        temp_symbol = self.input_string[i + j]
                    else:
                        temp_symbol += self.input_string[i + j]

                    j += 1

                #self.output_list.append(temp_symbol)
                self.append_type_to_output_list(temp_symbol, temp_symbol, 'NUMBER')
                temp_symbol = None
                i += j - 1

            else:
                for sym in self.math_sym_list:
                    if sym == input_string[i:i + len(sym)]:
                        #if temp_symbol is not None:
                        #    self.append_type_to_output_list(temp_symbol, temp_symbol, 'NUMBER')

                        self.append_type_to_output_list(sym, sym, 'OPERATOR')
                        i += len(sym) - 1

            i += 1

        #if temp_symbol is not None:
        #    self.output_list.append(temp_symbol)

        print(self.output_list)










if __name__ == '__main__':

    input_string = "22*22.2"
    SmartParser(input_string).tokenize()