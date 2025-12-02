import time
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from dotenv import load_dotenv
from bson import ObjectId
import random
import os 
from flask_socketio import SocketIO, emit
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.date import DateTrigger
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from flask import Response
from prometheus_flask_exporter import PrometheusMetrics

app = Flask(__name__)
metrics = PrometheusMetrics(app)

REQUEST_COUNT = Counter(
    'ava_request_count',
    'Total HTTP requests',
    ['method', 'endpoint']
)

REQUEST_LATENCY = Histogram(
    'ava_request_latency_seconds',
    'Latency of HTTP requests in seconds',
    ['endpoint']
)

REMINDER_SAVED = Counter(
    'ava_reminder_saved_total',
    'Total reminders saved'
)

from functools import wraps

def track_metrics(endpoint_name):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            start = time.time()
            REQUEST_COUNT.labels(method=request.method, endpoint=endpoint_name).inc()
            response = f(*args, **kwargs)
            REQUEST_LATENCY.labels(endpoint=endpoint_name).observe(time.time() - start)
            return response
        return wrapper
    return decorator

socketio = SocketIO(app)
dt = datetime.today()
TODAY = dt.strftime('%A').lower()
scheduler = BackgroundScheduler()
scheduler.start()



load_dotenv()
app.secret_key = os.getenv("SECRET_KEY")

# MongoDB Connection
client = MongoClient(os.getenv("MONGO_URI"))
db = client.test 

# # Initialize Google Generative AI
# # Set the API key for google.generativeai
# genai.configure(api_key=os.getenv("API_KEY"))

users_collection = db.users 

# model = genai.GenerativeModel(model_name="gemini-1.5-flash")
#model = genai.GenerativeModel(model_name="tunedModels/avamentalhealthft1-23b1qsi4o8g0")
#model = genai.GenerativeModel(model_name="tunedModels/mentalhealthchatbot-7mrtrsg0fib1")

from google import genai

import os

API_KEY = 'AIzaSyB76uW0XLIijk8ulil5MW358tbsM-VP6zU' # or hardcode temporarily

client = genai.Client(api_key=API_KEY)
chat_object = client.chats.create(model="gemini-2.5-flash")

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
            'timestamp': msg.get('timestamp') or datetime.now().isoformat()
        }
        for msg in messages
    ]

#Helper Function to get current user's ID from the session
def get_user_id():
    user_id = session.get('user_id')
    if not user_id:
        raise ValueError("User ID not found in session.")
    return ObjectId(user_id)

def get_chat_history():
    user_id = get_user_id()
    user = users_collection.find_one({"_id": ObjectId(user_id)})
    if user and "chat_history" in user:
        return user["chat_history"]
    return []

def model_with_history():
    chat_history = get_chat_history()
    # for new users, the chat history will be empty. 
    if not chat_history:
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
            "Hey! How can I be helpful to you today?", "Hi there! How’s your emotional well-being right now?"
        ]
        random_prompt = random.choice(initial_prompts)
        print(f"Selected initial prompt: {random_prompt}") 
        return f"Bot: {random_prompt}"
    
    #otherwise, i built the prompt with existing chat history. 
    prompt_history = ""
    for msg in chat_history:
        role = msg["role"]
        content = msg["content"]
        prompt_history += f"{role.capitalize()}: {content}\n"

    guidance_prompt = (
            "As A.V.A, a mental health assistant, review the chat history and craft a brief, empathetic response. "
            "Ask a concise, caring follow-up question directly related to the user's previous messages. Use exactly 1-2 short sentences."
    )

    initial_prompt = f"{guidance_prompt}\n\n{prompt_history}Bot:"
    return initial_prompt
   

@app.route('/api/initChat', methods=['POST'])
def init_chat():
    try:
        prompt = model_with_history()
        chat_history = get_chat_history()
        if not chat_history:
            bot_response = prompt.replace("Bot: ", "")
        else:
            result = chat_object.send_message(prompt)
            follow_up_question = " Would you like to continue talking about this, or is there something new you'd like to discuss today?"
            bot_response = result.text + follow_up_question
        return jsonify({"reply": bot_response})
    except Exception as error:
        print("Error generating initial response:", error)
        return jsonify({"error": "Error generating initial response"}), 500

@app.route('/api/chat', methods=['POST'])
@track_metrics("api_chat")
def chat():
    data = request.json
    user_input = data.get('input')
    user_id = data.get('userId')

    prompt = f"""You are a compassionate and knowledgeable mental health assistant. Your role is to listen to the user’s emotional concerns and 
    provide supportive advice. Act as a friend or caretaker to the user. Use simple, everyday language to keep things easy to understand. Make 
    sure your tone is conversational, and avoid technical terms or complex phrases. At the end ask a specific follow-up question related to their 
    health or well-being. Keep your question friendly and focused on keeping the conversation going in a positive, engaging way. Provide the best 
    course of action based on this input: {user_input}. Use strictly just 1-2 short sentences [max 50 words]"""

    try:
        result = chat_object.send_message(prompt)
        bot_response = result.text

        if user_id:
            try:
                users_collection.update_one(
                    {'_id': ObjectId(user_id)},
                    {'$push': {
                        'chat_history': [
                            {
                                'role': 'user',
                                'content': user_input,
                                'timestamp': datetime.now()
                            },
                            {
                                'role': 'bot',
                                'content': bot_response,
                                'timestamp': datetime.now()
                            },
                        ],
                    }}
                )
                print("Chat history saved successfully.")
            except Exception as db_error:
                print("Database error:", db_error)

        return jsonify({"reply": bot_response})
    except Exception as error:
        print("Error generating response:", error)
        return jsonify({"error": "Error generating response"}), 500
    
    
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
        
