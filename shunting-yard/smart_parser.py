

class Smart_parser:

    def __init__(self, input_string):

        self.input_string = input_string
        self.math_sym_list = ['+', '-', '*', '/', '^', '(', ')']
        self.function_list = ['sin', 'cos']
        self.output_list = []

    def parse(self):

        temp_symbol = None
        for i in range(len(self.input_string)):
            symbol = self.input_string[i]

            # If a digit, check type of next
            if symbol.isdigit():
                if





if __name__ == '__main__':

    input_string = "**(cos(b))"
    print(Smart_parser(input_string).parser())