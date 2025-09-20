// Diagnosis Form Submission
document.getElementById('diagnosisForm').addEventListener('submit', function(event) {
    event.preventDefault();
    const patientName = document.getElementById('patient_name').value;
    const symptoms = document.getElementById('symptoms').value;

    const formData = new FormData();
    formData.append('patient_name', patientName);
    formData.append('symptoms', symptoms);

    fetch('/api/diagnosis', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('diagnosisResult').innerHTML = `
            <div class="result-box">
                <h3>Diagnosis Result</h3>
                <p><strong>Patient:</strong> ${patientName}</p>
                <p><strong>Symptoms:</strong> ${symptoms}</p>
                <p><strong>Diagnosis:</strong> ${data.diagnosis}</p>
            </div>
        `;
    })
    .catch((error) => {
        console.error('Error:', error);
        document.getElementById('diagnosisResult').innerHTML = `
            <div class="error-box">
                <p>Error getting diagnosis. Please try again.</p>
            </div>
        `;
    });
});

// Consultation Booking Form Submission
document.getElementById('consultationForm').addEventListener('submit', function(event) {
    event.preventDefault();
    const name = document.getElementById('name').value;
    const email = document.getElementById('email').value;
    const date = document.getElementById('date').value;

    const formData = new FormData();
    formData.append('name', name);
    formData.append('email', email);
    formData.append('date', date);

    fetch('/api/consultation', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('consultationResult').innerHTML = `
            <div class="result-box">
                <h3>Booking Confirmation</h3>
                <p>${data.message}</p>
                <p><strong>Details:</strong></p>
                <p>Name: ${name}</p>
                <p>Email: ${email}</p>
                <p>Date: ${date}</p>
            </div>
        `;
    })
    .catch((error) => {
        console.error('Error:', error);
        document.getElementById('consultationResult').innerHTML = `
            <div class="error-box">
                <p>Error booking consultation. Please try again.</p>
            </div>
        `;
    });
});

// Healthcare Plan Form Submission
document.getElementById('healthcarePlanForm').addEventListener('submit', function(event) {
    event.preventDefault();
    const age = document.getElementById('age').value;
    const goals = document.getElementById('goals').value;

    const formData = new FormData();
    formData.append('age', age);
    formData.append('goals', goals);

    fetch('/api/healthcare-plan', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('healthcarePlanResult').innerHTML = `
            <div class="result-box">
                <h3>Your Personalized Healthcare Plan</h3>
                <p><strong>Age:</strong> ${age}</p>
                <p><strong>Goals:</strong> ${goals}</p>
                <p><strong>Plan:</strong> ${data.plan}</p>
            </div>
        `;
    })
    .catch((error) => {
        console.error('Error:', error);
        document.getElementById('healthcarePlanResult').innerHTML = `
            <div class="error-box">
                <p>Error generating healthcare plan. Please try again.</p>
            </div>
        `;
    });
});

// Health Data Analysis Form Submission
document.getElementById('dataAnalysisForm').addEventListener('submit', function(event) {
    event.preventDefault();
    const fileInput = document.getElementById('dataUpload');
    const file = fileInput.files[0];

    if (!file) {
        document.getElementById('dataAnalysisResult').innerHTML = `
            <div class="error-box">
                <p>Please select a file to upload.</p>
            </div>
        `;
        return;
    }

    const formData = new FormData();
    formData.append('dataUpload', file);

    fetch('/api/data-analysis', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('dataAnalysisResult').innerHTML = `
            <div class="result-box">
                <h3>Analysis Complete</h3>
                <p><strong>File:</strong> ${file.name}</p>
                <p><strong>Result:</strong> ${data.analysis}</p>
            </div>
        `;
    })
    .catch((error) => {
        console.error('Error:', error);
        document.getElementById('dataAnalysisResult').innerHTML = `
            <div class="error-box">
                <p>Error analyzing data. Please try again.</p>
            </div>
        `;
    });
});

// Blog Integration
let blogOffset = 0;
const blogsPerPage = 5;

// Load blog posts
function loadBlogPosts() {
    fetch(`http://localhost:5001/api/blogs?limit=${blogsPerPage}&offset=${blogOffset}`)
    .then(response => response.json())
    .then(data => {
        const blogContainer = document.getElementById('blogPosts');

        if (data.length === 0 && blogOffset === 0) {
            blogContainer.innerHTML = '<p>No blog posts available.</p>';
            return;
        }

        if (data.length === 0) {
            document.getElementById('loadMoreBlogs').style.display = 'none';
            return;
        }

        data.forEach(post => {
            const postElement = document.createElement('div');
            postElement.className = 'blog-post';
            postElement.innerHTML = `
                <h3>${post.title}</h3>
                <p><strong>By:</strong> ${post.author}</p>
                <p>${post.content.substring(0, 200)}...</p>
                <p><small>${new Date(post.date).toLocaleDateString()}</small></p>
                <button onclick="readMore('${post._id}')">Read More</button>
            `;
            blogContainer.appendChild(postElement);
        });

        blogOffset += blogsPerPage;

        if (data.length === blogsPerPage) {
            document.getElementById('loadMoreBlogs').style.display = 'block';
        } else {
            document.getElementById('loadMoreBlogs').style.display = 'none';
        }
    })
    .catch((error) => {
        console.error('Error loading blogs:', error);
        document.getElementById('blogPosts').innerHTML = `
            <div class="error-box">
                <p>Error loading blog posts. Make sure the blog server is running on port 5001.</p>
            </div>
        `;
    });
}

// Load more blogs
document.getElementById('loadMoreBlogs').addEventListener('click', function() {
    loadBlogPosts();
});

// Read more function
function readMore(postId) {
    fetch(`http://localhost:5001/api/blogs/${postId}`)
    .then(response => response.json())
    .then(post => {
        const blogContainer = document.getElementById('blogPosts');
        blogContainer.innerHTML = `
            <div class="blog-post-full">
                <button onclick="loadBlogPosts()">← Back to Posts</button>
                <h2>${post.title}</h2>
                <p><strong>By:</strong> ${post.author}</p>
                <p><small>${new Date(post.date).toLocaleDateString()}</small></p>
                <div>${post.content}</div>
            </div>
        `;
    })
    .catch((error) => {
        console.error('Error loading blog post:', error);
    });
}

// Initialize blog loading
document.addEventListener('DOMContentLoaded', function() {
    loadBlogPosts();
});

// Smooth scrolling for navigation links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
        e.preventDefault();
        document.querySelector(this.getAttribute('href')).scrollIntoView({
            behavior: 'smooth'
        });
    });
});
