import User from "../models/user.model.js";

export const login = async (req, res) => {
    try {
        const user = await User.findOne({ username: req.body.username });
        if (user) {
          const result = req.body.password === user.password;
          if (result) {
            return res.status(200).json(user);
          } else {
            res.status(400).json({ error: "Incorrect password" });
          }
        } else {
          res.status(400).json({ error: "User doesn't exist" });
        }
      } catch (error) {
        res.status(400).json({ error });
      }
};

export const signup = async (req, res) => {
  const username = req.body.username;
  const password = req.body.password;
  const usernameExists = await User.findOne({ username });
  if(usernameExists) {
    return res.status(400).json({ error: "Username exists." });
  }
  else{
    const user = await User.create({
      username: username,
      password: password,
    });  
    res.status(200).json(user);
  }
};