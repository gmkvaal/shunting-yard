import re
import shlex

class Shutting_yard:

    def __init__(self, input_string):
        self.input_string = input_string

    def read_input_string(self):
        pass


    def split_input_string(self):
        """Split string of input tokens into a list each token"""

        #re.split(r'(\d+|\W+)', 'x+13.5*10x-4e1')
        #token_list = re.split(r'(\d+|\W+)', self.input_string)
        token_list = shlex.shlex(self.input_string)
        return token_list

    def sort_tokens(self):
        """ Parses input string and sorts tokens into lists of numbers and mathematical operators"""

        print("input list", [i for i in self.split_input_string()])

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
                    # If operator stack is empty: append token
                    if len(operator_stack) == 0:
                        operator_stack.append(token)
                    else:
                        if operator_stack[-1] == "(":
                            operator_stack.append(token)
                        #If token has higher precedence than top of stack: append token

                        elif precedence_dict[token][1] == "right":
                            operator_stack.append(token)

                        elif (precedence_dict[token][0] > precedence_dict[operator_stack[-1]][0]
                                                        and precedence_dict[token][1] == "left"):
                            operator_stack.append(token)
                        else:
                            #If lower than equal precedence, pop from stack to output queue
                            #and procede until reaching lower precedence or empty stack

                            print(token, "has leq precedence tag than", operator_stack[-1])

                            while precedence_dict[token] <= precedence_dict[operator_stack[-1]]:
                                output_queue.append(operator_stack.pop())
                                if len(operator_stack) == 0:
                                    break
                            operator_stack.append(token)

                else:
                    print("found a paranthesis", token)
                    if token == "(":
                        operator_stack.append(token)
                    if token == ")":
                        while operator_stack[-1] is not "(":
                            output_queue.append(operator_stack.pop())
                        operator_stack.pop()

        while len(operator_stack) > 0:
            output_queue.append(operator_stack.pop())



        print(' '.join(output_queue))
        print()
        print("3 4 2 × 1 5 − 2 3 ^ ^ ÷ +")

        #for token in self.input_string
        #    if '+' or '-' in token: #or '*' or '/' in token: # or '(' or ')' in token:
        #        print(token)

input = "3+4*2/(1-5)^2^3"

sy = Shutting_yard(input)

sy.sort_tokens()

print(input)