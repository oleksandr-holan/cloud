# FastAPI CRUD Application for Cloud Deployment

This README explains how our FastAPI application works, how to modify it, and how to set up your development environment for cloud services.

## Table of Contents

- [Application Overview](#application-overview)
- [How It Works](#how-it-works)
- [Setting Up Your Development Environment](#setting-up-your-development-environment)
- [Deploying to Heroku](#deploying-to-heroku)
- [Testing the API](#testing-the-api)

## Application Overview

This application is a RESTful API built with FastAPI that implements CRUD (Create, Read, Update, Delete) operations for managing items. It's designed to be deployed to Heroku, a cloud platform as a service.

## How It Works

### Deployment Configuration

- **requirements.txt**: Lists all dependencies
- **Procfile**: Tells Heroku how to run the application
- **.python-version**: Specifies the Python version

## Setting Up Your Development Environment

### Prerequisites

- Python 3.11+
- Git
- Heroku CLI

### Step 1: Install Python Dependencies

```bash
# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Set Up Local Development

```bash
# Run the application locally
uvicorn app.main:app --reload
```

### Step 3: Install Heroku CLI

```bash
# On macOS
brew install heroku/brew/heroku

# On Windows
# Download installer from: https://devcenter.heroku.com/articles/heroku-cli

# On Ubuntu
curl https://cli-assets.heroku.com/install.sh | sh
```

### Step 4: Configure Heroku

```bash
# Login to Heroku
heroku login

# Create a new Heroku app
heroku create your-app-name
```

## Deploying to Heroku

```bash
# Initialize Git repository (if not already done)
git init
git add .
git commit -m "Initial commit"

# Deploy to Heroku
git push heroku main

# Scale the app
heroku ps:scale web=1

# Open the app in browser
heroku open
```

```bash
# Destroy the app after you finish
heroku apps:destroy --app your-app-name --confirm your-app-name
```

## Testing the API

Once deployed, you can access the interactive API documentation:

- Swagger UI: `https://your-app-name.herokuapp.com/docs`
- ReDoc: `https://your-app-name.herokuapp.com/redoc`

### Example API Requests

#### Create an Item

```bash
curl -X POST "https://your-app-name.herokuapp.com/items/" \
     -H "Content-Type: application/json" \
     -d '{"name":"Test Item","description":"This is a test item","price":19.99}'
```

#### Get All Items

```bash
curl -X GET "https://your-app-name.herokuapp.com/items/"
```

#### Update an Item

```bash
curl -X PUT "https://your-app-name.herokuapp.com/items/item-uuid" \
     -H "Content-Type: application/json" \
     -d '{"name":"Updated Item","description":"This item was updated","price":29.99}'
```

#### Delete an Item

```bash
curl -X DELETE "https://your-app-name.herokuapp.com/items/item-uuid"
```
