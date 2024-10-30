import express from 'express';
import { saveChatMessage, getChatHistory } from '../controllers/chat.controller.js';

const router = express.Router();

router.post('/message', saveChatMessage);
router.get('/history/:userId', getChatHistory);

export default router