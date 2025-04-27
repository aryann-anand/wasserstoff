import React, { useState, useEffect } from 'react';
import Confetti from 'react-confetti';
import './styles/App.css';
import { makeGuess, getHistory, resetGame } from './services/api';

function App() {
  const [gameState, setGameState] = useState({
    score: 0,
    lastGuess: '',
    previousItem: 'Rock',
    globalCount: 0,
    gameOver: false,
    success: false,
    message: 'Start by guessing what beats Rock!'
  });
  
  const [history, setHistory] = useState([]);
  const [persona, setPersona] = useState('serious');
  const [showConfetti, setShowConfetti] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [guess, setGuess] = useState('');
  const [showFullHistory, setShowFullHistory] = useState(false);
  const [fullHistory, setFullHistory] = useState([]);

  // Fetch history on component mount
  useEffect(() => {
    fetchHistory();
  }, []);

  // Fetch full history when showFullHistory changes
  useEffect(() => {
    if (showFullHistory) {
      fetchFullHistory();
    }
  }, [showFullHistory]);

  const fetchHistory = async () => {
    try {
      const response = await getHistory();
      setHistory(response.guesses || []);
    } catch (err) {
      setError('Failed to load game history');
      console.error(err);
    }
  };

  const fetchFullHistory = async () => {
    try {
      const response = await getHistory(100); // Get up to 100 entries
      setFullHistory(response.guesses || []);
    } catch (err) {
      setError('Failed to load complete game history');
      console.error(err);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!guess.trim()) return;
    
    setLoading(true);
    setError(null);
    
    try {
      const response = await makeGuess(guess, persona);
      setGameState({
        score: response.score,
        lastGuess: response.last_guess,
        previousItem: response.previous_item,
        globalCount: response.global_count,
        gameOver: response.game_over,
        success: response.success,
        message: response.message
      });
      
      // Show confetti on successful guess
      if (response.success) {
        setShowConfetti(true);
        setTimeout(() => setShowConfetti(false), 3000);
      }
      
      // Update history
      fetchHistory();
      setGuess('');
    } catch (err) {
      setError('Failed to process your guess. Please try again.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleReset = async () => {
    setLoading(true);
    setError(null);
    
    try {
      await resetGame();
      setGameState({
        score: 0,
        lastGuess: '',
        previousItem: 'Rock',
        globalCount: 0,
        gameOver: false,
        success: false,
        message: 'Game reset! Start by guessing what beats Rock!'
      });
      
      // Update history
      fetchHistory();
      // Reset full history view
      setShowFullHistory(false);
    } catch (err) {
      setError('Failed to reset the game. Please try again.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App">
      {showConfetti && <Confetti recycle={false} />}
      
      <header className="App-header">
        <h1>What Beats Rock?</h1>
        
        <div className="persona-selector">
          <label>Host Personality:</label>
          <select value={persona} onChange={(e) => setPersona(e.target.value)}>
            <option value="serious">Serious</option>
            <option value="cheery">Cheery</option>
          </select>
        </div>
      </header>
      
      <main className="App-main">
        <div className="game-message">
          <p>{gameState.message}</p>
          {error && <p className="error-message">{error}</p>}
        </div>
        
        <div className="game-status">
          <h2>Game Status</h2>
          <p className="score">Score: {gameState.score}</p>
          
          {gameState.lastGuess && (
            <div className="last-guess">
              <p>Last Guess: <strong>{gameState.lastGuess}</strong></p>
              <p>Previous Item: <strong>{gameState.previousItem}</strong></p>
              {gameState.globalCount > 0 && (
                <p>This answer has been guessed <strong>{gameState.globalCount}</strong> times globally!</p>
              )}
            </div>
          )}
          
          {gameState.gameOver && (
            <div className="game-over">
              <h3>Game Over!</h3>
              <p>Your final score: {gameState.score}</p>
            </div>
          )}
        </div>
        
        <form onSubmit={handleSubmit} className="guess-form">
          <input
            type="text"
            value={guess}
            onChange={(e) => setGuess(e.target.value)}
            placeholder="What beats the current item?"
            disabled={loading || gameState.gameOver}
            className="guess-input"
          />
          <button 
            type="submit" 
            disabled={loading || gameState.gameOver || !guess.trim()} 
            className="guess-button"
          >
            Submit
          </button>
        </form>
        
        {gameState.gameOver ? (
          <button 
            className="reset-button"
            onClick={handleReset}
            disabled={loading}
          >
            Play Again
          </button>
        ) : (
          <button 
            className="history-button"
            onClick={() => setShowFullHistory(!showFullHistory)}
            disabled={loading}
          >
            {showFullHistory ? "Hide Full History" : "Show Full History"}
          </button>
        )}
        
        <div className="history-list">
          <h3>Last 5 Guesses</h3>
          {history.length > 0 ? (
            <ul>
              {history.map((item, index) => (
                <li key={index}>{item}</li>
              ))}
            </ul>
          ) : (
            <p>No guesses yet!</p>
          )}
        </div>
        
        {showFullHistory && (
          <div className="full-history-list">
            <h3>Complete Guess History</h3>
            {fullHistory.length > 0 ? (
              <ul>
                {fullHistory.map((item, index) => (
                  <li key={index}>{item}</li>
                ))}
              </ul>
            ) : (
              <p>No guesses yet!</p>
            )}
          </div>
        )}
      </main>
      
      <footer className="App-footer">
        <div className="social-links">
          <a href="https://hiaryan.vercel.app" target="_blank" rel="noopener noreferrer" title="Portfolio">
            <i className="fas fa-globe"></i>
          </a>
          <a href="https://github.com/aryann-anand" target="_blank" rel="noopener noreferrer" title="GitHub">
            <i className="fab fa-github"></i>
          </a>
          <a href="https://www.linkedin.com/in/aryananand18" target="_blank" rel="noopener noreferrer" title="LinkedIn">
            <i className="fab fa-linkedin"></i>
          </a>
        </div>
        <p className="copyright">© Aryan Anand 2025</p>
      </footer>
    </div>
  );
}

export default App;
