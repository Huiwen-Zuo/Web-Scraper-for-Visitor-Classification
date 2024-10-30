import { createSlice, createAsyncThunk, PayloadAction } from '@reduxjs/toolkit';
import { apiService } from '../../services/api';

export interface Question {
  id: string;
  text: string;
  options: string[];
}

interface ScraperState {
  url: string;
  loading: boolean;
  questions: Question[];
  error: string | null;
  answers: Record<string, string>;
  classification: string | null;
  confidence: number | null;
}

const initialState: ScraperState = {
  url: '',
  loading: false,
  questions: [],
  error: null,
  answers: {},
  classification: null,
  confidence: null,
};

// Async thunks
export const scrapeWebsite = createAsyncThunk(
  'scraper/scrapeWebsite',
  async (url: string) => {
    const response = await apiService.scrapeWebsite(url);
    return response;
  }
);

export const submitAnswers = createAsyncThunk(
  'scraper/submitAnswers',
  async ({ url, answers }: { url: string; answers: Record<string, string> }) => {
    const response = await apiService.submitAnswers(url, answers);
    return response;
  }
);

const scraperSlice = createSlice({
  name: 'scraper',
  initialState,
  reducers: {
    setUrl: (state, action: PayloadAction<string>) => {
      state.url = action.payload;
    },
    setAnswer: (state, action: PayloadAction<{ questionId: string; answer: string }>) => {
      state.answers[action.payload.questionId] = action.payload.answer;
    },
    resetState: (state) => {
      Object.assign(state, initialState);
    },
  },
  extraReducers: (builder) => {
    builder
      // Scrape website cases
      .addCase(scrapeWebsite.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(scrapeWebsite.fulfilled, (state, action) => {
        state.loading = false;
        state.questions = action.payload.questions;
      })
      .addCase(scrapeWebsite.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message || 'Failed to scrape website';
      })
      // Submit answers cases
      .addCase(submitAnswers.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(submitAnswers.fulfilled, (state, action) => {
        state.loading = false;
        state.classification = action.payload.classification;
        state.confidence = action.payload.confidence;
      })
      .addCase(submitAnswers.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message || 'Failed to submit answers';
      });
  },
});

export const { setUrl, setAnswer, resetState } = scraperSlice.actions;
export default scraperSlice.reducer;