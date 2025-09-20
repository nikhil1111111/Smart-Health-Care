const express = require('express');
const router = express.Router();
const Blog = require('../models/Blog');
const auth = require('../middleware/auth');

// Create a new blog post (Protected)
router.post('/', auth, async (req, res) => {
    try {
        const { title, content, author } = req.body;

        if (!title || !content || !author) {
            return res.status(400).json({ msg: 'Please include all fields' });
        }

        const newBlog = new Blog({ title, content, author });
        await newBlog.save();
        res.json(newBlog);
    } catch (err) {
        res.status(500).json({ error: 'Server error' });
    }
});

// Get all blog posts with pagination
router.get('/', async (req, res) => {
    try {
        const limit = parseInt(req.query.limit) || 10;
        const offset = parseInt(req.query.offset) || 0;

        const blogs = await Blog.find()
            .sort({ date: -1 })
            .limit(limit)
            .skip(offset);

        const total = await Blog.countDocuments();

        res.json({
            blogs,
            pagination: {
                total,
                limit,
                offset,
                hasMore: offset + limit < total
            }
        });
    } catch (err) {
        res.status(500).json({ error: 'Server error' });
    }
});

// Get single blog post by ID
router.get('/:id', async (req, res) => {
    try {
        const blog = await Blog.findById(req.params.id);
        if (!blog) return res.status(404).json({ msg: 'Blog not found' });
        res.json(blog);
    } catch (err) {
        res.status(500).json({ error: 'Server error' });
    }
});

// Update blog post (Protected)
router.put('/:id', auth, async (req, res) => {
    try {
        const { title, content, author } = req.body;
        const blog = await Blog.findByIdAndUpdate(
            req.params.id,
            { title, content, author },
            { new: true }
        );
        if (!blog) return res.status(404).json({ msg: 'Blog not found' });
        res.json(blog);
    } catch (err) {
        res.status(500).json({ error: 'Server error' });
    }
});

// Delete blog post (Protected)
router.delete('/:id', auth, async (req, res) => {
    try {
        const blog = await Blog.findByIdAndDelete(req.params.id);
        if (!blog) return res.status(404).json({ msg: 'Blog not found' });
        res.json({ msg: 'Blog post deleted' });
    } catch (err) {
        res.status(500).json({ error: 'Server error' });
    }
});

module.exports = router;
