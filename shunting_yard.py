#import shlex
#import re

class Shunting_yard:
    """ A class for converting to reverse polish notation """

    def __init__(self, input_string):
        self.input_string = input_string


    def read_input_string(self):
        pass

    # Old parser method
    #def split_input_string(self):
    #    """Split string of input tokens into a list each token using the shlex module"""
    #
    #    token_list = shlex.shlex(self.input_string)
    #    return token_list


    def split_input_string_with_regex(self):
        """Not complete"""

        return re.findall(r"[-+]?\d*\.\d+|\d+", self.input_string)


    def split_input_with_functions(self):
        """ Performs the shunting yard algorithm on tokens separated as list indices"""

        math_sym_list = ['+', '-', '*', '/', '^', '(', ')']
        output_list = []
        temp_variable = None

        for symbol in self.input_string:
            if symbol == ',':
                output_list.append(temp_variable)
                temp_variable = None

            elif symbol == '.':
                try:
                    int(temp_variable)
                    temp_variable += symbol
                except ValueError:
                    print("Invalid: '.' after non number symbol")

            elif symbol in math_sym_list:
                if temp_variable != None:
                    output_list.append(temp_variable)
                    temp_variable = None
                output_list.append(symbol)

            else:
                try:
                    # If symbol is a number: append to output"""
                    int(symbol)
                    if temp_variable == None:
                        temp_variable = symbol

                    else:
                        temp_variable += symbol

                except ValueError:
                    # If symbol is neither a mathematical symbol or a number
                    if temp_variable == None:
                        temp_variable = symbol

                    else:
                        try:
                            # If temp_variable is a int, append it to output_list and update temp variable
                            int(temp_variable)
                            output_list.append(temp_variable)
                            temp_variable = symbol

                        except ValueError:
                            # If temp variable is a letter, add to temp variable
                            temp_variable += symbol

        if temp_variable != None:
            output_list.append(temp_variable)

        return(output_list)

    def sort_tokens(self):
        """ Tokens of a input string according to the shunting yard algorithm (ref. Wikipedia) """

        precedence_dict = {
            '^': [4, "right"],
            '*': [3, "left"],
            '/': [3, "left"],
            '+': [2, "left"],
            '-': [2, "left"]
        }

        output_queue = []
        operator_stack = []

        for token in self.split_input_with_functions():

            print("token:", token, "output:", output_queue, "stack:", operator_stack)

            try:
                # If token is a number: append to output"""
                float(token)
                output_queue.append(token)

            except ValueError:
                # If not a number
                if token in precedence_dict.keys():
                    # If operator stack is empty: append to operator stack
                    if len(operator_stack) == 0:
                        operator_stack.append(token)

                    else:
                        # If top of stack is a right '(': append to operator stack
                        if operator_stack[-1] == "(":
                            operator_stack.append(token)

                        # If token is right associative: append to operator stack
                        elif precedence_dict[token][1] == "right":
                            operator_stack.append(token)

                        # If token has higher precedence than top of stack and is left assoc: append to operator stack
                        elif (precedence_dict[token][0] > precedence_dict[operator_stack[-1]][0]
                                and precedence_dict[token][1] == "left"):
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
                    # If token is a '(': append to stack
                    if token == "(":
                        operator_stack.append(token)

                    # If token is a ')' pop from stack to output queue until '(' is reached and poped
                    elif token == ")":
                        while operator_stack[-1] is not "(":
                            output_queue.append(operator_stack.pop())
                        operator_stack.pop()

                        if operator_stack[-1] not in precedence_dict.keys():
                            output_queue.append(operator_stack.pop())

                    # If token is not a number, math sym, or bracket, it is a function (or operator?)
                    else:
                       operator_stack.append(token)

        # Poping remaining tokens from stack to output queue
        while len(operator_stack) > 0:
            output_queue.append(operator_stack.pop())

        return output_queue


    def output_queue_list_2_string(self, output_queue_list):
        """ Takes list of tokes and joins to string without spaces"""

        return ''.join(output_queue_list)


if __name__ == '__main__':

    #input = "3+4*2/(1-5)^2^3"
    #input = 'sin(max(2,3)/3*3.1415)'
    #input = '2+(3*(2+3))'
    #input = 'sin(3)'
    #input = "22+2a"
    #input = "sin(2a)"
    input = "sin(2a)"

    sy = Shunting_yard(input)

    output_list = sy.split_input_with_functions()
    print(output_list)

    output_queue_list = sy.sort_tokens()

    print(sy.output_queue_list_2_string(output_queue_list))

    #print(input)