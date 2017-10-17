

class SmartParser:

    def __init__(self, input_string):

        self.input_string = input_string
        self.math_sym_list = ['+', '-', '*', '/', '^', '(', ')']
        self.function_list = ['sin', 'cos']

    def tokenize(self):

        temp_symbol = None
        output_list = []

        i = 0
        while i < len(self.input_string):
            symbol = self.input_string[i]
            if temp_symbol is None:
                temp_symbol = symbol

            if symbol == ' ':
                pass

            if symbol.isdigit():
                j = 1
                if temp_symbol[-1].isdigit or temp_symbol[-1] == '.':
                    while j+i < len(self.input_string) and (self.input_string[i + j].isdigit() or self.input_string == '.'):
                        temp_symbol += self.input_string[i + j]
                        j+=1

                    i += j - 1
                    output_list.append(
                        temp_symbol)

            i += 1
        print(output_list)








if __name__ == '__main__':

    input_string = "12345"
    SmartParser(input_string).tokenize()