def send_reminder(reminder):
    socketio.emit('reminder', reminder)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = users_collection.find_one({"username": username})
        
        if user and check_password_hash(user["password"], password):
            session['user_id'] = str(user["_id"])
            flash("Login successful!")

            if user.get('reminders'):
                reminders = user['reminders']
                for reminder in reminders:
                    day = reminder['day'].lower()
                    if day == TODAY:
                        now = datetime.now()
                        time = reminder['time']
                        reminder_datetime = datetime.combine(
                            now.date(), 
                            datetime.strptime(time, "%H:%M").time()
                        )

                        scheduler.add_job(
                            send_reminder,
                            trigger=DateTrigger(run_date=reminder_datetime),
                            args=[reminder],
                        )

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
            new_user = {"username": username, "password": generate_password_hash(password1), "chat_history": [], "reminders": []}
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
    scheduler.remove_all_jobs()
    flash("Logged out successfully")
    return render_template('login.html')

@app.route('/send_messages', methods=['POST'])
def send_messages():
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

@app.route('/save_reminder', methods=['POST'])
@track_metrics("save_reminder")
def save_reminder():
    user_id = session['user_id']
    data = request.get_json() 
    day = data['day'].lower()
    time = data['time']

    users_collection.update_one(
        {"_id": ObjectId(user_id)},
        {"$push": {
            "reminders": {
              "text": data['text'], 
              "time": time,
              "day": day, 
              "frequency": data['frequency'], 
            }}}
    )
    if day == TODAY:
        now = datetime.now()
        reminder_datetime = datetime.combine(
            now.date(), 
            datetime.strptime(time, "%H:%M").time()
        )

        scheduler.add_job(
            send_reminder,
            trigger=DateTrigger(run_date=reminder_datetime),
            args=[data],
        )

    return jsonify({"reply": 'success'})


def generate_bot_response():
    user_input = request.json.get("input", "")
    
    prompt = f"""You are a compassionate and knowledgeable mental health assistant. Your role is to listen to the user’s emotional concerns and 
    provide supportive advice. Act as a friend or caretaker to the user. Use simple, everyday language to keep things easy to understand. Make 
    sure your tone is conversational, and avoid technical terms or complex phrases. At the end ask a specific follow-up question related to their 
    health or well-being. Keep your question friendly and focused on keeping the conversation going in a positive, engaging way. Provide the best 
    course of action based on this input: {user_input}. Use strictly just 1-2 short sentences [max 50 words]"""

    try:
        result = chat_object.send_message(prompt)
        print(result.text) 
        bot_response = result.text
        return jsonify({"reply": bot_response})
    except Exception as error:
        print("Error generating response:", error)
        return jsonify({"error": "Error generating response"}), 500

@app.route('/speed_bar')
def speed_bar():
    return render_template('speed_bar.html')

# @app.route('/emotion_analysis_page')
# def emotion_analysis_page():
#     if 'user_id' not in session:
#         return redirect(url_for('login'))
#     return render_template('emotion_analysis.html')

# @app.route('/emotion_analysis', methods=['GET'])
# @track_metrics("emotion_analysis")
# def get_emotion_analysis():
#     if 'user_id' not in session:
#         return jsonify({"error": "User not logged in"}), 401
#     try:
#         emotion_detector = EmotionDetector()
#         user_id = get_user_id()
#         chat_history = get_chat_history()
#         emotion_analysis = {
#             'emotion_counts': {},
#             'emotion_trends': [],
#             'overall_dominant_emotion': None
#         }
#         user_messages = [
#             msg for msg in chat_history 
#             if msg['role'] == 'user'
#         ][-20:]   # Only analyzes the last 20 user messages
        
#         for message in user_messages:
#             text = message.get('content', '')
#             if text:
#                 try:
#                     emotion, confidence = emotion_detector.detect_emotion(text)
#                     emotion_analysis['emotion_counts'][emotion] = emotion_analysis['emotion_counts'].get(emotion, 0) + 1
#                     emotion_analysis['emotion_trends'].append({
#                         'emotion': emotion,
#                         'confidence': confidence,
#                         'timestamp': message.get('timestamp')
#                     })
#                 except Exception as emotion_error:
#                     print(f"Error detecting emotion for message: {text}")
#                     print(f"Error details: {emotion_error}")
        
#         # Determining the overall dominant emotion based on counts
#         if emotion_analysis['emotion_counts']:
#             emotion_analysis['overall_dominant_emotion'] = max(
#                 emotion_analysis['emotion_counts'], 
#                 key=emotion_analysis['emotion_counts'].get
#             )
        
#         return jsonify(emotion_analysis)
    
#     except Exception as e:
#         print(f"Emotion Analysis Error: {e}")
#         return jsonify({"error": "Error processing emotion analysis"}), 500

@app.route("/metrics")
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)

if __name__ == '__main__':
    app.run(debug=True, port=3000)