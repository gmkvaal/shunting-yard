from Parser import parser


class Shunting_yard:
    """ A class for converting to reverse polish notation

     Takes list of tokens as input, returns tokens sorted in list
     """

    def __init__(self, input_list_of_tokens):
        self.input_list_of_tokens = input_list_of_tokens

    def sort_tokens(self):
        """ Tokens of a input string according to the shunting yard algorithm (ref. Wikipedia) """

        precedence_dict = {
            '^': [4, 'right'],
            '*': [3, 'left'],
            '/': [3, 'left'],
            '+': [2, 'left'],
            '-': [2, 'left']
        }

        output_queue = []
        operator_stack = []

        for token in self.input_list_of_tokens:

            print('token:', token, 'output:', output_queue, 'stack:', operator_stack)

            if token.isdigit():
                # If token is a number: append to output"""
                float(token)
                output_queue.append(token)

            else:
                # If not a number
                if token in precedence_dict.keys():

                    print('token is in precedence list', token)

                    # If operator stack is empty: append to operator stack
                    if len(operator_stack) == 0:
                        operator_stack.append(token)

                    else:
                        # If top of stack is a right '(': append to operator stack
                        if operator_stack[-1] == '(':
                            operator_stack.append(token)

                        # If token is right associative: append to operator stack
                        elif precedence_dict[token][1] == 'right':
                            operator_stack.append(token)

                        # If token has higher precedence than top of stack and is left assoc: append to operator stack
                        elif (precedence_dict[token][0] > precedence_dict[operator_stack[-1]][0]
                                and precedence_dict[token][1] == 'left'):
                            operator_stack.append(token)

                        else:
                            # If lower than equal precedence, pop from stack to output queue
                            # and procede until reaching lower precedence, empty stack,
                            # or a left bracket
                            while precedence_dict[token] <= precedence_dict[operator_stack[-1]]:
                                output_queue.append(operator_stack.pop())
                                if len(operator_stack) == 0 or operator_stack[-1] == '(':
                                    break
                            operator_stack.append(token)

                else:

                    print('token is NOT in precedence list', token)


                    # If token is a '(': append to stack
                    if token == '(':
                        operator_stack.append(token)

                    # If token is a ')' pop from stack to output queue until '(' is reached and poped
                    elif token == ')':
                        while operator_stack[-1] is not '(':
                            output_queue.append(operator_stack.pop())
                        operator_stack.pop()

                        if operator_stack[-1] not in precedence_dict.keys():
                            output_queue.append(operator_stack.pop())

                    # If the len of the not number token is 1, it is a algebraic variable (a, x, etc... )
                    elif len(token) == 1:
                        output_queue.append(token)

                    # If token is not a number, math symbol, or bracket, it is a function or operator
                    else:
                        operator_stack.append(token)

        # Poping remaining tokens from stack to output queue
        while len(operator_stack) > 0:
            output_queue.append(operator_stack.pop())

        return output_queue

    def output_queue_list_2_string(self):
        """ Takes list of tokes and joins to string without spaces """

        return ''.join(self.sort_tokens())

    def print_output(self):
        """ Prints the output """

        print('\n', self.output_queue_list_2_string())

def read_input_string():
    print("Rules: \n multiply: * \n division: / \n power: ^ \n ")
    print("Multiplication with unknown variables must be done as '2*x' not '2x'")
    return str(input("Enter an expression to be converted into RPN:"))


if __name__ == '__main__':

    #input_str = "3+4*2/(1-5)^2^3"
    #input_str = 'sin(max(2,3)/3*3.1415)'
    #input_str = '2+(3*(2+3))'
    #input_str = 'sin(3)'
    input_str = "2*2*a*a"
    #input_str = "sin(2a)"
    #input_str = "sin(2a)"


    #input_str = read_input_string()


    input_list = parser(input_str)
    sy = Shunting_yard(input_list)

    #output_list = sy.split_input_with_functions()
    #print(output_list)

    #sy.sort_tokens()
    sy.print_output()
