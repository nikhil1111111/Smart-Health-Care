const express = require('express');
const router = express.Router();
const Blog = require('../models/Blog');
const auth = require('../middleware/auth');

// Create a new blog post (Protected)
router.post('/', auth, async (req, res) => {
    const { title, content, author } = req.body;

    if (!title || !content || !author) {
        return res.status(400).json({ msg: 'Please include all fields' });
    }

    const newBlog = new Blog({ title, content, author });
    await newBlog.save();
    res.json(newBlog);
});

// Get all blog posts
router.get('/', async (req, res) => {
    const blogs = await Blog.find().sort({ date: -1 });
    res.json(blogs);
});

// Get single blog post by ID
router.get('/:id', async (req, res) => {
    const blog = await Blog.findById(req.params.id);
    if (!blog) return res.status(404).json({ msg: 'Blog not found' });
    res.json(blog);
});

module.exports = router;
