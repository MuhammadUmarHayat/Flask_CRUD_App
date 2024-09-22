from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

# MySQL configuration
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="flask_crud"
)
cursor = db.cursor()

# Create operation (adding a user)
@app.route('/create', methods=['POST'])
def create():
    name = request.form['name']
    email = request.form['email']
    phone = request.form['phone']
    
    query = "INSERT INTO users (name, email, phone) VALUES (%s, %s, %s)"
    cursor.execute(query, (name, email, phone))
    db.commit()
    
    return redirect(url_for('index'))

# Read operation (display users)
@app.route('/')
def index():
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    return render_template('index.html', users=users)

# Update operation (edit user)
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        
        query = "UPDATE users SET name=%s, email=%s, phone=%s WHERE id=%s"
        cursor.execute(query, (name, email, phone, id))
        db.commit()
        
        return redirect(url_for('index'))
    else:
        cursor.execute("SELECT * FROM users WHERE id = %s", (id,))
        user = cursor.fetchone()
        return render_template('edit.html', user=user)

# Delete operation (remove a user)
@app.route('/delete/<int:id>')
def delete(id):
    query = "DELETE FROM users WHERE id = %s"
    cursor.execute(query, (id,))
    db.commit()
    
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)
