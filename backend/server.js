// backend/server.js
import dotenv from "dotenv";
import router from './routes/user.routes.js';
import express from 'express';
import cors from 'cors';
import { GoogleGenerativeAI } from '@google/generative-ai';
import path from 'path';
import { connectDB } from './config/db.js';
import User from './models/user.model.js';
import { fileURLToPath } from 'url';


const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const app = express();
app.use(express.json());
app.use(cors());

app.use("/api/user", router);

dotenv.config();

const genAI = new GoogleGenerativeAI(process.env.API_KEY);
const model = genAI.getGenerativeModel({ model: "gemini-1.5-flash" });
//const model = genAI.getGenerativeModel({ model: "tunedModels/my-increment-model" });

const initialPrompts = ["Hey there! How are you feeling today?","Hi! I'm here for you. What’s on your mind?","Hello! How’s everything going for you today?","Hey! I’m ready to listen. How are you feeling?",
"Hi there! How are you doing, both physically and mentally?","Hello! What’s something you’d like to talk about today?","Hi! How’s your day been so far?","Hey! It’s good to see you. How are you holding up?",
"Hello! How can I support you today?","Hi! What’s been on your mind lately?","Hey! I’m here to help you feel better. How are you?","Hi! I’d love to hear how you’re doing today.",
"Hello! Is there anything on your mind that you'd like to share?","Hey! How’s your mood today?","Hi there! How are you feeling emotionally today?", "Hello! It’s great to see you. How’s everything going for you?",
"Hi! How are you feeling in this moment?", "Hey! I’m here if you need someone to talk to. How are you?","Hello! How’s your mental health been lately?","Hi! Let’s chat. How are you feeling today?",
"Hey! How’s your headspace today? Need a little support?","Hello! What’s something on your mind that we can talk about?","Hi there! How are things going for you today?","Hey! How are you really feeling today?",
"Hello! How has your week been so far?","Hi! Anything on your mind that you’d like to talk about?","Hey! How can I be helpful to you today?","Hi there! How’s your emotional well-being right now?",
"Hello! Let’s check in. How are you doing today?","Hi! What’s something you’ve been thinking about lately?","Hey! How have you been feeling emotionally this week?","Hello! How’s your mental health today?",
"Hi! I’m here for you. What’s been on your mind?","Hey! How are you feeling today, physically and mentally?","Hi there! Anything you’d like to talk about today?","Hello! How are you feeling emotionally and physically?",
"Hi! Let’s take a moment to check in. How are you feeling?","Hey! How’s your stress level today? Need to talk?","Hello! I’m ready to listen. How’s your day been?","Hi! How’s your mental space right now?",
"Hey! What’s one thing you’ve been thinking about lately?","Hello! How’s your energy level today? How are you feeling?","Hi! It’s great to check in with you. How are you feeling?","Hey! Let’s chat about how you’re doing today.",
"Hello! What’s been on your mind this week?","Hi! I’m here for you. How’s your mental health?","Hey! How’s your day going? Need someone to talk to?","Hello! How are you feeling emotionally and mentally?",
"Hi there! How can I help support you today?","Hey! What’s something you’ve been feeling lately?"
]; 

//cahtbot api init
app.post('/api/initChat', async (req, res) => {
  const initialPrompt = initialPrompts[Math.floor(Math.random() * initialPrompts.length)];
  
  try {
    const result = await model.generateContent(initialPrompt);
    const botResponse = await result.response.text(); // Ensure you await if necessary
    res.json({ reply: initialPrompt });
  } catch (error) {
    console.error("Error generating initial response:", error);
    res.status(500).json({ error: "Error generating initial response" });
  }
});

app.post('/api/chat', async (req, res) => {
  const userInput = req.body.input;
  const {userId} = req.body;

  const prompt = `You are a compassionate and knowledgeable mental health assistant. Your role is to listen to the user’s emotional concerns and 
    provide supportive advice. Act as a friend or caretaker to the user. Use simple, everyday language to keep things easy to understand. Make 
    sure your tone is conversational, and avoid technical terms or complex phrases. At the end ask a specific follow-up question related to their 
    health or well-being. Keep your ques;cdtions friendly and focused on keeping the conversation going in a positive, engaging way. Provide the best 
    course of action based on this input: ${userInput} Respond in 3-4 sentences.`;

    try {
      const result = await model.generateContent(prompt);
      const botResponse = await result.response.text(); // Ensure you await if necessary
      if (userId){
        try{
          await User.findByIdAndUpdate(userId, {
            $push: {
              chat_history: [
              {
                role: 'user',
                content: userInput,
                timestamp: new Date()
              }, 
              {
                role: 'bot',
                content: botResponse,
                timestamp: new Date()
              },
            ],
            },
          });
          console.log("Chat history saved successfully.");
        } catch(dbError) {
          console.error("Database error:", dbError);
        }
      }

      res.json({ reply: botResponse });
  } catch (error) {
    console.error("Error generating response:", error);
    res.status(500).json({ error: "Error generating response" });
  }
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
  connectDB();
  console.log("Server started at http://localhost:" + PORT);
});

