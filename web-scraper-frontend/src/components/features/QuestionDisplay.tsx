import React from 'react';
import { useSelector } from 'react-redux';
import styled from 'styled-components';
import { RootState } from '../../store';
import { Question } from '../../store/slices/scraperSlice';

const QuestionContainer = styled.div`
  margin: 20px 0;
`;

const QuestionCard = styled.div`
  background: white;
  border-radius: 8px;
  padding: 20px;
  margin-bottom: 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
`;

const OptionsList = styled.div`
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-top: 10px;
`;

const OptionButton = styled.button`
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  background: white;
  cursor: pointer;
  text-align: left;
  
  &:hover {
    background: #f5f5f5;
  }
`;

const QuestionDisplay: React.FC = () => {
  const questions = useSelector((state: RootState) => state.scraper.questions);
  const loading = useSelector((state: RootState) => state.scraper.loading);
  const error = useSelector((state: RootState) => state.scraper.error);

  if (loading) {
    return <div>Loading questions...</div>;
  }

  if (error) {
    return <div>Error: {error}</div>;
  }

  return (
    <QuestionContainer>
      {questions.map((question: Question) => (
        <QuestionCard key={question.id}>
          <h3>{question.text}</h3>
          <OptionsList>
            {question.options.map((option, index) => (
              <OptionButton key={index} onClick={() => console.log(option)}>
                {option}
              </OptionButton>
            ))}
          </OptionsList>
        </QuestionCard>
      ))}
    </QuestionContainer>
  );
};

export default QuestionDisplay; 