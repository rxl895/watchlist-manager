#!/bin/bash

# Development Environment Checker
# Ensures all requirements are met for development

echo "🔍 Checking Development Environment"
echo "=================================="

errors=0

# Check Python
if command -v python3 &> /dev/null; then
    python_version=$(python3 --version | cut -d' ' -f2)
    echo "✅ Python $python_version"
    
    # Check Python version is 3.9+
    required_version="3.9"
    if [[ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" = "$required_version" ]]; then
        echo "✅ Python version is compatible"
    else
        echo "❌ Python 3.9+ required, found $python_version"
        errors=$((errors + 1))
    fi
else
    echo "❌ Python 3 not found"
    errors=$((errors + 1))
fi

# Check Node.js
if command -v node &> /dev/null; then
    node_version=$(node --version | sed 's/v//')
    echo "✅ Node.js $node_version"
    
    # Check Node version is 16+
    required_version="16.0.0"
    if [[ "$(printf '%s\n' "$required_version" "$node_version" | sort -V | head -n1)" = "$required_version" ]]; then
        echo "✅ Node.js version is compatible"
    else
        echo "❌ Node.js 16+ required, found $node_version"
        errors=$((errors + 1))
    fi
else
    echo "❌ Node.js not found"
    errors=$((errors + 1))
fi

# Check npm
if command -v npm &> /dev/null; then
    npm_version=$(npm --version)
    echo "✅ npm $npm_version"
else
    echo "❌ npm not found"
    errors=$((errors + 1))
fi

# Check Git
if command -v git &> /dev/null; then
    git_version=$(git --version | cut -d' ' -f3)
    echo "✅ Git $git_version"
else
    echo "❌ Git not found"
    errors=$((errors + 1))
fi

# Check Docker (optional)
if command -v docker &> /dev/null; then
    docker_version=$(docker --version | cut -d' ' -f3 | sed 's/,//')
    echo "✅ Docker $docker_version"
else
    echo "⚠️  Docker not found (optional for development)"
fi

# Check if in project directory
if [ -f "README.md" ] && [ -f "package.json" ]; then
    echo "✅ In correct project directory"
else
    echo "❌ Not in project root directory"
    errors=$((errors + 1))
fi

# Check environment files
if [ -f "backend/.env" ]; then
    echo "✅ Backend .env file exists"
else
    echo "⚠️  Backend .env file missing (copy from .env.example)"
fi

if [ -f "frontend/.env.local" ]; then
    echo "✅ Frontend .env.local file exists"
else
    echo "⚠️  Frontend .env.local file missing (copy from .env.example)"
fi

# Check virtual environment
if [ -d "backend/venv" ]; then
    echo "✅ Python virtual environment exists"
else
    echo "⚠️  Python virtual environment not found"
fi

# Check node_modules
if [ -d "frontend/node_modules" ]; then
    echo "✅ Frontend dependencies installed"
else
    echo "⚠️  Frontend dependencies not installed"
fi

echo ""
echo "=================================="

if [ $errors -eq 0 ]; then
    echo "🎉 Environment check passed! You're ready to develop."
    echo ""
    echo "Quick start commands:"
    echo "1. make install    # Install dependencies"
    echo "2. make start      # Start development servers"
else
    echo "❌ Environment check failed with $errors error(s)"
    echo "Please fix the issues above before continuing."
    exit 1
fi
