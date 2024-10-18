// backend/server.js
require('dotenv').config();
const express = require('express');
const cors = require('cors');
const { GoogleGenerativeAI } = require('@google/generative-ai');

const app = express();
app.use(cors());
app.use(express.json());

const genAI = new GoogleGenerativeAI(process.env.API_KEY);
const model = genAI.getGenerativeModel({ model: "gemini-1.5-flash" });

app.post('/api/chat', async (req, res) => {
  const userInput = req.body.input;

  const prompt = `You are a professional mental health counselor. Provide the best course of action based on this input: "${userInput}" Respond in 3-4 sentences.`;

  try {
    const result = await model.generateContent(prompt);
    const botResponse = await result.response.text(); // Ensure you await if necessary

    res.json({ reply: botResponse });
  } catch (error) {
    console.error("Error generating response:", error);
    res.status(500).json({ error: "Error generating response" });
  }
});

const PORT = process.env.PORT || 5000;
app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
