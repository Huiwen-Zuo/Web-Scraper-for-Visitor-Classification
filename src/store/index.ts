import { configureStore } from '@reduxjs/toolkit';
import scraperReducer from './slices/scraperSlice';

export const store = configureStore({
  reducer: {
    scraper: scraperReducer,
  },
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;