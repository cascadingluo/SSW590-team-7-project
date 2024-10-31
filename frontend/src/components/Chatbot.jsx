import React, { useState, useEffect } from 'react';

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
    console.log(userMessage);
    setMessages((prevMessages) => [...prevMessages, userMessage]);
    setInput("");

    try {
      const response = await fetch('http://localhost:3000/api/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ input }),
      });

      if (!response.ok) {
        throw new Error(`Error: ${response.statusText}`);
      }

      const data = await response.json();
      const botResponse = data.reply;

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

  // Voice input handler remains unchanged
  const handleVoiceInput = () => {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    const recognition = new SpeechRecognition();

    recognition.onstart = () => {
      console.log("Voice recognition activated. Try speaking into the microphone.");
    };

    recognition.onresult = (event) => {
      const transcript = event.results[0][0].transcript;
      setInput(transcript);
      sendMessage();
    };

    recognition.onerror = (event) => {
      console.error("Error occurred in recognition: ", event.error);
    };

    recognition.start();
  };

  // Add useEffect hook for text-to-speech
  useEffect(() => {
    console.log("useEffect triggered");
    if (messages.length > 0) {
      const lastMessage = messages[messages.length - 1];
      console.log("Last message:", lastMessage);
      if (lastMessage.role === 'bot') {
        console.log("Initiating speech synthesis");
        window.speechSynthesis.cancel();
        const utterance = new SpeechSynthesisUtterance(lastMessage.content);
        window.speechSynthesis.speak(utterance);
      }
    }
  }, [messages]);
  

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
