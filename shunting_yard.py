import re
import shlex

class Shutting_yard:

    def __init__(self, input_string):
        self.input_string = input_string


    def read_input_string(self):
        pass


    def split_input_string(self):
        """Split string of input tokens into a list each token"""

        token_list = shlex.shlex(self.input_string)
        return token_list


    def sort_tokens(self):
        """ Tokens of a input string according to the shunting yard algorithm """

        precedence_dict = {
            '^': [4, "right"],
            '*': [3, "left"],
            '/': [3, "left"],
            '+': [2, "left"],
            '-': [2, "left"]
        }

        output_queue = []
        operator_stack = []

        for token in self.split_input_string():
            try:
                # If token is a number: append to output"""
                int(token)
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
                            # and procede until reaching lower precedence or empty stack
                            while precedence_dict[token] <= precedence_dict[operator_stack[-1]]:
                                output_queue.append(operator_stack.pop())
                                if len(operator_stack) == 0:
                                    break
                            operator_stack.append(token)

                else:
                    # If token is a '(': append to stack
                    if token == "(":
                        operator_stack.append(token)

                    # If token is a ')' pop from stack to output queue until '(' is reached and poped
                    if token == ")":
                        while operator_stack[-1] is not "(":
                            output_queue.append(operator_stack.pop())
                        operator_stack.pop()

        # Poping remaining tokens from stack to output queue
        while len(operator_stack) > 0:
            output_queue.append(operator_stack.pop())



        print('Output string', ' '.join(output_queue))


        #for token in self.input_string
        #    if '+' or '-' in token: #or '*' or '/' in token: # or '(' or ')' in token:
        #        print(token)


if __name__ == '__main__':

    input = "3+4*2/(1-5)^2^3"

    sy = Shutting_yard(input)

    print("input list", [i for i in sy.split_input_string()])

    sy.sort_tokens()

    #print(input)