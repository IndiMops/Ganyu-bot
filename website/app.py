from flask import Flask, render_template, url_for, request, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
import sqlite3


app = Flask(__name__, static_folder='static')
app.config['SQLALCHEMY DATABASE_URI'] = 'sqlite:///./'


@app.route('/')
@app.route('/home')
def index():
    data = sqlite3.connect('data.sqlite')# connect to DB
    cur = data.cursor()
    
    for row in cur.execute(f'SELECT guilds, users, commands FROM stats_bot'):
        guilds = row[0]
        users = row[1]
        commands = row[2]
    print(guilds, users, commands)
    return render_template('index.html', guilds=guilds, users=users, commands=commands)




@app.route('/stats')
def stats():
    data = sqlite3.connect('data.sqlite')# connect to DB
    cur = data.cursor()
    
    for row in cur.execute(f'SELECT guilds, users, commands FROM stats_bot'):
        guilds = row[0]
        users = row[1]
        commands = row[2]
        
    def cast(number: int) -> str:
        if number >= 1000000:
            formatted_number = "{:.1f} млн.".format(number / 1000000)
        elif number > 1000:
            formatted_number = "{:.1f} тис.".format(number / 1000)
        else:
            formatted_number = number
        return formatted_number
    
    data = {
        "guilds": cast(guilds),
        "users": cast(users),
        "commands": cast(commands)
    }
    return jsonify(data)

@app.errorhandler(404)
def pageNotFound(error):
    print(error)
    return render_template('error/404.html')


def app_main():
    app.run(debug=True)
    logo = url_for( 'static', filename='assets/logo.gif')


if __name__ == "__main__":
    app_main()
