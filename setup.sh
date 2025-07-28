#!/bin/bash

# Watchlist Manager Setup Script
# This script helps you get started with the project quickly

echo "🎬 Welcome to Watchlist Manager Setup!"
echo "======================================"

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed."
    echo "Please install Python 3.9 or higher and try again."
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is required but not installed."
    echo "Please install Node.js 16+ and try again."
    exit 1
fi

echo "✅ Python and Node.js are installed"

# Setup backend
echo ""
echo "🔧 Setting up backend..."
cd backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Copy environment file
if [ ! -f .env ]; then
    cp .env.example .env
    echo "📝 Created .env file from template. Please edit it with your API keys."
fi

# Initialize database
python -c "from app.database import init_db; init_db()"
echo "✅ Backend setup complete"

# Setup frontend
echo ""
echo "🔧 Setting up frontend..."
cd ../frontend

# Install dependencies
npm install

# Copy environment file
if [ ! -f .env.local ]; then
    cp .env.example .env.local
    echo "📝 Created .env.local file from template. Please edit it with your configuration."
fi

echo "✅ Frontend setup complete"

echo ""
echo "🎉 Setup complete! Next steps:"
echo ""
echo "1. Edit backend/.env with your API keys (TMDB, OpenAI, etc.)"
echo "2. Edit frontend/.env.local with your configuration"
echo ""
echo "To start the development servers:"
echo ""
echo "Backend (Terminal 1):"
echo "cd backend && source venv/bin/activate && uvicorn main:app --reload"
echo ""
echo "Frontend (Terminal 2):"
echo "cd frontend && npm start"
echo ""
echo "Then visit http://localhost:3000 to see your watchlist manager!"
echo ""
echo "📚 Check out the README.md for more detailed instructions."
