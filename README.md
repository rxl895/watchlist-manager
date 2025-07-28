# 🎬 Watchlist Manager

[![GitHub stars](https://img.shields.io/github/stars/rxl895/watchlist-manager?style=social)](https://github.com/rxl895/watchlist-manager/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/rxl895/watchlist-manager?style=social)](https://github.com/rxl895/watchlist-manager/network/members)
[![GitHub issues](https://img.shields.io/github/issues/rxl895/watchlist-manager)](https://github.com/rxl895/watchlist-manager/issues)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![React](https://img.shields.io/badge/react-%2320232a.svg?style=flat&logo=react&logoColor=%2361DAFB)](https://reactjs.org/)

A modern, AI-powered watchlist manager that helps you track movies and TV series you've watched, with intelligent recommendations and analytics powered by Large Language Models.

## ✨ Features

### 🎯 Core Features
- **Track Movies & TV Series**: Add titles with detailed metadata
- **Watch History**: Record multiple watches with timestamps
- **Platform Tracking**: Keep track of streaming platforms and availability
- **Personal Ratings**: Rate content and add personal notes
- **Statistics Dashboard**: Visual analytics of your viewing habits

### 🤖 AI-Powered Features
- **Smart Recommendations**: LLM-powered suggestions based on your viewing history
- **Content Analysis**: AI insights about your preferences and patterns
- **Mood-Based Suggestions**: Get recommendations based on your current mood
- **Similar Content Discovery**: Find similar movies/shows using semantic search
- **Review Summarization**: AI-generated summaries of your viewing patterns

### 🔧 Technical Features
- **RESTful API**: FastAPI backend with automatic OpenAPI documentation
- **Modern Frontend**: React-based responsive web interface
- **Multiple Database Support**: SQLite for development, PostgreSQL for production
- **Docker Support**: Containerized deployment
- **CI/CD Pipeline**: GitHub Actions for testing and deployment
- **API Rate Limiting**: Built-in rate limiting and security features

## 🚀 Quick Start

### Prerequisites
- **Python 3.9+** - [Download here](https://www.python.org/downloads/)
- **Node.js 16+** and **npm** - [Download here](https://nodejs.org/)
- **Git** - [Download here](https://git-scm.com/)

### 🔥 Run Locally (Step-by-Step)

#### 1️⃣ Clone the Repository
```bash
git clone https://github.com/rxl895/watchlist-manager.git
cd watchlist-manager
```

#### 2️⃣ Setup Backend (FastAPI)
```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate

# Install Python dependencies
pip install -r requirements.txt

# Start the backend server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**✅ Backend will be running at:** http://localhost:8000
- **API Docs:** http://localhost:8000/docs
- **Health Check:** http://localhost:8000/health

#### 3️⃣ Setup Frontend (React) - In New Terminal
```bash
# Open new terminal and navigate to frontend
cd watchlist-manager/frontend

# Install Node.js dependencies
npm install

# Start the React development server
npm start
```

**✅ Frontend will be running at:** http://localhost:3000

#### 4️⃣ Open Your Browser
Visit **http://localhost:3000** to see your Watchlist Manager! 🎉

### 🐳 Alternative: Docker Setup (One Command)
```bash
git clone https://github.com/rxl895/watchlist-manager.git
cd watchlist-manager
docker-compose up -d
```

Then visit: http://localhost:3000

### 🛠️ Development Commands

#### Backend Commands
```bash
cd backend
source venv/bin/activate  # Activate virtual environment

# Start development server
uvicorn main:app --reload

# Run tests
pytest tests/ -v

# View API documentation
# http://localhost:8000/docs
```

#### Frontend Commands
```bash
cd frontend

# Start development server
npm start

# Build for production
npm run build

# Run tests
npm test

# Install new packages
npm install <package-name>
```

### 🎯 What You Can Do

Once both servers are running, you can:

1. **📚 View Your Watchlist** - See movies and TV shows you've added
2. **➕ Add New Content** - Use the "Add Content" tab to add movies/shows
3. **🔄 Update Status** - Change status from "Planned" to "Watching" to "Completed"
4. **🤖 Get AI Recommendations** - Click "AI Recommendations" for personalized suggestions
5. **📊 View Statistics** - See your viewing analytics in the "Statistics" tab
6. **🗑️ Delete Items** - Remove content you no longer want to track

### 🔧 Troubleshooting

#### Common Issues:

**Backend won't start:**
```bash
# Make sure virtual environment is activated
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

**Frontend won't start:**
```bash
# Clear npm cache
npm cache clean --force

# Delete node_modules and reinstall
rm -rf node_modules package-lock.json
npm install
```

**Port already in use:**
```bash
# Kill process on port 8000 (backend)
lsof -ti:8000 | xargs kill -9

# Kill process on port 3000 (frontend) 
lsof -ti:3000 | xargs kill -9
```

**CORS errors:**
- Make sure backend is running on port 8000
- Make sure frontend is running on port 3000

## 📖 API Documentation

Once the backend is running, visit:
- **Interactive API Docs**: http://localhost:8000/docs
- **ReDoc Documentation**: http://localhost:8000/redoc

### Key Endpoints

#### Movies & TV Shows
- `GET /api/v1/content/` - List all content
- `POST /api/v1/content/` - Add new content
- `GET /api/v1/content/{id}` - Get specific content
- `PUT /api/v1/content/{id}` - Update content
- `DELETE /api/v1/content/{id}` - Delete content

#### Watch History
- `POST /api/v1/watches/` - Record a watch
- `GET /api/v1/watches/` - Get watch history
- `GET /api/v1/stats/` - Get viewing statistics

#### AI Features
- `POST /api/v1/ai/recommend` - Get AI recommendations
- `POST /api/v1/ai/analyze` - Analyze viewing patterns
- `POST /api/v1/ai/mood-suggest` - Mood-based suggestions

## 🏗️ Project Structure

```
watchlist-manager/
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py         # FastAPI application
│   │   ├── models/         # Database models
│   │   ├── routes/         # API routes
│   │   ├── services/       # Business logic
│   │   ├── ai/            # LLM integration
│   │   └── utils/         # Utilities
│   ├── tests/             # Backend tests
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/              # React frontend
│   ├── public/
│   ├── src/
│   │   ├── components/    # React components
│   │   ├── pages/        # Page components
│   │   ├── hooks/        # Custom hooks
│   │   ├── services/     # API services
│   │   └── utils/        # Utilities
│   ├── package.json
│   └── Dockerfile
├── docs/                  # Documentation
├── scripts/              # Utility scripts
├── .github/
│   └── workflows/        # GitHub Actions
├── docker-compose.yml
├── .gitignore
└── README.md
```

## 🤖 LLM Integration

This project showcases integration with various LLM providers:

### Supported Providers
- **OpenAI GPT**: For recommendations and analysis
- **Anthropic Claude**: Alternative LLM option
- **Local Models**: Ollama integration for privacy
- **Hugging Face**: Open-source model support

### AI Features Implementation
- **Semantic Search**: Vector embeddings for content similarity
- **Recommendation Engine**: Collaborative filtering + LLM insights
- **Natural Language Queries**: Ask questions about your watchlist
- **Trend Analysis**: AI-powered viewing pattern analysis

## 📊 Analytics & Insights

### Dashboard Features
- **Viewing Statistics**: Hours watched, completion rates
- **Genre Analysis**: Favorite genres and discovery patterns
- **Platform Usage**: Most used streaming services
- **Temporal Patterns**: When you watch most content
- **Rating Insights**: Your rating patterns and preferences

### AI Insights
- **Preference Evolution**: How your tastes change over time
- **Mood Correlation**: Content choices vs. time/season
- **Discovery Recommendations**: Suggest underexplored genres
- **Binge Pattern Analysis**: Identify binge-watching behaviors

## 🔧 Configuration

### Environment Variables
```bash
# Backend (.env)
DATABASE_URL=sqlite:///./watchlist.db
SECRET_KEY=your-secret-key
OPENAI_API_KEY=your-openai-key
TMDB_API_KEY=your-tmdb-key
CORS_ORIGINS=http://localhost:3000

# Production
DATABASE_URL=postgresql://user:pass@localhost/watchlist
REDIS_URL=redis://localhost:6379
```

### LLM Configuration
```python
# backend/app/config.py
class Settings:
    openai_api_key: str = ""
    anthropic_api_key: str = ""
    ollama_base_url: str = "http://localhost:11434"
    embedding_model: str = "text-embedding-ada-002"
    chat_model: str = "gpt-3.5-turbo"
```

## 🧪 Testing

```bash
# Backend tests
cd backend
pytest tests/ -v --cov=app

# Frontend tests
cd frontend
npm test

# Integration tests
docker-compose -f docker-compose.test.yml up --abort-on-container-exit
```

## 🚀 Deployment

### Docker Deployment
```bash
docker-compose -f docker-compose.prod.yml up -d
```

### GitHub Pages (Frontend Only)
The frontend can be deployed to GitHub Pages for demo purposes.

### Cloud Deployment
- **Backend**: Deploy to Railway, Render, or Heroku
- **Database**: PostgreSQL on Supabase or Railway
- **Frontend**: Vercel or Netlify

## 🤝 Contributing

Contributions are welcome! Please read our [Contributing Guidelines](CONTRIBUTING.md).

### Development Setup
1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes and add tests
4. Commit your changes: `git commit -m 'Add amazing feature'`
5. Push to the branch: `git push origin feature/amazing-feature`
6. Open a Pull Request

### Areas for Contribution
- 🎨 UI/UX improvements
- 🤖 New AI features
- 📱 Mobile app development
- 🌐 Internationalization
- 📊 Advanced analytics
- 🔌 New platform integrations

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **TMDB API**: Movie and TV show metadata
- **OpenAI**: LLM capabilities
- **FastAPI**: Backend framework
- **React**: Frontend framework
- **Contributors**: All the amazing people who contribute to this project

## 📈 GitHub Achievements Roadmap

This project is designed to help achieve various GitHub badges:

- ✅ **Quickdraw**: First PR merged
- ✅ **Pull Shark**: Multiple PRs
- ✅ **Galaxy Brain**: Answered discussions
- ✅ **YOLO**: Merged without review
- ✅ **Public Sponsor**: Sponsor open source
- ⭐ **Starstruck**: Get stars on repository
- 🍴 **Forked**: Get repository forks

## 📞 Contact

- **GitHub**: [@rxl895](https://github.com/rxl895)
- **Project Link**: [https://github.com/rxl895/watchlist-manager](https://github.com/rxl895/watchlist-manager)

---

⭐ **Star this repository if you find it helpful!** ⭐