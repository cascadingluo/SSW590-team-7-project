import sys
import os
import unittest
from pymongo import MongoClient
from werkzeug.security import generate_password_hash
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# from front import app, users_collection
from AVA.app import app, users_collection
# from AVA.emotion_detector import EmotionDetector


class FlaskTestCase(unittest.TestCase):
    
    def setUp(self):
        # Set up the test client and test database
        self.app = app.test_client()
        self.app.testing = True
        
        # Add a test user to the database
        self.test_username = 'testuser'
        self.test_password = 'password123'
        self.test_hashed_password = generate_password_hash(self.test_password)
        users_collection.insert_one({
            "username": self.test_username,
            "password": self.test_hashed_password,
            "chat_history": []
        })
    
    def tearDown(self):
        # Clean up the test user from the database
        users_collection.delete_one({"username": self.test_username})

    def test_signup_page_loads(self):
        response = self.app.get('/signup')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'sign up', response.data)
    
    def test_successful_signup(self):
        response = self.app.post('/signup', data={
            'username': self.test_username ,
            'password1': 'newpassword',
            'password2': 'newpassword'
        }, follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome to A.V.A, your personal AI', response.data)
        
        # Clean up the new user created during the test
        users_collection.delete_one({"username": self.test_username })
    
    def test_signup_passwords_do_not_match(self):
        response = self.app.post('/signup', data={
            'username': 'mismatchuser',
            'password1': 'password123',
            'password2': 'password321'
        }, follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'sign up', response.data)

    def test_login_page_loads(self):
        response = self.app.get('/login')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login', response.data)
    
    def test_successful_login(self):
        response = self.app.post('/login', data={
            'username': self.test_username,
            'password': self.test_password
        }, follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome to A.V.A, your personal AI', response.data)
    
    def test_unsuccessful_login(self):
        response = self.app.post('/login', data={
            'username': 'wronguser',
            'password': 'wrongpassword'
        }, follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login', response.data)

if __name__ == '__main__':
    unittest.main()
