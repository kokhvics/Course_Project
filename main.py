from flask import Flask, render_template, request, redirect, url_for, jsonify
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

def get_user_year_of_study(login, password):
    conn = psycopg2.connect(**db_params)
    cur = conn.cursor()
    cur.execute("SELECT fk_year_of_study_id FROM students WHERE st_login = %s AND st_password = %s", (login, password))
    row = cur.fetchone()
    conn.close()
    return row[0] if row else None

# Функция для получения информации о subtopic из базы данных
def fetch_subtopics(login, password):
    year_of_study = get_user_year_of_study(login, password)
    if year_of_study is None:
        return None  # Обработка случая, когда пользователь не найден или год обучения не указан

    conn = psycopg2.connect(**db_params)
    cur = conn.cursor()
    cur.execute("SELECT s.subtopic_name FROM subtopics s JOIN task_topic_year_of_study t ON s.subtopic_id = t.subtopic_id WHERE t.year_of_study_id = %s", (year_of_study,))
    subtopics = cur.fetchall()
    conn.close()
    return subtopics

@app.route('/login', methods=['POST'])
def login():
    login = request.form['login']
    password = request.form['password']

    # Проверка наличия пользователя в базе данных
    if get_user_name(login, password):
        return redirect(url_for('home_page', login=login, password=password))
    else:
        return "Ошибка: неверный логин или пароль"

@app.route('/home')
def home_page():
    login = request.args.get('login')
    password = request.args.get('password')

    subtopics = fetch_subtopics(login, password)

    # Получение URL из базы данных
    conn = psycopg2.connect(**db_params)
    cur = conn.cursor()
    cur.execute("SELECT url FROM students WHERE st_login = %s AND st_password = %s", (login, password))
    image_url = cur.fetchone()[0]
    conn.close()

    if subtopics:
        return render_template('Home page.html', user_name=login, subtopics=subtopics, image_url=image_url)
    else:
        return "Ошибка: Пользователь не найден или не указан год обучения."

#нужно сделать так, чтобы в блоке заданий выводились названия только тех subtopic, которые соответсвуют году обучения

#нужно завести массив или другую структуру данных, чтобы хранить а)количество заданий в этой теме, б)присваивать номеру
#задания которе сейчас выполняется id задания из бд


@app.route('/exersice')
def exers_info():
    return render_template('exer_info.html')

@app.route('/exersice_text')
def exers_txt():
    return render_template('exer_text.html')

@app.route('/exersice_text_left')
def exers_txt_left():
    return render_template('exer_text_left.html')

@app.route('/exersice_vars')
def exers_vars():
    return render_template('exer_vars.html')


# Маршрут для обработки POST-запросов на /process_topic
@app.route('/process_topic', methods=['POST'])
def process_topic():
    # Проверяем, что запрос содержит данные в формате JSON
    if request.is_json:
        # Получаем JSON-данные из запроса
        data = request.get_json()

        # Извлекаем название темы из полученных данных
        topic_name = data.get('topicName')

        # Ваш код для дальнейшей обработки названия темы

        # Пример: вы можете вернуть обратно на клиент подтверждение успешной обработки
        return jsonify({'message': 'Название темы успешно получено и обработано'}), 200
    else:
        # Если данные не в формате JSON, возвращаем ошибку
        return jsonify({'error': 'Неверный формат данных'}), 400


# Функция для получения количества заданий по названию подтемы
def get_task_count(subtopic_name):
    conn = psycopg2.connect(**db_params)
    cur = conn.cursor()

    # Получаем ID подтемы по ее названию
    cur.execute("SELECT id FROM subtopics WHERE name = %s", (subtopic_name,))
    subtopic_id = cur.fetchone()[0]  # Получаем первый найденный ID

    # Получаем количество заданий для данной подтемы
    cur.execute("SELECT COUNT(*) FROM exercises_choose_ans WHERE fk_subtopic_id = %s", (subtopic_id,))
    task_count = cur.fetchone()[0]  # Получаем количество заданий

    cur.close()
    conn.close()

    return task_count

@app.route('/get_task_count/<subtopic_name>')
def get_task_count_route(subtopic_name):
    task_count = get_task_count(subtopic_name)
    return str(task_count)

@app.route('/exersice_start')
def exers_num():
    return render_template('the_exercise.html')


if __name__ == '__main__':
    app.run(debug=True)
