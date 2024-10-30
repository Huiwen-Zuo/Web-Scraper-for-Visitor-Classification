import React from 'react';
import { useDispatch, useSelector } from 'react-redux';
import styled from 'styled-components';
import { RootState, AppDispatch } from '../../store';
import { setAnswer, submitAnswers } from '../../store/slices/scraperSlice';
import LoadingSpinner from '../common/LoadingSpinner';
import ErrorMessage from '../common/ErrorMessage';

const AnswerContainer = styled.div`
  margin: 20px 0;
`;

const ResultCard = styled.div`
  background: #f8f9fa;
  border-radius: 8px;
  padding: 20px;
  margin-top: 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
`;

const SubmitButton = styled.button`
  background: #28a745;
  color: white;
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  margin-top: 20px;

  &:hover {
    background: #218838;
  }

  &:disabled {
    background: #6c757d;
    cursor: not-allowed;
  }
`;

const AnswerSection: React.FC = () => {
  const dispatch = useDispatch<AppDispatch>();
  const {
    questions,
    answers,
    loading,
    error,
    url,
    classification,
    confidence
  } = useSelector((state: RootState) => state.scraper);

  const handleSubmit = async () => {
    if (Object.keys(answers).length === questions.length) {
      try {
        await dispatch(submitAnswers({ url, answers })).unwrap();
      } catch (error) {
        console.error('Failed to submit answers:', error);
      }
    }
  };

  if (loading) {
    return <LoadingSpinner />;
  }

  if (error) {
    return <ErrorMessage message={error} />;
  }

  return (
    <AnswerContainer>
      {questions.map((question) => (
        <div key={question.id}>
          <h3>{question.text}</h3>
          {question.options.map((option, index) => (
            <label key={index} style={{ display: 'block', margin: '10px 0' }}>
              <input
                type="radio"
                name={question.id}
                value={option}
                checked={answers[question.id] === option}
                onChange={() => dispatch(setAnswer({ questionId: question.id, answer: option }))}
              />
              {' '}{option}
            </label>
          ))}
        </div>
      ))}

      {questions.length > 0 && (
        <SubmitButton
          onClick={handleSubmit}
          disabled={Object.keys(answers).length !== questions.length}
        >
          Submit Answers
        </SubmitButton>
      )}

      {classification && (
        <ResultCard>
          <h3>Classification Result</h3>
          <p>Category: {classification}</p>
          <p>Confidence: {(confidence || 0) * 100}%</p>
        </ResultCard>
      )}
    </AnswerContainer>
  );
};

export default AnswerSection; 