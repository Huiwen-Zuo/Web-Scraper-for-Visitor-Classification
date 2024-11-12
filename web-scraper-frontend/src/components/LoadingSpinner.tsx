import React from 'react';

export interface LoadingSpinnerProps {}

const LoadingSpinner: React.FC<LoadingSpinnerProps> = () => (
  <div className="loading-spinner">
    <div className="spinner"></div>
    <p>Analyzing website content...</p>
  </div>
);

export default LoadingSpinner; 