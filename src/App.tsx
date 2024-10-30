import React from 'react';
import { Provider } from 'react-redux';
import { store } from './store';
import styled from 'styled-components';
import UrlInput from './components/features/UrlInput';
import QuestionDisplay from './components/features/QuestionDisplay';

const AppContainer = styled.div`
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
`;

const Title = styled.h1`
  color: #333;
  text-align: center;
  margin-bottom: 30px;
`;

function App() {
  return (
    <Provider store={store}>
      <AppContainer>
        <Title>Web Scraper for Visitor Classification</Title>
        <UrlInput />
        <QuestionDisplay />
      </AppContainer>
    </Provider>
  );
}

export default App;
