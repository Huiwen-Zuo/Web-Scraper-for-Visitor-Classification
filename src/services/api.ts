import axios, { AxiosResponse } from 'axios';
import { Question } from '../store/slices/scraperSlice';

const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || 'http://localhost:5000';

export const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Response types
interface ScrapeResponse {
  questions: Question[];
  websiteInfo?: {
    title: string;
    description: string;
  };
}

interface SubmitAnswersResponse {
  classification: string;
  confidence: number;
}

// API methods
export const apiService = {
  // Scrape website and get questions
  scrapeWebsite: async (url: string): Promise<ScrapeResponse> => {
    try {
      const response: AxiosResponse<ScrapeResponse> = await api.post('/scrape', { url });
      return response.data;
    } catch (error) {
      throw new Error(error instanceof Error ? error.message : 'Failed to scrape website');
    }
  },

  // Submit user's answers and get classification
  submitAnswers: async (
    url: string,
    answers: Record<string, string>
  ): Promise<SubmitAnswersResponse> => {
    try {
      const response: AxiosResponse<SubmitAnswersResponse> = await api.post('/classify', {
        url,
        answers,
      });
      return response.data;
    } catch (error) {
      throw new Error(error instanceof Error ? error.message : 'Failed to submit answers');
    }
  },
};

// If there are no other exports, you can add:
export {};