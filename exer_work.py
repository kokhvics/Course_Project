from flask import Flask, render_template, request, redirect, url_for
import psycopg2
import time

app = Flask(__name__)

# Параметры подключения к базе данных PostgreSQL
db_params = {
    'dbname': 'Smarty',
    'user': 'postgres',
    'password': '123',
    'host': 'localhost',
    'port': '5432'
}
@app.route('/exersice')
def exers_num():
    return render_template('the_exercise.html')

@app.route('/exersice_text')
def exers_txt():
    return render_template('exer_text.html')

@app.route('/exersice_text_left')
def exers_txt_left():
    return render_template('exer_text_left.html')

@app.route('/exersice_vars')
def exers_vars():
    return render_template('exer_vars.html')