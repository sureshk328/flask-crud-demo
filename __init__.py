from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL



app = Flask(__name__)
app.secret_key = 'Suresh'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'python_flaskdb'

mysql = MySQL(app)

def checkTableExists(tablename):
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT COUNT(*)
        FROM information_schema.tables
        WHERE table_name = '{0}'
        """.format(tablename.replace('\'', '\'\'')))
    if cur.fetchone()[0] == 1:
        cur.close()
        return True

    cur.close()
    return False

@app.route('/')
def Index():
    if checkTableExists("students"):
        cur = mysql.connection.cursor()
        cur.execute("SELECT  * FROM students")
        data = cur.fetchall()
        cur.close()
    else:
        flash("Table has been created Successfully")
        cur = mysql.connection.cursor()
        cur.execute("CREATE TABLE students ( studentid INT(11) NOT NULL AUTO_INCREMENT,  firstname VARCHAR(50), lastname VARCHAR(50),  dob VARCHAR(20),  amountdue VARCHAR(20), CONSTRAINT student_pk PRIMARY KEY (studentid));")
        mysql.connection.commit()
        return redirect(url_for('Index'))




    return render_template('index2.html', students=data )



@app.route('/insert', methods = ['POST'])
def insert():

    if request.method == "POST":
        flash("Data Inserted Successfully")
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        dob = request.form['dob']
        amountdue = request.form['amountdue']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO students (firstname, lastname, dob, amountdue) VALUES (%s, %s, %s,%s)", (firstname, lastname, dob, amountdue))
        mysql.connection.commit()
        return redirect(url_for('Index'))




@app.route('/delete/<string:studentid>', methods = ['GET'])
def delete(studentid):
    flash("Record Has Been Deleted Successfully")
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM students WHERE studentid=%s", (studentid))
    mysql.connection.commit()
    return redirect(url_for('Index'))





@app.route('/update',methods=['POST','GET'])
def update():

    if request.method == 'POST':
        studentid = request.form['studentid']
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        dob = request.form['dob']
        amountdue = request.form['amountdue']
        cur = mysql.connection.cursor()
        cur.execute("""
               UPDATE students
               SET  firstname=%s, lastname=%s, dob=%s, amountdue=%s
               WHERE studentid=%s
            """, (firstname, lastname, dob, amountdue, studentid))
        flash("Data Updated Successfully")
        mysql.connection.commit()
        return redirect(url_for('Index'))









if __name__ == "__main__":
    app.run(debug=True)
