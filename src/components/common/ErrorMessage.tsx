import React from 'react';
import styled from 'styled-components';

const ErrorContainer = styled.div`
  background-color: #fff3f3;
  border: 1px solid #ffcdd2;
  border-radius: 4px;
  padding: 15px;
  margin: 10px 0;
  color: #d32f2f;
`;

interface ErrorMessageProps {
  message: string;
}

const ErrorMessage: React.FC<ErrorMessageProps> = ({ message }) => (
  <ErrorContainer>
    <p>{message}</p>
  </ErrorContainer>
);

export default ErrorMessage; 