from flask import Flask, render_template, send_from_directory
from app.db import History, db
from peewee import fn

from app.lookup import get_name_phone

app = Flask(__name__)

db.connect()
db.create_tables([History])


def most_frequent(n=50):
    phones = (History
              .select(History, fn.COUNT(History.phone).alias('n_calls'))
              .group_by(History.phone).order_by(fn.COUNT(History.phone).desc()).limit(n))
    return list(phones.dicts())


def call_history(n=20):
    phones = (History
              .select()
              .order_by(History.phone_date.desc()))
    return list(phones.dicts())


@app.route('/')
@app.route('/dashboard')
def dashboard():
    print("dashboard !!!!!!!!!!")
    frequent = most_frequent()
    for phone in frequent:
        phone['name'], phone['registered'] = get_name_phone(phone['phone'])
    calls = call_history()
    for phone in calls:
        phone['phone_date'] = phone['phone_date'].strftime("%d/%m/%Y %H:%M")
    return render_template('dashboard.html', page='dashboard', title='Dashboard', frequent=frequent, calls=calls)


@app.route('/number/<number_id>')
def number(number_id):
    name = get_name_phone(number_id)[0]
    History.create(name=name, phone=number_id)
    return name or ""


@app.route('/<path:path>')
def send_static(path):
    return send_from_directory('static', path)


if __name__ == '__main__':
    app.run()
