

class SmartParser:

    def __init__(self, input_string):

        self.input_string = input_string
        self.math_sym_list = ['+', '-', '*', '/', '^', '(', ')']
        self.function_list = ['sin', 'cos']

    def tokenize(self):

        temp_symbol = None
        output_list = []


        i = 0
        #for i in range(len(self.input_string)):
        while i < len(self.input_string):
            j = 0
            symbol = self.input_string[i]

            if symbol == '':
                pass

            elif temp_symbol == None:
                temp_symbol = symbol

            # If digit or dot, then
            elif symbol.isdigit() or symbol == '.':
                # If temp_symbol is also digit
                if temp_symbol[-1].isdigit(): # or symbol != '.':
                    print(temp_symbol[-1])
                    while i+j < len(self.input_string) and (self.input_string[i+j].isdigit() or self.input_string[i+j] == '.'):
                        temp_symbol += input_string[i + j]
                        j += 1

                    output_list.append({'name': str(temp_symbol),
                                        'value': float(temp_symbol),
                                        'type': "NUMBER"
                                        })

                # Raise error if no operator between digit and letter
                else:
                    raise Exception("Wrong format: {}{}".format(self.input_string[i - 1], self.input_string[i]))

            else:
                if symbol == ".":
                    # If symbol is dot, temp_symbol should be a digit
                    if temp_symbol[-1].isdigit():
                        temp_symbol += symbol
                    else:
                         raise Exception("Wrong format: {}{}".format(self.input_string[i - 1], self.input_string[i]))

                #elif symbol in self.math_sym_list:
                #    if temp_symbol

            i += j + 1




        print(output_list)








if __name__ == '__main__':

    input_string = "3..14"
    Smart_parser(input_string).tokenize()