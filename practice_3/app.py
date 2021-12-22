import psycopg2
from flask import Flask, render_template, request, redirect

from config import user, password

app = Flask(__name__)
conn = psycopg2.connect(database="service_db",
                        user=user,
                        password=password,
                        host="localhost",
                        port="5432")

cursor = conn.cursor()


@app.route('/login/', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        if request.form.get("login"):
            username = request.form.get('username')
            password = request.form.get('password')

            if not username or not password:
                return render_template('login.html', username=username, password=password, first_time=False,
                                       db_error=False)

            try:
                cursor.execute("SELECT * FROM service.users WHERE login=%s AND password=%s",
                               (str(username), str(password)))
                records = list(cursor.fetchall())
                return render_template('account.html', full_name=records[0][1], username=records[0][2],
                                       password=records[0][3])
            except IndexError:
                return render_template('login.html', username=username, password=password, first_time=False,
                                       db_error=True)

        elif request.form.get("registration"):
            return redirect("/registration/")

    return render_template('login.html', username="", password="", first_time=True, db_error=False)


@app.route('/registration/', methods=['POST', 'GET'])
def registration():
    if request.method == 'POST':
        name = request.form.get('name')
        login = request.form.get('login')
        password = request.form.get('password')

        if not name or not login or not password:
            return render_template('registration.html', name=name, login=login, password=password, first_time=False)

        cursor.execute('INSERT INTO service.users (full_name, login, password) VALUES (%s, %s, %s);',
                       (str(name), str(login), str(password)))
        conn.commit()

        return redirect('/login/')

    return render_template('registration.html', name="", login="", password="", first_time=True)
