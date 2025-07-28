# Watchlist Manager - Contributing Guidelines

Thank you for your interest in contributing to the Watchlist Manager! This document provides guidelines and information for contributors.

## 🤝 How to Contribute

### 1. Fork and Clone
```bash
git clone https://github.com/YOUR_USERNAME/watchlist-manager.git
cd watchlist-manager
```

### 2. Set up Development Environment
```bash
# Backend
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Frontend
cd ../frontend
npm install
```

### 3. Create a Branch
```bash
git checkout -b feature/your-feature-name
```

### 4. Make Changes
- Write clear, documented code
- Add tests for new features
- Update documentation as needed

### 5. Test Your Changes
```bash
# Backend tests
cd backend
pytest tests/ -v

# Frontend tests
cd frontend
npm test
```

### 6. Submit a Pull Request
- Write a clear PR description
- Reference any related issues
- Ensure all tests pass

## 🎯 Areas for Contribution

### High Priority
- 🤖 LLM integration improvements
- 📊 Advanced analytics features
- 🎨 UI/UX enhancements
- 📱 Mobile responsiveness

### Medium Priority
- 🌐 Internationalization (i18n)
- 🔌 New streaming platform integrations
- 📈 Performance optimizations
- 🔒 Security enhancements

### Good First Issues
- 📝 Documentation improvements
- 🐛 Bug fixes
- ✨ Small feature additions
- 🧪 Test coverage improvements

## 📋 Code Style Guidelines

### Python (Backend)
- Follow PEP 8
- Use type hints
- Write docstrings for functions and classes
- Use Black for formatting
- Use isort for import sorting

### JavaScript/TypeScript (Frontend)
- Use ESLint and Prettier
- Follow Airbnb style guide
- Use TypeScript when possible
- Write JSDoc comments

### Git Commit Messages
```
type(scope): description

feat(api): add recommendation endpoint
fix(ui): resolve mobile layout issue
docs(readme): update installation instructions
test(api): add unit tests for auth service
```

## 🏗️ Development Setup

### Environment Variables
Create `.env` files:

**Backend (.env)**
```
DATABASE_URL=sqlite:///./watchlist.db
SECRET_KEY=dev-secret-key
OPENAI_API_KEY=your-openai-key
TMDB_API_KEY=your-tmdb-key
```

**Frontend (.env.local)**
```
REACT_APP_API_URL=http://localhost:8000
REACT_APP_TMDB_API_KEY=your-tmdb-key
```

### Running Tests
```bash
# Backend
cd backend
pytest tests/ -v --cov=app --cov-report=html

# Frontend
cd frontend
npm test -- --coverage
```

## 🐛 Reporting Issues

When reporting issues, please include:
- Clear description of the problem
- Steps to reproduce
- Expected vs actual behavior
- Screenshots (if applicable)
- Environment details (OS, browser, versions)

## 💡 Suggesting Features

For feature requests:
- Check existing issues first
- Provide clear use case
- Explain the problem it solves
- Consider implementation complexity

## 📚 Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Documentation](https://reactjs.org/docs/)
- [TMDB API Documentation](https://developers.themoviedb.org/3)
- [OpenAI API Documentation](https://platform.openai.com/docs)

## ⚖️ License

By contributing, you agree that your contributions will be licensed under the MIT License.
