from app import app
from flask import render_template, request
from shunting_yard import Shunting_yard

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def my_form_post():

    input_str = request.form['text']
    sy = Shunting_yard(input_str)
    output_str = sy.output_queue_list_2_string()

    return render_template('index.html',
                           output_str = output_str,
                           input_str = input_str)
