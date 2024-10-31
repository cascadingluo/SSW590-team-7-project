from flask import Flask, render_template, request, redirect, url_for, session, flash,  request, jsonify
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
import google.generativeai as genai
import os
import random
app = Flask(__name__)
app.secret_key = "supersecretkey"

# Load environment variables
load_dotenv()


# MongoDB Connection
client = MongoClient('mongodb+srv://asalama0204:ye16MiS52yKp1sAC@cluster0.zli9h.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0&ssl=true&tlsAllowInvalidCertificates=true')
db = client.test 

users_collection = db.users 

print(os.getenv("API_KEY"))

# Initialize Google Generative AI
# Set the API key for google.generativeai
genai.configure(api_key=os.getenv("API_KEY"))

model = genai.GenerativeModel(model_name="tunedModels/avamentalhealthft1-23b1qsi4o8g0")

# Start a chat session
chat = model.start_chat()



# Initial prompts
initial_prompts = [
    "Hey there! How are you feeling today?", "Hi! I'm here for you. What’s on your mind?",
    "Hello! How’s everything going for you today?", "Hey! I’m ready to listen. How are you feeling?",
    "Hi there! How are you doing, both physically and mentally?", "Hello! What’s something you’d like to talk about today?",
    "Hi! How’s your day been so far?", "Hey! It’s good to see you. How are you holding up?",
    "Hello! How can I support you today?", "Hi! What’s been on your mind lately?",
    "Hey! I’m here to help you feel better. How are you?", "Hi! I’d love to hear how you’re doing today.",
    "Hello! Is there anything on your mind that you'd like to share?", "Hey! How’s your mood today?",
    "Hi there! How are you feeling emotionally today?", "Hello! It’s great to see you. How’s everything going for you?",
    "Hi! How are you feeling in this moment?", "Hey! I’m here if you need someone to talk to. How are you?",
    "Hello! How’s your mental health been lately?", "Hi! Let’s chat. How are you feeling today?",
    "Hey! How’s your headspace today? Need a little support?", "Hello! What’s something on your mind that we can talk about?",
    "Hi there! How are things going for you today?", "Hey! How are you really feeling today?",
    "Hello! How has your week been so far?", "Hi! Anything on your mind that you’d like to talk about?",
    "Hey! How can I be helpful to you today?", "Hi there! How’s your emotional well-being right now?",
    "Hello! Let’s check in. How are you doing today?", "Hi! What’s something you’ve been thinking about lately?",
    "Hey! How have you been feeling emotionally this week?", "Hello! How’s your mental health today?",
    "Hi! I’m here for you. What’s been on your mind?", "Hey! How are you feeling today, physically and mentally?",
    "Hi there! Anything you’d like to talk about today?", "Hello! How are you feeling emotionally and physically?",
    "Hi! Let’s take a moment to check in. How are you feeling?", "Hey! How’s your stress level today? Need to talk?",
    "Hello! I’m ready to listen. How’s your day been?", "Hi! How’s your mental space right now?",
    "Hey! What’s one thing you’ve been thinking about lately?", "Hello! How’s your energy level today? How are you feeling?",
    "Hi! It’s great to check in with you. How are you feeling?", "Hey! Let’s chat about how you’re doing today.",
    "Hello! What’s been on your mind this week?", "Hi! I’m here for you. How’s your mental health?",
    "Hey! How’s your day going? Need someone to talk to?", "Hello! How are you feeling emotionally and mentally?",
    "Hi there! How can I help support you today?", "Hey! What’s something you’ve been feeling lately?"
]



@app.route('/chatbot')
def chatbot():
    return render_template('chatbot.html')

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = users_collection.find_one({"username": username})
        
        if user and check_password_hash(user["password"], password):
            session['user_id'] = str(user["_id"])
            flash("Login successful!")
            return redirect(url_for('chatbot'))
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



# Route to initialize chat
@app.route('/api/initChat', methods=['POST'])
def init_chat():
    initial_prompt = random.choice(initial_prompts)
    
    try:
        # result = chat.send_message(initial_prompt)
        # print(result.text) 
        # bot_response = result.text  # Assuming response is accessed this way
        return jsonify({"reply": initial_prompt})
    except Exception as error:
        print("Error generating initial response:", error)
        return jsonify({"error": "Error generating initial response"}), 500

# Route to handle chat messages
@app.route('/api/chat', methods=['POST'])
def chatGoogle():
    user_input = request.json.get("input", "")
    
    prompt = (
        f"You are a compassionate and knowledgeable mental health assistant. Your role is to listen to the user’s emotional concerns and "
        f"provide supportive advice. Act as a friend or caretaker to the user. Use simple, everyday language to keep things easy to understand. "
        f"Make sure your tone is conversational, and avoid technical terms or complex phrases. At the end ask a specific follow-up question related "
        f"to their health or well-being. Keep your questions friendly and focused on keeping the conversation going in a positive, engaging way. "
        f"Provide the best course of action based on this input: {user_input} Respond in 3-4 sentences."
    )

    try:
        result = chat.send_message(prompt)
        print(result.text) 
        bot_response = result.text  # Assuming response is accessed this way
        return jsonify({"reply": bot_response})
    except Exception as error:
        print("Error generating response:", error)
        return jsonify({"error": "Error generating response"}), 500
    


if __name__ == '__main__':
    app.run(debug=True, port=3000)