# Web Scraper for Visitor Classification - Frontend

This project is the frontend component of a web scraping and visitor classification system built with React, TypeScript, and Redux.

## Features

- URL input for website scraping
- Dynamic question generation based on website content
- User response collection
- Visitor classification based on responses
- Real-time feedback and error handling

## Tech Stack

- React 18
- TypeScript
- Redux Toolkit
- Styled Components
- Axios

## Project Structure
web-scraper-frontend/
├── src/
│ ├── components/
│ │ ├── common/
│ │ │ ├── ErrorMessage.tsx
│ │ │ └── LoadingSpinner.tsx
│ │ └── features/
│ │ ├── UrlInput.tsx
│ │ ├── QuestionDisplay.tsx
│ │ └── AnswerSection.tsx
│ ├── store/
│ │ ├── slices/
│ │ │ └── scraperSlice.ts
│ │ └── index.ts
│ ├── services/
│ │ └── api.ts
│ ├── styles/
│ │ └── GlobalStyles.ts
│ └── App.tsx

## Development Progress

### Completed
- ✅ Frontend project setup with React and TypeScript
- ✅ Redux store configuration
- ✅ Basic component structure
- ✅ API service layer

### In Progress
- 🔄 Backend development with Flask
- 🔄 AWS infrastructure setup
- 🔄 Integration testing

### TODO
- ⭕ Implement web scraping logic
- ⭕ Add AWS Comprehend integration
- ⭕ Enhance UI/UX design
- ⭕ Add user authentication
- ⭕ Implement caching mechanism
- ⭕ Add analytics dashboard
- ⭕ Write comprehensive tests

## Technical Implementation Details

### Frontend Architecture
The frontend is built with a focus on maintainability and scalability:
- **Component Structure**: Organized into feature-based and common components
- **State Management**: Centralized Redux store with async thunks for API calls
- **Type Safety**: Comprehensive TypeScript implementation
- **Styling**: Modular styled-components with global theming

### API Integration
- RESTful API communication using Axios
- Type-safe API responses
- Error handling and loading states
- Response caching (planned)

## Next Steps

The immediate focus is on developing the backend infrastructure and implementing the core web scraping functionality. This will be followed by AWS service integration and enhanced frontend features.

## License
This project is licensed under the MIT License.