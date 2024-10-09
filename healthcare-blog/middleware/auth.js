// middleware/auth.js

const jwt = require('jsonwebtoken');

// Middleware to check JWT token in requests
const auth = (req, res, next) => {
  const token = req.header('Authorization');
  if (!token) {
    return res.status(401).json({ error: 'No token, authorization denied' });
  }

  try {
    // Verify token
    const decoded = jwt.verify(token, process.env.JWT_SECRET);
    req.user = decoded.userId; // Add userId to req object
    next(); // Proceed to the next middleware
  } catch (err) {
    res.status(401).json({ error: 'Token is not valid' });
  }
};

module.exports = auth;