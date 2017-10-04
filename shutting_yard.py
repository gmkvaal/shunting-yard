import re


class Shutting_yard:

    def __init__(self, input_string):
        self.input_string = input_string

    def read_input_string(self):
        pass


    def split_input_string(self):
        """Split string of input tokens into a list each token"""

        token_list = re.split(r'([\D.]+|\W+)', self.input_string)
        return token_list

    def sort_tokens(self):
        """ Parses input string and sorts tokens into lists of numbers and mathematical operators"""

        numbers = []
        num_operators = []


        for token in self.split_input_string():
            try:
                int(token)
                numbers.append(token)
            except ValueError:
                print(token)

        print(numbers)

        #for token in self.input_string
        #    if '+' or '-' in token: #or '*' or '/' in token: # or '(' or ')' in token:
        #        print(token)

sy = Shutting_yard("1+2-33+(3-1)")

#sy.split_input_string()

sy.sort_tokens()