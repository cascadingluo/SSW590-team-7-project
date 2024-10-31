import User from "../models/user.model.js";
import mongoose from 'mongoose';

export const saveChatMessage = async (req, res) => {
  try {
    const { userId, role, content } = req.body;

    if (!mongoose.Types.ObjectId.isValid(userId)) {
        return res.status(400).json({ error: "Invalid user ID format" });
    }
    const user = await User.findById(userId);
    if (!user) {
      return res.status(404).json({ error: "User not found" });
    }

    user.chat_history.push({
      role,
      content,
      timestamp: new Date()
    });

    await user.save();
    return res.status(200).json({ message: "Chat message saved successfully" });
  } catch (error) {
    console.error("Error saving chat message:", error);
    return res.status(500).json({ error: "Error saving chat message" });
  }
};

export const getChatHistory = async (req, res) => {
  try {
    const { userId } = req.params;
    if (!mongoose.Types.ObjectId.isValid(userId)) {
        return res.status(400).json({ error: "Invalid user ID format" });
    }
    const user = await User.findById(userId);
    if (!user) {
      return res.status(404).json({ error: "User not found" });
    }

    return res.status(200).json({ chat_history: user.chat_history });
  } catch (error) {
    console.error("Error fetching chat history:", error);
    return res.status(500).json({ error: "Error fetching chat history" });
  }
};