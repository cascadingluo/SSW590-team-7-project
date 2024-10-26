from flask import Flask, render_template, request, redirect, url_for, session, flash
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "supersecretkey"

# MongoDB Connection
client = MongoClient("mongodb+srv://asalama0204:ye16MiS52yKp1sAC@cluster0.zli9h.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client.test 

users_collection = db.users 

@app.route('/chatbot')
def chatbot():
    return render_template('chatbot.html')

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = users_collection.find_one({"username": username})
        
        if user and check_password_hash(user["password"], password):
            session['user_id'] = str(user["_id"])
            flash("Login successful!")
            return render_template('chatbot.html')
        else:
            flash("Invalid username or password")
            return render_template('login.html')
    
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password1 = request.form['password1']
        password2 = request.form['password2']
        
        user = users_collection.find_one({"username": username})

        if user is None:
            if password1 != password2:
                flash("Passwords do not match")
                return redirect(url_for('signup'))
            new_user = {"username": username, "password": generate_password_hash(password1)}
            users_collection.insert_one(new_user)
            return render_template('chatbot.html')
        
        else:
            flash("Username is taken.")
            return redirect(url_for('signup'))
    
    return render_template('signup.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash("Logged out successfully")
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True, port=3000)
