import { createSlice, PayloadAction } from '@reduxjs/toolkit';

interface ScraperState {
  url: string;
  loading: boolean;
  questions: Question[];
  error: string | null;
}

interface Question {
  id: string;
  text: string;
  options: string[];
}

const initialState: ScraperState = {
  url: '',
  loading: false,
  questions: [],
  error: null,
};

const scraperSlice = createSlice({
  name: 'scraper',
  initialState,
  reducers: {
    setUrl: (state, action: PayloadAction<string>) => {
      state.url = action.payload;
    },
    setLoading: (state, action: PayloadAction<boolean>) => {
      state.loading = action.payload;
    },
    setQuestions: (state, action: PayloadAction<Question[]>) => {
      state.questions = action.payload;
    },
    setError: (state, action: PayloadAction<string | null>) => {
      state.error = action.payload;
    },
  },
});

export const { setUrl, setLoading, setQuestions, setError } = scraperSlice.actions;
export default scraperSlice.reducer;

// Also export the Question interface if needed elsewhere
export type { Question }; 