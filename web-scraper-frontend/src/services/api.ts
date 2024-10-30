import axios from 'axios';
import { Question } from '../store/slices/scraperSlice';

const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || 'http://localhost:5000';

interface ScrapeResponse {
  questions: Question[];
}

interface ClassificationResponse {
  classification: string;
  confidence: number;
}

export const api = {
  scrapeWebsite: async (url: string): Promise<ScrapeResponse> => {
    try {
      const response = await axios.post(`${API_BASE_URL}/scrape`, { url });
      return response.data;
    } catch (error) {
      if (axios.isAxiosError(error) && error.response) {
        throw new Error(error.response.data.error || 'Failed to scrape website');
      }
      throw new Error('Failed to connect to the server');
    }
  },

  submitAnswers: async (
    url: string, 
    answers: Record<string, string>
  ): Promise<ClassificationResponse> => {
    try {
      const response = await axios.post(`${API_BASE_URL}/classify`, { 
        url, 
        answers 
      });
      return response.data;
    } catch (error) {
      if (axios.isAxiosError(error) && error.response) {
        throw new Error(error.response.data.error || 'Failed to submit answers');
      }
      throw new Error('Failed to connect to the server');
    }
  }
}; 