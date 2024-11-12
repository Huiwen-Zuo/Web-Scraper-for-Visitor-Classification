export interface AnalyzerResponse {
  title: string;
  question: string;
  options: string[];
}

export interface ApiError {
  message: string;
  code?: string;
}

export type { LoadingSpinnerProps } from '../components/LoadingSpinner'; 