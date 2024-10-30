import React, { useState } from 'react';
import { useDispatch } from 'react-redux';
import styled from 'styled-components';
import { scrapeWebsite } from '../../store/slices/scraperSlice';
import { AppDispatch } from '../../store';

const InputContainer = styled.div`
  margin: 20px 0;
`;

const Input = styled.input`
  width: 70%;
  padding: 10px;
  margin-right: 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
`;

const Button = styled.button`
  padding: 10px 20px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;

  &:hover {
    background-color: #0056b3;
  }
`;

const UrlInput: React.FC = () => {
  const [inputUrl, setInputUrl] = useState('');
  const dispatch = useDispatch<AppDispatch>();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (inputUrl) {
      try {
        await dispatch(scrapeWebsite(inputUrl)).unwrap();
      } catch (error) {
        console.error('Failed to scrape website:', error);
      }
    }
  };

  return (
    <InputContainer>
      <form onSubmit={handleSubmit}>
        <Input
          type="url"
          value={inputUrl}
          onChange={(e) => setInputUrl(e.target.value)}
          placeholder="Enter website URL..."
          required
        />
        <Button type="submit">Analyze</Button>
      </form>
    </InputContainer>
  );
};

export default UrlInput; 