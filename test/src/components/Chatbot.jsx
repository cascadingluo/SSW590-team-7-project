import React, { useState } from 'react';
import axios from 'axios';

const Chatbot = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");

  const handleInputChange = (e) => {
    setInput(e.target.value);
  };
  
  const sendMessage = async () => {
    if (!input.trim()) return; 
    const userMessage = { role: 'user', content: input };
    setMessages((prevMessages) => [...prevMessages, userMessage]);
    setInput("");

    try {
      const apiUrl = 'API KEY GOES HERE!!';
      const response = await axios({
        url: apiUrl,
        method: "post",
        data: {
          contents: [{
            parts: [{text: "you are a proffesional mental health person respond to this input with the best course of actions based of these: " + input + " respond in 3-4 sentences"}]
          }]
        }
      });
      
      // Extract the bot's response from the API response
      const botResponse = response.data.candidates[0].content.parts[0].text;
      const botMessage = { role: 'bot', content: botResponse };
      setMessages((prevMessages) => [...prevMessages, botMessage]);
    } catch (error) {
      console.error("Error sending message:", error);
      setMessages((prevMessages) => [...prevMessages, { role: 'bot', content: "Sorry, I encountered an error. Please try again." }]);
    }
  };

  return (
    <div>
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="fixed p-3 text-white bg-blue-600 rounded-full shadow-lg bottom-5 right-5 hover:bg-blue-700 focus:outline-none"
      >
        {isOpen ? 'Close' : 'Chat'}
      </button>
      {isOpen && (
        <div className="fixed flex flex-col bg-white border border-gray-200 rounded-lg shadow-lg bottom-20 right-5 w-80 h-96">
          <div className="flex-1 p-4 overflow-y-auto bg-gray-100">
            {messages.map((msg, index) => (
              <div key={index} className={`mb-2 ${msg.role === 'user' ? 'text-right' : 'text-left'}`}>
                <strong>{msg.role === 'user' ? 'You' : 'Bot'}:</strong> {msg.content}
              </div>
            ))}
          </div>
          <div className="flex p-3 border-t border-gray-300">
            <input
              type="text"
              value={input}
              onChange={handleInputChange}
              onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
              className="flex-1 p-2 border border-gray-300 rounded-lg focus:outline-none"
              placeholder="Type a message..."
            />
            <button
              onClick={sendMessage}
              className="p-2 ml-2 text-white bg-blue-600 rounded-lg hover:bg-blue-700 focus:outline-none"
            >
              Send
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default Chatbot;