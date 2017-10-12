from shunting_yard import Shunting_yard


def test_input_string():
    """ Testing shunting yard algorithm by giving by asserting output from a input with a known RPL"""

    innstr = "3+4*2/(1-5)^2^3"
    correct_answer =  	"342*15-23^^/+"
    sy = Shunting_yard(innstr)
    output_queue_list = sy.sort_tokens()
    output_string = sy.output_queue_list_2_string(output_queue_list)

    assert output_string == correct_answer


def test_input_string_with_functions():
    """ Testing shunting yard algorithm by giving by asserting output from a input with a known RPL, including functions"""

    innstr = "sin(max(2,3)/3*3.1415)"
    correct_answer = "23max3/3.1415*sin"
    sy = Shunting_yard(innstr)
    output_queue_list = sy.sort_tokens()
    output_string = sy.output_queue_list_2_string(output_queue_list)

    assert output_string == correct_answer


