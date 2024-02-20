from flask import Flask, render_template, request, redirect, url_for
import psycopg2
import exer_work

app = Flask(__name__)

# Параметры подключения к базе данных PostgreSQL
db_params = {
    'dbname': 'Smarty',
    'user': 'postgres',
    'password': '123',
    'host': 'localhost',
    'port': '5432'
}

# Маршрут для отображения HTML-страницы
@app.route('/')
def enter_page():
    return render_template('Enter page.html')

def get_user_name(login, password):
    conn = psycopg2.connect(**db_params)
    cur = conn.cursor()
    cur.execute("SELECT st_name  FROM students WHERE st_login = %s AND st_password = %s", (login, password))
    row = cur.fetchone()
    conn.close()
    return row[0] if row else None

# Функция для получения информации о subtopic из базы данных
# нужно доделать получение класса в котором учится ребенок
def fetch_subtopics():
    conn = psycopg2.connect(**db_params)
    cur = conn.cursor()
    cur.execute("SELECT s.subtopic_name FROM subtopics s JOIN task_topic_year_of_study t ON s.subtopic_id = t.subtopic_id WHERE t.year_of_study_id = 9")
    subtopics = cur.fetchall()
    conn.close()
    return subtopics

# Получаем информацию о subtopic из базы данных
subtopics = fetch_subtopics()



@app.route('/login', methods=['POST'])
def login():
    # Получение введенных значений логина и пароля
    login = request.form['login']
    password = request.form['password']
    user_name = get_user_name(login, password)
    if user_name:
        return redirect(url_for('home_page', user_name=user_name))
    else:
        conn = psycopg2.connect(**db_params)
        cur = conn.cursor()

        # Выполнение SQL-запроса для проверки наличия значения в таблице students
        cur.execute("SELECT * FROM students WHERE st_login = %s AND st_password = %s", (login, password))
        result = cur.fetchone()

        # Закрытие курсора и соединения
        cur.close()
        conn.close()

        if result:
            return redirect(url_for('home_page'))
        else:
            return "Ошибка: неверный логин или пароль"
        pass

    # Установка соединения с базой данных
    conn = psycopg2.connect(**db_params)
    cur = conn.cursor()

    # Выполнение SQL-запроса для проверки наличия значения в таблице students
    cur.execute("SELECT * FROM students WHERE st_login = %s AND st_password = %s", (login, password))
    result = cur.fetchone()

    # Закрытие курсора и соединения
    cur.close()
    conn.close()

    if result:
        return redirect(url_for('home_page'))
    else:
        return "Ошибка: неверный логин или пароль"

@app.route('/home')
def home_page():
    user_name = request.args.get('user_name')
    return render_template('Home page.html', user_name=user_name, subtopics=subtopics)

#нужно сделать так, чтобы в блоке заданий выводились названия только тех subtopic, которые соответсвуют году обучения

#нужно завести массив или другую структуру данных, чтобы хранить а)количество заданий в этой теме, б)присваивать номеру
#задания которе сейчас выполняется id задания из бд

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

if __name__ == '__main__':
    app.run(debug=True)
