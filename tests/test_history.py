import sys
import os
import unittest
import json
import datetime
from bson import ObjectId
from pymongo import MongoClient
from flask import session
from unittest.mock import patch
from AVA.app import app, users_collection

#Test cases to check the save_history() and send_message() function is working or not. 

# For handling datetime objects
class DateTimeEncoder(json.JSONEncoder): 
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.isoformat() #Convert to ISO format string
        return super().default(obj)

class FlaskTestCase(unittest.TestCase):
     
    @patch('builtins.input', return_value='')
    def setUp(self, mock_input):
        self.app = app.test_client()
        self.app.testing = True

        #checking if that test user is not present already
        existing_user = users_collection.find_one({"username": "testuser"})
        if existing_user:
            self.test_user = existing_user
            self.test_user_id = str(self.test_user['_id'])
        else:
            result = users_collection.insert_one({
                "username": "testuser",
                "chat_history": []
            })

            # Stored ID of created user
            self.test_user_id = str(result.inserted_id)

        print(f"Created test user with ID: {self.test_user_id}")
        
        #Simulating logged-in user
        with self.app as c:
            with c.session_transaction() as sess:
                sess['user_id'] = self.test_user_id
        
        #input("\nTest user has been created, press Enter to continue with the tests")

    def test_save_history(self):
        print("\n Testing save_history endpoint")
        test_messages = {
            'messages': [
                {
                    'role': 'user',
                    'content': 'Hello',
                    'timestamp': datetime.datetime.now().isoformat()
                },
                {
                    'role': 'assistant',
                    'content': 'Hi there!',
                    'timestamp': datetime.datetime.now().isoformat()
                }
            ]
        }
        
        # Sending POST request to save_history endpoint
        response = self.app.post('/save_history', data=json.dumps(test_messages), content_type='application/json')
        
        print("\nMessages have been saved - Check MongoDB")
        print(f"Check user with ID: {self.test_user_id}")

        #input("Press Enter to continue with verification")
        
        # Verify database state
        user = users_collection.find_one({"_id": ObjectId(self.test_user_id)})
        print("\nChat history in database:", 
              json.dumps(user['chat_history'], indent=2, cls=DateTimeEncoder))
        
        self.assertEqual(len(user['chat_history']), 2)
        self.assertEqual(user['chat_history'][0]['content'], 'Hello')

    def tearDown(self):
        print("\n Ready to clean up test environment")
        #input("Press Enter to delete the test user")
        users_collection.delete_one({"_id": ObjectId(self.test_user_id)})
        print(f"Deleted test user with ID: {self.test_user_id}")

if __name__ == '__main__':
    unittest.main(verbosity=2)

