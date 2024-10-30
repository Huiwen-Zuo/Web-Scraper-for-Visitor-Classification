import React from 'react';
import { Provider } from 'react-redux';
import { store } from './store';
import styled from 'styled-components';
import UrlInput from './components/features/UrlInput';
import QuestionDisplay from './components/features/QuestionDisplay';
import AnswerSection from './components/features/AnswerSection';
import GlobalStyles from './styles/GlobalStyles';

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

const ContentSection = styled.section`
  background: white;
  border-radius: 8px;
  padding: 20px;
  margin-top: 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
`;

function App() {
  return (
    <Provider store={store}>
      <GlobalStyles />
      <AppContainer>
        <Title>Web Scraper for Visitor Classification</Title>
        <ContentSection>
          <UrlInput />
          <AnswerSection />
        </ContentSection>
      </AppContainer>
    </Provider>
  );
}

export default App;
