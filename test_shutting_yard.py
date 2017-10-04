from shutting_yard import Shutting_yard


def test_input_string():

    innstr = "1+2+33"
    sy = Shutting_yard(innstr)

    assert len(innstr) == len(sy.split_input_string())
