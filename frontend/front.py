from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from bson import ObjectId

app = Flask(__name__)
app.secret_key = "supersecretkey"

# MongoDB Connection
client = MongoClient('mongodb+srv://asalama0204:ye16MiS52yKp1sAC@cluster0.zli9h.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0&ssl=true&tlsAllowInvalidCertificates=true')
db = client.test 

users_collection = db.users 

@app.route('/chatbot')
def chatbot():
    return render_template('chatbot.html')

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/reminders')
def reminders():
    return render_template('reminders.html')
    
#Helper Function to process the message data
def process_messages(messages):
    return [
        {
            'role': msg.get('role'),
            'content': msg.get('content'),
            'timestamp': msg.get('timestamp') or datetime.datetime.now().isoformat()
        }
        for msg in messages
    ]

#Helper Function to get current user's ID from the session
def get_user_id():
    user_id = session.get('user_id')
    if not user_id:
        raise ValueError("User ID not found in session.")
    return ObjectId(user_id)

@app.route('/save_history', methods=['POST'])
def save_history():
    if request.method == 'POST' and request.is_json:
        data = request.get_json() 

        if 'messages' not in data:
            return jsonify({"error": "'messages' field is required."}), 400
        
        messages = data['messages']

        try:
            formatted_messages = process_messages(messages)
            user_id = get_user_id()
            
            result = users_collection.update_one(
                {'_id': user_id},
                {'$push': {
                    'chat_history': {'$each': formatted_messages}
                }}
            )

            if result.matched_count == 0:
                return jsonify({"error": "User not found."}), 404

            return jsonify({"message": "Chat history updated successfully"}), 200
        
        except ValueError as e:
            return jsonify({"error": str(e)}), 400

# this code does NOT validate the input from the form, i.e if username and password are null
# include one return point if something failed
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username and password:
            user = users_collection.find_one({"username": username})
            if user and check_password_hash(user["password"], password):
                session['user_id'] = str(user["_id"])
                flash("Login successful!")
                return redirect(url_for('chatbot'))
            else:
                flash("Invalid username or password")
    return render_template('login.html')

# this code does NOT validate the input from the form, i.e if username and password are null
# it would make sense to first check if passwords match, then check if the user already exists
# multiple calls to redirect, it would be cleaner to have one destination
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password1 = request.form['password1']
        password2 = request.form['password2']

        if userename and password1 and password2:
            user = users_collection.find_one({"username": username})
            if password1 != password2:
                flash("Passwords do not match")
                    return redirect(url_for('signup'))
            if user is None:
                
                new_user = {"username": username, "password": generate_password_hash(password1), "chat_history": []}
                users_collection.insert_one(new_user)
                session['user_id'] = str(new_user["_id"])
                return redirect(url_for('chatbot'))
            
            else:
                flash("Username is taken.")
                return redirect(url_for('signup'))
    
    return render_template('signup.html')
        
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash("Logged out successfully")
    return render_template('login.html')

@app.route('/send_message', methods=['POST'])
def send_message():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user_id = session['user_id']
    message = request.form.get('message')

    if not message:
        return jsonify({"error": "Message cannot be empty"}), 400
    
    # Save message to the user's chat history
    save_to_chat_history(user_id, message)
    
    bot_response = generate_bot_response()

    save_to_chat_history(user_id, bot_response)

    return jsonify({"reply": bot_response})

#Helper function to save messages to the database.
def save_to_chat_history(user_id, message):
    timestamp = datetime.now()
    users_collection.update_one(
        {"_id": ObjectId(user_id)},
        {"$push": {"chat_history": {"message": message, "timestamp": timestamp}}}
    )

def generate_bot_response():
    return "This is a bot response."

@app.route('/speed_bar')
def speed_bar():
    return render_template('speed_bar.html')

if __name__ == '__main__':
    app.run(debug=True, port=3000)