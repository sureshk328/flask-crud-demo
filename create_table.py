from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL



app = Flask(__name__)
app.secret_key = 'Suresh'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'python_flaskdb'

mysql = MySQL(app)



@app.route('/')
def Index():
    cur = mysql.connection.cursor()
    cur.execute("CREATE TABLE students ( student_id INT(11) NOT NULL AUTO_INCREMENT, firstname VARCHAR(50), lastname VARCHAR(50),  dob VARCHAR(20),  amountdue VARCHAR(20), CONSTRAINT student_pk PRIMARY KEY (student_id));")
    mysql.connection.commit()
    cur = mysql.connection.cursor()
    cur.execute("SELECT  * FROM students")
    data = cur.fetchall()
    cur.close()



    return render_template('index2.html', students=data )


if __name__ == "__main__":
    app.run(debug=True)
