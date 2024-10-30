import React, { useEffect, useState } from 'react';

const Chatbot = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const userId = '<%=Session["user_id"]%>';

  const handleInputChange = (e) => {
    setInput(e.target.value);
  };

  const sendMessage = async () => {
    if (!input.trim()) return;
    const userMessage = { role: 'user', content: input };
    setMessages((prevMessages) => [...prevMessages, userMessage]);
    setInput("");

    console.log("Sending message:", { userId, role: 'user', content: input });

    try {
      const response = await fetch('http://localhost:3000/api/chat/message', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({userId, role: 'user', content: input}),
      });

      if (!response.ok) {
        throw new Error(`Error: ${response.statusText}`);
      }

      const data = await response.json();
      const botResponse = data.reply;
    //const utterance = new SpeechSynthesisUtterance("Hello How are you");   -- trying Voice Output
    //window.speechSynthesis.speak(utterance);

      const botMessage = { role: 'bot', content: botResponse };
      setMessages((prevMessages) => [...prevMessages, botMessage]);
    } catch (error) {
      console.error("Error sending message:", error);
      setMessages((prevMessages) => [
        ...prevMessages,
        { role: 'bot', content: "Sorry, I encountered an error. Please try again." },
      ]);
    }
  };

  useEffect(() => {
    if(userId) {
      fetchChatHistory();
    }
  }, [userId]);

  const fetchChatHistory = async () => {
    try {
      const response = await fetch(`http://localhost:3000/api/chat/history/${userId}`);
      if (!response.ok) {
        throw new Error(`Error: ${response.statusText}`);
      }
      const data = await response.json();
      setMessages(data.chat_history);
    } catch(error) {
      console.error("Error fetching chat history:", error);
    }
  };

  // Using browser's SpeechRecognition API for recognising voice input as well along with text. 
  const handleVoiceInput = () => {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    const recognition = new SpeechRecognition();

    recognition.onstart = () => {
      console.log("Voice recognition activated. Try speaking into the microphone.");
    };

    recognition.onresult = (event) => {
      const transcript = event.results[0][0].transcript;
      setInput(transcript); // Set the transcribed text to input
      sendMessage();
    };

    recognition.onerror = (event) => {
      console.error("Error occurred in recognition: ", event.error);
    };

    recognition.start(); // Starts voice recognition
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
              <div
                key={index}
                className={`mb-2 ${msg.role === 'user' ? 'text-right' : 'text-left'}`}
              >
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
            <button
              onClick={handleVoiceInput}
              className="p-2 ml-2 text-white bg-green-600 rounded-lg hover:bg-green-700 focus:outline-none"
            >
              🎤
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default Chatbot;
