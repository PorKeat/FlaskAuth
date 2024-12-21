from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

app = Flask(__name__)


app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '1234'
app.config['MYSQL_DB'] = 'login'



mysql = MySQL(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods = ['POST'])
def login():
    if request.method == 'POST':
        email = request.form['loginEmail']
        password = request.form['loginPass']
        
        cursor = mysql.connection.cursor()
        
        cursor.execute('''SELECT * FROM users WHERE email = %s AND password = %s''', (email, password))
        user = cursor.fetchone()
        if user:
            cursor.close()
            return redirect(url_for('success'))
        else:
            cursor.close()
            return "Invalid email or password. Please try again."
        
@app.route('/register', methods = ['POST'])
def register():
    if request.method == 'POST':
        email = request.form['rEmail']
        password = request.form['rPass']
        confirmPass = request.form['cPass']
        cursor = mysql.connection.cursor()
        
        cursor.execute('''SELECT * FROM users WHERE email = %s''',(email,))
        user = cursor.fetchone()
        if user:
            return "Email already exist"
        else:
            if password == confirmPass:
                cursor.execute('''INSERT INTO users (email, password, confirmPass) VALUES (%s, %s, %s)''', (email, password,confirmPass))
                mysql.connection.commit()
                cursor.close()
                
                return redirect(url_for('success'))
            else: 
                return "Password need to be matched"

@app.route('/success')
def success():
    return render_template('success.html')


if __name__ == '__main__':
    app.run(debug=True)
