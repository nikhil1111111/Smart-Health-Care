// routes/auth.js

const express = require('express');
const jwt = require('jsonwebtoken');
const bcrypt = require('bcryptjs');
const User = require('../models/User'); // Assuming you have a User model
const router = express.Router();

// Register route (optional)
// router.post('/register', async (req, res) => {
//   try {
//     const { username, password } = req.body;
//     const hashedPassword = await bcrypt.hash(password, 10);
//     const user = new User({ username, password: hashedPassword });
//     await user.save();
//     res.status(201).json({ message: 'User created' });
//   } catch (err) {
//     res.status(500).json({ error: 'Server error' });
//   }
// });

// Login route
router.post('/login', async (req, res) => {
  const { username, password } = req.body;

  // Check if user exists
  const user = await User.findOne({ username });
  if (!user) {
    return res.status(404).json({ error: 'User not found' });
  }

  // Check password
  const isMatch = await bcrypt.compare(password, user.password);
  if (!isMatch) {
    return res.status(400).json({ error: 'Invalid credentials' });
  }

  // Generate JWT Token
  const token = jwt.sign({ userId: user._id }, process.env.JWT_SECRET, {
    expiresIn: '1h',
  });
  res.json({ token });
});

module.exports = router;












// const express = require('express');
// const bcrypt = require('bcryptjs');
// const jwt = require('jsonwebtoken');
// const router = express.Router();

// // Fake users (For simplicity)
// const users = [{ username: 'admin', password: '123456' }];

// // Login Route
// router.post('/login', (req, res) => {
//     const { username, password } = req.body;

//     const user = users.find(u => u.username === username);
//     if (!user) return res.status(400).json({ msg: 'Invalid credentials' });

//     const isMatch = password === user.password;
//     if (!isMatch) return res.status(400).json({ msg: 'Invalid credentials' });

//     const token = jwt.sign({ userId: user.username }, 'mysecret', { expiresIn: '1h' });
//     res.json({ token });
// });

// // Middleware to protect routes
// const auth = (req, res, next) => {
//     const token = req.header('x-auth-token');
//     if (!token) return res.status(401).json({ msg: 'No token, authorization denied' });

//     try {
//         const decoded = jwt.verify(token, 'mysecret');
//         req.user = decoded.userId;
//         next();
//     } catch (err) {
//         res.status(401).json({ msg: 'Token is not valid' });
//     }
// };

// module.exports = router;
// module.exports.auth = auth;