// import dotenv from "dotenv";
// import router from './routes/user.routes.js';
// import express from 'express';
// import cors from 'cors';
// import { GoogleGenerativeAI } from '@google/generative-ai';
// import path from 'path';
// import { connectDB } from './config/db.js';
// import User from './models/user.model.js';
// import { fileURLToPath } from 'url';

// class ChatHistoryManager {
//   constructor() {
//     this.formatChatHistory = this.formatChatHistory.bind(this);
//     this.getRecentChatHistory = this.getRecentChatHistory.bind(this);
//     this.createContextAwarePrompt = this.createContextAwarePrompt.bind(this);
//   }

//   formatChatHistory(chatHistory) {
//     if (!chatHistory || chatHistory.length === 0) return '';
    
//     return chatHistory.map(msg => 
//       `${msg.role === 'user' ? 'User' : 'Assistant'}: ${msg.content}`
//     ).join('\n');
//   }

//   async getRecentChatHistory(userId, maxMessages = 5) {
//     try {
//       const user = await User.findById(userId);
//       if (!user || !user.chat_history) return [];
      
//       return user.chat_history.slice(-maxMessages);
//     } catch (error) {
//       console.error("Error fetching chat history:", error);
//       return [];
//     }
//   }

//   async createContextAwarePrompt(userId, currentInput) {
//     try {
//       const recentHistory = await this.getRecentChatHistory(userId);
//       const formattedHistory = this.formatChatHistory(recentHistory);
//       const historyContext = formattedHistory ? `\nPrevious conversation history:\n${formattedHistory}\n` : '';

//       return `${historyContext}
// Current user message: ${currentInput}

// You are a compassionate and knowledgeable mental health assistant named A.V.A. Your role is to listen to the user's emotional concerns and 
// provide supportive advice, taking into account the conversation history above. Act as a friend or caretaker to the user. 
// Use simple, everyday language to keep things easy to understand. Make sure your tone is conversational, and avoid technical 
// terms or complex phrases. At the end ask a specific follow-up question related to their health or well-being that builds on 
// the context of your conversation. Keep your questions friendly and focused on keeping the conversation going in a positive, 
// engaging way. Respond in 3-4 sentences.`;
//     } catch (error) {
//       console.error("Error creating context-aware prompt:", error);
//       return `You are a compassionate and knowledgeable mental health assistant named A.V.A. Your role is to listen to the user's emotional concerns and 
// provide supportive advice. Act as a friend or caretaker to the user. Use simple, everyday language to keep things easy to understand. Make 
// sure your tone is conversational, and avoid technical terms or complex phrases. At the end ask a specific follow-up question related to their 
// health or well-being. Keep your questions friendly and focused on keeping the conversation going in a positive, engaging way. Respond to this input: ${currentInput} in 3-4 sentences.`;
//     }
//   }
// }

// const __filename = fileURLToPath(import.meta.url);
// const __dirname = path.dirname(__filename);

// const app = express();
// app.use(express.json());
// app.use(cors());

// app.use("/api/user", router);

// dotenv.config();

// const genAI = new GoogleGenerativeAI(process.env.API_KEY);
// const model = genAI.getGenerativeModel({ model: "gemini-1.5-flash" });
// const chatHistoryManager = new ChatHistoryManager();

// const initialPrompts = ["Hey there! 👋 It's great to hear from you. Is there anything you'd like to talk about today? I'm here to listen and offer support. How are things going for you overall?"];

// app.post('/api/initChat', async (req, res) => {
//   const { userId } = req.body;
//   const initialPrompt = initialPrompts[Math.floor(Math.random() * initialPrompts.length)];
  
//   try {
//     if (userId) {
//       await User.findByIdAndUpdate(userId, {
//         $push: {
//           chat_history: {
//             role: 'bot',
//             content: initialPrompt,
//             timestamp: new Date()
//           }
//         }
//       });
//     }
    
//     res.json({ reply: initialPrompt });
//   } catch (error) {
//     console.error("Error generating initial response:", error);
//     res.status(500).json({ error: "Error generating initial response" });
//   }
// });

// app.post('/api/chat', async (req, res) => {
//   const userInput = req.body.input;
//   const { userId } = req.body;

//   if (!userInput) {
//     return res.status(400).json({ error: "User input is required" });
//   }

