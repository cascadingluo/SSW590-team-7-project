import unittest
from flask import json
from AVA.app import app
from bson import ObjectId
from datetime import datetime, timezone
from unittest.mock import patch, MagicMock


class TestChatBot(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()
        self.test_user_id = str(ObjectId())

    @patch("AVA.app.get_chat_object")
    def test_chat_response(self, mock_get_chat_object):
        # Mock the chat object returned by get_chat_object()
        mock_chat = MagicMock()
        mock_chat.send_message.return_value.text = "Mocked bot reply"
        mock_get_chat_object.return_value = mock_chat

        test_input = {
            "input": "I am feeling sick?",
            "userId": self.test_user_id,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

        response = self.client.post(
            "/api/chat",
            data=json.dumps(test_input),
            content_type="application/json"
        )

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)

        self.assertIn("reply", data)
        self.assertIsInstance(data["reply"], str)
        self.assertEqual(data["reply"], "Mocked bot reply")

        print(f"\nBot Response: {data['reply']}")


if __name__ == "__main__":
    unittest.main()