# What Beats Rock?

A creative word association game where you think of items that beat the previous one. Starting with "Rock", can you create a chain of winning items?

## Live Demo

Play the game [here](https://wasserstoff-aryan.vercel.app/) .

```bash
https://wasserstoff-aryan.vercel.app/
```

## How to Play

Choose between "Serious" or "Cheery" host personalities for different game experiences.

1. The game starts with "Rock" as the first item
2. Think of something that would beat or overcome the current item
3. Type your guess and submit
4. If it's a valid answer (judged by AI), your score increases and your answer becomes the new item
5. If your answer is invalid or has been used before, the game ends
6. Try to achieve the highest score by creating a long chain of beating items!

## Method 1: Docker Setup

### Prerequisites

- Docker

### 1. Clone the repository

```bash
git clone https://github.com/aryann-anand/wasserstoff.git
```

### 2. Make sure the following Docker files are present:

```bash
wasserstoff/Dockerfile.backend
wasserstoff/Dockerfile.frontend
wasserstoff/docker-compose.yml
```

### 3. Run with Docker Compose

```bash
export GEMINI_API_KEY=your_api_key_here
docker-compose up --build
```

### 4. The webapp will be available at:

```bash
localhost
```

# ______________________________________________________________
## Method 2: Local Development Setup

### Prerequisites

- Node.js (v22)
- Python (3.12)
- MongoDB
- Redis
- Google Cloud account (for Gemini API access)

### Backend Setup

#### 1. Clone the repository:

```bash
git clone https://github.com/aryann-anand/wasserstoff.git
cd wasserstoff/backend
```

#### 2. Create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

#### 3. Install dependencies:

```bash
pip install fastapi uvicorn[standard] motor redis pydantic pydantic-settings python-dotenv google-generativeai better-profanity
```

#### 4. Create a .env file in the backend directory:

```bash
MONGODB_URL=mongodb://localhost:27017
MONGODB_DB_NAME=whatbeatsrock
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_PASSWORD=
GEMINI_API_KEY=your_gemini_api_key
GEMINI_MODEL=gemini-2.0-flash
```

#### 5. Run the backend server:

```bash
uvicorn app.main:app --reload
```

### The backend will be available at [http://localhost:8000](http://localhost:8000) .

### Frontend Setup

#### 1. Navigate to the frontend directory:
```bash
cd wasserstoff/backend
```

#### 2. Install dependencies:
```bash
npm install
```

#### 3. Start the development server:
```bash
npm start
```

### The frontend will be available at [http://localhost:3000](http://localhost:3000) .

# ______________________________________________________________

# Technical Architecture

## Backend

- **FastAPI**: Modern, high-performance web framework for building APIs
- **MongoDB**: Document database for storing game data and statistics
- **Redis**: In-memory data store for caching AI responses
- **Google Gemini AI**: AI model to judge if one item beats another
- **Better Profanity**: Filter for inappropriate content

## Frontend

- **React**: UI library for building the user interface
- **Axios**: HTTP client for API requests
- **React Confetti**: Visual effect for celebrating successful guesses

## Architecture

- **Session-based Gameplay**: Uses cookies to maintain game state across sessions
- **Linked List for Game History**: Efficiently stores and traverses game history
- **AI for Game Logic**: Uses AI to determine valid "beats" relationships
- **Caching Strategy**: Caches AI responses to reduce API calls and improve performance
- **Persona System**: Customizable game experience with different host personalities
- **Cross-Origin Communication**: Configured with proper CORS settings to enable frontend-backend communication across domains
- **Moderation System**: Prevents inappropriate content with automated filtering
- **Global Statistics**: Tracks how many times each answer has been used globally

# ______________________________________________________________

# Connect with me

### [Linkedin](https://www.linkedin.com/in/aryananand18)
### [Portfolio](https://hiaryan.vercel.app/)
### [GitHub](https://github.com/aryann-anand)