//   try {
//     // Create context-aware prompt using chat history
//     const contextAwarePrompt = await chatHistoryManager.createContextAwarePrompt(userId, userInput);
    
//     // Generate response using the context-aware prompt
//     const result = await model.generateContent(contextAwarePrompt);
//     const botResponse = await result.response.text();

//     if (userId) {
//       try {
//         await User.findByIdAndUpdate(userId, {
//           $push: {
//             chat_history: [
//               {
//                 role: 'user',
//                 content: userInput,
//                 timestamp: new Date()
//               },
//               {
//                 role: 'bot',
//                 content: botResponse,
//                 timestamp: new Date()
//               },
//             ],
//           },
//         });
//         console.log("Chat history saved successfully.");
//       } catch (dbError) {
//         console.error("Database error:", dbError);
//       }
//     }

//     res.json({ reply: botResponse });
//   } catch (error) {
//     console.error("Error generating response:", error);
//     res.status(500).json({ error: "Error generating response" });
//   }
// });

// const PORT = process.env.PORT || 3000;
// app.listen(PORT, () => {
//   console.log(`Server running on port ${PORT}`);
//   connectDB();
//   console.log("Server started at http://localhost:" + PORT);
// });

// import dotenv from "dotenv";
// import router from './routes/user.routes.js';
// import express from 'express';
// import cors from 'cors';
// import { GoogleGenerativeAI } from '@google/generative-ai';
// import path from 'path';
// import { connectDB } from './config/db.js';
// import User from './models/user.model.js';
// import { fileURLToPath } from 'url';

// // Initialize express app at the top level
// const app = express();
// app.use(express.json());
// app.use(cors());
// app.use("/api/user", router);

// dotenv.config();

// const __filename = fileURLToPath(import.meta.url);
// const __dirname = path.dirname(__filename);

// const genAI = new GoogleGenerativeAI(process.env.API_KEY);
// const model = genAI.getGenerativeModel({ model: "gemini-1.5-flash" });

// class ChatHistoryManager {
//   constructor() {
//     this.formatChatHistory = this.formatChatHistory.bind(this);
//     this.getRecentChatHistory = this.getRecentChatHistory.bind(this);
//     this.createContextAwarePrompt = this.createContextAwarePrompt.bind(this);
//     this.createInitialGreeting = this.createInitialGreeting.bind(this);
//   }

//   formatChatHistory(chatHistory) {
//     if (!chatHistory || chatHistory.length === 0) return '';
    
//     return chatHistory.map(msg => 
//       `${msg.role === 'user' ? 'User' : 'Assistant'}: ${msg.content}`
//     ).join('\n');
//   }

//   async getRecentChatHistory(userId, maxMessages = 5) {
//     try {
//       const user = await User.findById(userId);
//       if (!user || !user.chat_history) return [];
      
//       return user.chat_history.slice(-maxMessages);
//     } catch (error) {
//       console.error("Error fetching chat history:", error);
//       return [];
//     }
//   }

//   async createInitialGreeting(userId) {
//     try {
//       const user = await User.findById(userId);
//       console.log("User found:", user);
  
//       // If no user or no chat history, provide the default initial greeting
//       if (!user || !user.chat_history || user.chat_history.length === 0) {
//         console.log("No chat history found, returning initial greeting.");
//         return "Hey there! 👋 It's great to meet you. How are you feeling today?";
//       }
  
//       // Retrieve the last few messages from the chat history
//       const lastConversation = user.chat_history.slice(-6);
//       console.log("Last conversation retrieved:", lastConversation);
  
//       // Format the chat history for the greeting prompt
//       const formattedHistory = this.formatChatHistory(lastConversation);
//       console.log("Formatted chat history:", formattedHistory);
  
//       // Generate the greeting prompt with the existing chat context
//       const greetingPrompt = `Previous conversation history:
//   ${formattedHistory}
  
//   You are A.V.A., a mental health assistant. Generate a warm welcome message that specifically:
//   1. References the user's last mentioned health condition or concern
//   2. Shows genuine care about their current state
//   3. Asks a specific follow-up question about their previous health issue
//   4. Keep it natural and conversational
  
//   Important: Don't give a generic greeting. Make sure to explicitly mention what they told you last time about their health.
//   Limit to 2-3 sentences.`;
//       console.log("Greeting prompt created:", greetingPrompt);
  
//       // Generate the response using the generative model
//       const result = await model.generateContent(greetingPrompt);
//       const greeting = await result.response.text();
//       console.log("Generated greeting:", greeting);
  
//       // Prevent duplicate greetings if the last message was from the bot
//       if (lastConversation.length > 0 && lastConversation[lastConversation.length - 1].role === 'bot') {
//         await User.findByIdAndUpdate(userId, {
//           $pop: { chat_history: 1 }
//         });
//         console.log("Removed duplicate bot message from chat history.");
//       }
  
