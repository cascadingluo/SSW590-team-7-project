import unittest
from flask import json
from AVA.app import app
import os
from dotenv import load_dotenv
from bson import ObjectId
from datetime import datetime, timezone
from unittest.mock import patch, MagicMock


# Testing send_message() function --> Creating tet case to test the bot response has been retrived or not when user sends message
class TestChatBot(unittest.TestCase):
    def setUp(self):
        load_dotenv()
        app.config['TESTING'] = True
        self.client = app.test_client()
        self.test_user_id = str(ObjectId())
        
    @patch("AVA.app.chat_object.send_message")    
    def test_chat_response(self, mock_send_message):

        mock_send_message.return_value = MagicMock(text="Mocked bot reply")

        current_time = datetime.now(timezone.utc)
        test_input = {
            "input": "I am feeling sick?",
            "userId": self.test_user_id ,
            "timestamp": current_time.isoformat()
        }
        
        response = self.client.post(
            '/api/chat',
            data=json.dumps(test_input),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('reply', data)
        self.assertIsInstance(data['reply'], str)
        self.assertNotEqual(data['reply'].strip(), '')
        print(f"\nBot Response: {data['reply']}")

if __name__ == '__main__':
    unittest.main()