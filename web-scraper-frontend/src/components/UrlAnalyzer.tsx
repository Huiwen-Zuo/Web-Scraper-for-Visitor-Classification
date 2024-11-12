import React, { useState } from 'react';
import axios from 'axios';
import LoadingSpinner from './LoadingSpinner';
import { AnalyzerResponse, ApiError } from '../types';

const UrlAnalyzer: React.FC = () => {
  const [url, setUrl] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<AnalyzerResponse | null>(null);
  const [error, setError] = useState<string>('');
  const [selectedOption, setSelectedOption] = useState<string>('');

  const API_URL = process.env.REACT_APP_API_URL || 'YOUR_API_GATEWAY_URL/analyze';

  const validateUrl = (url: string): boolean => {
    try {
      new URL(url);
      return true;
    } catch {
      return false;
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!validateUrl(url)) {
      setError('Please enter a valid URL');
      return;
    }

    setLoading(true);
    setError('');
    setResult(null);
    setSelectedOption('');

    try {
      const response = await axios.post(API_URL, { url });
      const data = JSON.parse(response.data.body);
      
      if (data.error) {
        throw new Error(data.error);
      }
      
      setResult(data);
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to analyze URL';
      setError(errorMessage);
      console.error('Error:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleOptionSelect = (option: string) => {
    setSelectedOption(option);
    // Here you could add analytics or store the user's selection
  };

  return (
    <div className="url-analyzer">
      <form onSubmit={handleSubmit} className="analyzer-form">
        <div className="input-group">
          <input
            type="url"
            value={url}
            onChange={(e) => setUrl(e.target.value)}
            placeholder="Enter website URL (e.g., https://www.example.com)"
            required
            className="url-input"
            disabled={loading}
          />
          <button type="submit" disabled={loading} className="submit-button">
            {loading ? 'Analyzing...' : 'Analyze'}
          </button>
        </div>
      </form>

      {error && (
        <div className="error-message" role="alert">
          {error}
        </div>
      )}
      
      {loading && <LoadingSpinner />}
      
      {result && (
        <div className="result-container">
          <h2 className="website-title">{result.title}</h2>
          <h3 className="question">{result.question}</h3>
          <div className="options-grid">
            {result.options.map((option, index) => (
              <button
                key={index}
                onClick={() => handleOptionSelect(option)}
                className={`option-button ${selectedOption === option ? 'selected' : ''}`}
              >
                {option}
              </button>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default UrlAnalyzer; 