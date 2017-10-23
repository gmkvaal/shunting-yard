from tokenizer_FSM import tokenizer



def check_balanced_paranthesis(token_list):

    if '(' in token_list:
        if token_list.count('(') != token_list.count(')'):
            raise Exception("Unmatching number of left and right paranthesis")





if __name__ == '__main__':

    input_string = '2+2'
    output_list = tokenizer(input_string)

    token_list = []
    for item in output_list:
        token = item['name']
        token_list.append(token)

    check_balanced_paranthesis(token_list)