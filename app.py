from flask import Flask, render_template, request, url_for, redirect
import sqlite3, datetime

database = 'wish_list.db'
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    current_year = datetime.datetime.now().year # get current year

    conn = sqlite3.connect(database)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("""SELECT * FROM people WHERE year=""" + str(current_year))
    rows = cur.fetchall()
    conn.commit()
    conn.close()
    return render_template('index.html', rows=rows)

@app.route('/person/<person_id>', methods=['GET', 'POST'])
def get_person(person_id):
    conn = sqlite3.connect(database)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("""SELECT * FROM people WHERE id=""" + person_id)
    person = cur.fetchone()
    conn.commit()
    conn.close()

    # if id is not in database, meaning there is no person, take them to homepage
    if not person:
        return redirect(url_for('index'))

    return render_template('person.html', person=person)

@app.route('/edit/<person_id>', methods=['GET', 'POST'])
def edit(person_id):
    conn = sqlite3.connect(database)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("""SELECT * FROM people WHERE id=""" + person_id)
    person = cur.fetchone()
    conn.commit()
    conn.close()

    # if id is not in database, meaning there is no person, take them to homepage
    if not person:
        return redirect(url_for('index'))

    return render_template('edit.html', person=person)

@app.route('/edited/<person_id>', methods=['GET', 'POST'])
def edited(person_id):
    name = request.form['name']
    gift = request.form['gift']
    complete = request.form.get('complete')  # checkbox is optional, so I need to use 'get' to prevent a Bad Gateway err

    conn = sqlite3.connect(database)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("""UPDATE people SET name=?, gift=?, complete=? WHERE id=?""", (name, gift, complete, person_id))
    conn.commit()
    conn.close()

    return redirect(url_for('index'))

@app.route('/add', methods=['GET', 'POST'])
def add():
    return render_template('add.html')

@app.route('/added', methods=['GET', 'POST'])
def added():
    name = request.form['name']
    gift = request.form['gift']

    conn = sqlite3.connect('wish_list.db')
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("""INSERT INTO people (name, gift, complete, year) VALUES (?, ?, 'False', strftime('%Y'))""", (name, gift ))
    conn.commit()
    conn.close()

    return redirect(url_for('index'))

@app.route('/delete/<person_id>', methods=['GET', 'POST'])
def delete(person_id):
    conn = sqlite3.connect(database)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("""SELECT * FROM people WHERE id=""" + person_id)
    person = cur.fetchone()
    conn.commit()

    # if id is not in database, meaning there is no person, take them to homepage
    if not person:
        conn.close()
        return redirect(url_for('index'))

    cur.execute("""DELETE FROM people WHERE id=?""", (person_id, ))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(debug=True, port=8080)
