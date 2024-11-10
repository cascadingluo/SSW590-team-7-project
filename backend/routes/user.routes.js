import express from "express";
import { login, signup } from "../controllers/user.controller.js";
import path from "path";
import { fileURLToPath } from 'url';

const router = express.Router();

router.post("/signup", signup);
router.post("/login", login);
router.get("/reminders", (req, res) => {
    res.sendFile(path.join(__dirname, "../../frontend/template/reminders.html"));  // Adjust path if necessary
  });

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

router.get("/reminders", (req, res) => {
    res.sendFile(path.join(__dirname, "../../frontend/templates/reminders.html"));
});


export default router;
