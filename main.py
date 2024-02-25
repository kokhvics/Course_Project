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

        # Получаем количество заданий по заданной теме
        total_exercises = get_total_exercises(topic_name)

        # Возвращаем количество заданий в формате JSON
        return jsonify({'totalExercises': total_exercises}), 200
    else:
        # Если данные не в формате JSON, возвращаем ошибку
        return jsonify({'error': 'Неверный формат данных'}), 400


def get_total_exercises(topic_name):
    conn = psycopg2.connect(**db_params)
    cursor = conn.cursor()
    sql_query = """
    SELECT COUNT(*) AS total_exercises
    FROM exercises_choose_ans
    WHERE fk_subtopic_id = (SELECT subtopic_id FROM subtopics WHERE subtopic_name = %s)
    """
    # Выполняем запрос с использованием данных из запроса
    cursor.execute(sql_query, (topic_name,))
    # Получаем результат запроса
    total_exercises = cursor.fetchone()[0]  # Получаем значение количества заданий
    # Закрываем соединение с базой данных
    cursor.close()
    conn.close()
    return total_exercises



@app.route('/exersice_start')
def exers_num():
    return render_template('the_exercise.html')\

@app.route('/exersice_next')
def exers_next():
    return render_template('exer_vars_next.html')


if __name__ == '__main__':
    app.run(debug=True)
