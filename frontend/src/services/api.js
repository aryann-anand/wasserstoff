import axios from 'axios';

const API_URL = 'https://wasserstoff-backend.onrender.com/api/v1';

const apiClient = axios.create({
  baseURL: API_URL,
  withCredentials: true,
});

export const makeGuess = async (guess, persona = 'serious') => {
  try {
    const response = await apiClient.post('/game/guess', { guess }, {
      headers: {
        'persona': persona
      }
    });
    return response.data;
  } catch (error) {
    console.error('Error making guess:', error);
    throw error;
  }
};

export const getHistory = async (limit = 5) => {
  try {
    const response = await apiClient.get(`/game/history?limit=${limit}`);
    return response.data;
  } catch (error) {
    console.error('Error getting history:', error);
    throw error;
  }
};

export const resetGame = async () => {
  try {
    const response = await apiClient.post('/game/reset');
    return response.data;
  } catch (error) {
    console.error('Error resetting game:', error);
    throw error;
  }
};