//       return greeting;
  
//     } catch (error) {
//       console.error("Error creating initial greeting:", error);
//       // Return a fallback message if any error occurs
//       return "Welcome back! I remember you weren't feeling well last time. How are you doing now?";
//     }
//   }
  

//   async createContextAwarePrompt(userId, currentInput) {
//     try {
//       const recentHistory = await this.getRecentChatHistory(userId);
//       const formattedHistory = this.formatChatHistory(recentHistory);
//       const historyContext = formattedHistory ? `\nPrevious conversation history:\n${formattedHistory}\n` : '';

//       return `${historyContext}
// Current user message: ${currentInput}

// You are a compassionate and knowledgeable mental health assistant named A.V.A. Your role is to listen to the user's emotional concerns and 
// provide supportive advice, taking into account the conversation history above. Act as a friend or caretaker to the user. 
// Use simple, everyday language to keep things easy to understand. Make sure your tone is conversational, and avoid technical 
// terms or complex phrases. At the end ask a specific follow-up question related to their health or well-being that builds on 
// the context of your conversation. Keep your questions friendly and focused on keeping the conversation going in a positive, 
// engaging way. Respond in 3-4 sentences.`;
//     } catch (error) {
//       console.error("Error creating context-aware prompt:", error);
//       return `You are a compassionate and knowledgeable mental health assistant named A.V.A. Your role is to listen to the user's emotional concerns and 
// provide supportive advice. Act as a friend or caretaker to the user. Use simple, everyday language to keep things easy to understand. Make 
// sure your tone is conversational, and avoid technical terms or complex phrases. At the end ask a specific follow-up question related to their 
// health or well-being. Keep your questions friendly and focused on keeping the conversation going in a positive, engaging way. Respond to this input: ${currentInput} in 3-4 sentences.`;
//     }
//   }
// }

// const chatHistoryManager = new ChatHistoryManager();

// // Route handlers
// app.post('/api/initChat', async (req, res) => {
//   const { userId } = req.body;
//   console.log("Received userId:", userId);

//   if (!userId) {
//     return res.status(400).json({ error: "User ID is required" });
//   }
  
//   try {
//     // Check if there's already an active conversation
//     const user = await User.findById(userId);
//     if (user && user.chat_history && user.chat_history.length > 0) {
//       const lastMessage = user.chat_history[user.chat_history.length - 1];
//       const timeSinceLastMessage = new Date() - new Date(lastMessage.timestamp);
//       const hoursSinceLastMessage = timeSinceLastMessage / (1000 * 60 * 60);
      
//       // If last message was less than 1 hour ago, don't send a new greeting
//       if (hoursSinceLastMessage < 1) {
//         return res.json({ reply: null });
//       }
//     }
    
//     const initialGreeting = await chatHistoryManager.createInitialGreeting(userId);
    
//     if (userId) {
//       await User.findByIdAndUpdate(userId, {
//         $push: {
//           chat_history: {
//             role: 'bot',
//             content: initialGreeting,
//             timestamp: new Date()
//           }
//         }
//       });
//     }
    
//     res.json({ reply: initialGreeting });
//   } catch (error) {
//     console.error("Error generating initial response:", error);
//     res.status(500).json({ error: "Error generating initial response" });
//   }
// });

// app.post('/api/chat', async (req, res) => {
//   const userInput = req.body.input;
//   const { userId } = req.body;

//   if (!userInput) {
//     return res.status(400).json({ error: "User input is required" });
//   }

//   try {
//     const contextAwarePrompt = await chatHistoryManager.createContextAwarePrompt(userId, userInput);
//     const result = await model.generateContent(contextAwarePrompt);
//     const botResponse = await result.response.text();

//     if (userId) {
//       try {
//         await User.findByIdAndUpdate(userId, {
//           $push: {
//             chat_history: [
//               {
//                 role: 'user',
//                 content: userInput,
//                 timestamp: new Date()
//               },
//               {
//                 role: 'bot',
//                 content: botResponse,
//                 timestamp: new Date()
//               },
//             ],
//           },
//         });
//         console.log("Chat history saved successfully.");
//       } catch (dbError) {
//         console.error("Database error:", dbError);
//       }
//     }

//     res.json({ reply: botResponse });
//   } catch (error) {
//     console.error("Error generating response:", error);
//     res.status(500).json({ error: "Error generating response" });
//   }
// });

// const PORT = process.env.PORT || 3000;
// app.listen(PORT, () => {
//   console.log(`Server running on port ${PORT}`);
//   connectDB();
//   console.log("Server started at http://localhost:" + PORT);
// });