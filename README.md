# Web Scraper for Visitor Classification

A full-stack web application that analyzes websites and generates dynamic visitor classification questionnaires using modern web technologies and AWS services.

## Project Overview

This application enables dynamic visitor profiling by:
- Analyzing website content through web scraping
- Generating relevant questions based on content analysis
- Classifying visitors based on their responses
- Providing insights about visitor interests and demographics

## Tech Stack

### Frontend (`/web-scraper-frontend`)
- **Core**: React 18, TypeScript
- **State Management**: Redux Toolkit
- **Styling**: Styled Components
- **API Communication**: Axios

### Backend (`/web-scraper-backend`)
- **Core**: Python, Flask
- **Web Scraping**: BeautifulSoup4
- **Data Validation**: Marshmallow
- **Cloud Services**: AWS (Comprehend, DynamoDB)

## Features

- **URL Analysis**: Extract meaningful content from any website
- **Dynamic Question Generation**: Create relevant questions based on website content
- **Visitor Classification**: Analyze responses to classify visitors
- **Real-time Processing**: Immediate feedback and classification results
- **Error Handling**: Robust error management for both frontend and backend

## Development Progress

### Completed
- ✅ Frontend project setup with React and TypeScript
- ✅ Redux store configuration
- ✅ Basic component structure
- ✅ Backend structure with Flask
- ✅ API service layer setup

### In Progress
- 🔄 Web scraping implementation
- 🔄 Question generation logic
- 🔄 Visitor classification algorithm

### Planned
- ⭕ AWS services integration
- ⭕ Enhanced error handling
- ⭕ UI/UX improvements
- ⭕ Performance optimization
- ⭕ Testing suite
- ⭕ Analytics dashboard

## Architecture

The application follows a microservices architecture:
- Frontend communicates with backend via RESTful APIs
- Backend processes requests and interacts with AWS services
- Data flow is managed through Redux on the frontend
- Modular component structure for scalability

## Next Steps

1. Implement core web scraping functionality
2. Develop question generation algorithm
3. Integrate AWS Comprehend for text analysis
4. Add comprehensive testing
5. Enhance UI/UX design
6. Implement caching and performance optimizations

## License

This project is licensed under the MIT License.