import React from 'react';
import { Provider } from 'react-redux';
import { store } from './store';
import styled from 'styled-components';
import UrlInput from './components/features/UrlInput';

const AppContainer = styled.div`
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
`;

function App() {
  return (
    <Provider store={store}>
      <AppContainer>
        <h1>Web Scraper for Visitor Classification</h1>
        <UrlInput />
      </AppContainer>
    </Provider>
  );
}

export default App;
