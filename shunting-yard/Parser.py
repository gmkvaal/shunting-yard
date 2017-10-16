def parser(input_string):
    """Parses the input string into a list of individual tokens

    Tokens are temprarily stored in temp_variable, to which new tokens are added according to a set of rules:
    - temp_varriable is appended to output_list when a different type or a math symbol is reached
    - Numbers are added to temp_variable until a non int/float is encountered
    - Letters, i.e strings not defined in math_syn_list (math symbols) are added until a math symbol is reached
    - When reaching a ',' og '.', temp_variable is appended to output_lust
    """

    math_sym_list = ['+', '-', '*', '/', '^', '(', ')']
    output_list = []
    temp_variable = None

    for symbol in input_string:
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
            if symbol.isdigit():
                # If symbol is a number: append to output"""
                if temp_variable == None:
                    temp_variable = symbol

                else:
                    temp_variable += symbol

            else:
                # If symbol is neither a mathematical symbol or a number
                if temp_variable == None:
                    temp_variable = symbol

                else:
                    if symbol.isdigit():
                        # If temp_variable is a int, append it to output_list and update temp variable
                        output_list.append(temp_variable)
                        temp_variable = symbol

                    else:
                        # If temp variable is a letter, add to temp variable
                        temp_variable += symbol

    if temp_variable != None:
        output_list.append(temp_variable)

    return (output_list)
