# 🏥 Smart Healthcare Platform

A comprehensive healthcare management system with AI diagnosis, consultation booking, personalized healthcare plans, health data analysis, and an integrated blog system.

## ✨ Features

### 🏠 Dashboard Services
- **AI Diagnosis**: Get instant health assessments based on symptoms
- **Consultation Booking**: Schedule appointments with healthcare providers
- **Healthcare Plans**: Receive personalized health and fitness recommendations
- **Data Analysis**: Upload and analyze health data files (CSV, JSON, TXT)
- **Blog Integration**: Access healthcare articles and resources

### 📝 Blog System
- Create, read, update, and delete blog posts
- User authentication and authorization
- Pagination support
- RESTful API endpoints

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 14+
- MongoDB (for blog system)

### 1. Clone and Setup
```bash
git clone <repository-url>
cd Smart-Health-Care
```

### 2. Install Dependencies

#### Python Dependencies
```bash
pip install -r requirements.txt
```

#### Node.js Dependencies
```bash
cd healthcare-blog
npm install
cd ..
```

### 3. Setup Database
```bash
python db_setup.py
```

### 4. Start All Servers
```bash
python start_servers.py
```

This will start:
- **Flask Backend**: http://localhost:5000
- **Node.js Blog API**: http://localhost:5001
- **Frontend Dashboard**: http://localhost:5000

## 🛠️ Manual Server Startup

### Start Flask Backend Only
```bash
python app.py
```

### Start Blog Server Only
```bash
cd healthcare-blog
node server.js
```

## 📊 API Endpoints

### Flask Backend (Port 5000)

#### Diagnosis
- `POST /api/diagnosis` - Get AI diagnosis from symptoms

#### Consultation
- `POST /api/consultation` - Book a consultation

#### Healthcare Plans
- `POST /api/healthcare-plan` - Generate personalized healthcare plan

#### Data Analysis
- `POST /api/data-analysis` - Analyze health data files

### Blog API (Port 5001)

#### Blog Posts
- `GET /api/blogs` - Get all blog posts (with pagination)
- `GET /api/blogs/:id` - Get single blog post
- `POST /api/blogs` - Create new blog post (requires auth)
- `PUT /api/blogs/:id` - Update blog post (requires auth)
- `DELETE /api/blogs/:id` - Delete blog post (requires auth)

#### Authentication
- `POST /api/auth/login` - User login

#### Health Check
- `GET /api/health` - Server health status

## 🗄️ Database Schema

### SQLite Database (db/healthcare.db)

#### Patients Table
- Patient information and diagnosis history

#### Consultations Table
- Appointment booking records

#### Healthcare Plans Table
- Personalized health recommendations

#### Health Data Analysis Table
- File upload and analysis records

### MongoDB (healthcare_blog)
- Blog posts and user management

## 🎨 Frontend Features

- **Responsive Design**: Works on desktop and mobile
- **Interactive Forms**: Real-time validation and feedback
- **Blog Integration**: Seamless access to healthcare articles
- **Modern UI**: Clean, professional healthcare interface
- **Error Handling**: User-friendly error messages

## 🔧 Development

### Project Structure
```
Smart-Health-Care/
├── app.py                 # Flask backend
├── db_setup.py           # Database initialization
├── start_servers.py      # Server management script
├── requirements.txt      # Python dependencies
├── templates/
│   └── index2.html       # Main dashboard
├── static/
│   ├── app.js           # Frontend JavaScript
│   └── style.css        # Styling
├── db/
│   └── healthcare.db    # SQLite database
└── healthcare-blog/     # Node.js blog system
    ├── server.js
    ├── models/
    ├── routes/
    └── middleware/
```

### Adding New Features

1. **Backend Changes**: Modify `app.py` for new API endpoints
2. **Frontend Changes**: Update `templates/index2.html` and `static/app.js`
3. **Database Changes**: Update `db_setup.py` for new tables
4. **Blog Features**: Modify files in `healthcare-blog/` directory

## 🐛 Troubleshooting

### Common Issues

1. **Port Already in Use**
   ```bash
   # Kill processes using ports 5000 or 5001
   lsof -ti:5000 | xargs kill -9
   lsof -ti:5001 | xargs kill -9
   ```

2. **Database Connection Issues**
   ```bash
   # Reset database
   rm db/healthcare.db
   python db_setup.py
   ```

3. **MongoDB Not Running**
   ```bash
   # Start MongoDB service
   sudo systemctl start mongod
   ```

4. **Node.js Dependencies Missing**
   ```bash
   cd healthcare-blog
   rm -rf node_modules package-lock.json
   npm install
   ```

### Logs and Debugging

- **Flask Logs**: Check console output when running `app.py`
- **Node.js Logs**: Check console output when running `server.js`
- **Database**: Run `python db_setup.py` to check database status

## 📝 Sample Data

The system includes sample data for testing:
- Sample patients with various symptoms
- Sample consultation bookings
- Sample healthcare plans
- Blog posts (when MongoDB is populated)

## 🔐 Security Features

- Input validation and sanitization
- SQL injection protection
- CORS configuration
- Authentication middleware for blog system
- Error handling without information leakage

## 📈 Performance

- Database indexes for faster queries
- Pagination for blog posts
- Efficient file upload handling
- Optimized static file serving

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
1. Check the troubleshooting section
2. Review the logs
3. Ensure all prerequisites are installed
4. Try the manual startup process

---

**Happy coding! 🏥💻**
