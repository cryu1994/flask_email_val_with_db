from flask import Flask, render_template, request, redirect, session, flash
from mysqlconnection import MySQLConnector
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
app = Flask(__name__)
mysql = MySQLConnector(app, 'mydb')
app.secret_key = 'asdfgk'

@app.route('/')
def main():
    return render_template('index.html')

@app.route('/create', methods=['post'])
def create():
    count = 0
    if len(request.form['email']) < 1:
        flash("Email Must be entered!")
        count += 1
    if not EMAIL_REGEX.match(request.form['email']):
        flash("Invalid Email!")
        count += 1
    if count < 1:
        query = "INSERT INTO users(email, created_at, updated_at) VALUES(:email, NOW(), NOW())"
        data = {
            'email': request.form['email']
        }
        mysql.query_db(query, data)
        return redirect('/success')
    else:
        return redirect('/')

@app.route('/success')
def success():
    query = "SELECT users.id, users.email, users.created_at from users"
    user = mysql.query_db(query)
    return render_template('success.html', all_user=user)

@app.route('/delete/<user_id>', methods=['post'])
def delete(user_id):
    query = "DELETE FROM users WHERE id = :id"
    data = {'id': user_id}
    mysql.query_db(query, data)
    print data
    return redirect('/success')
app.run(debug=True)
