# Visualization Generator with Gemini AI

This project uses FastAPI for the backend and React with TypeScript for the frontend to generate matplotlib visualizations using Google's Gemini AI.

## Project Structure 
project/
├── backend/
│ ├── agent/
│ │ └── code_generator_agent.py
│ └── requirements.txt
├── frontend/
│ ├── src/
│ │ ├── components/
│ │ ├── services/
│ │ └── types/
│ ├── package.json
│ └── tsconfig.json
└── README.md

## Backend Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)
- Google Gemini API key (get it from [Google AI Studio](https://makersuite.google.com/app/apikey))

### Installation

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment:
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the backend directory:
```env
GOOGLE_API_KEY=your-api-key-here
```

### Running the Backend

1. Make sure your virtual environment is activated
2. Start the FastAPI server:
```bash
# From the backend directory
uvicorn agent.code_generator_agent:app --reload
```

The backend will be available at `http://localhost:8000`

## Frontend Setup

### Prerequisites
- Node.js 14 or higher
- npm (Node package manager)

### Installation

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

### Running the Frontend

1. Start the development server:
```bash
npm start
```

The frontend will be available at `http://localhost:3000`

## API Endpoints

### Generate Visualization Code
- **Endpoint**: `POST /agent/code`
- **Request Body**:
```json
{
    "prompt": "string"
}
```
- **Response**:
```json
{
    "generated_code": "string",
    "image_base64": "string",
    "logs": "string"
}
```

## Usage

1. Start both the backend and frontend servers
2. Open your browser to `http://localhost:3000`
3. Enter a prompt describing the visualization you want (e.g., "Create a bar chart showing monthly sales data")
4. Click "Generate" to create the visualization

## Dependencies

### Backend
- fastapi
- uvicorn
- python-dotenv
- google-generativeai
- matplotlib
- numpy
- pydantic

### Frontend
- react
- typescript
- tailwindcss
- @types/react
- @types/react-dom

## Troubleshooting

### Common Issues

1. **Backend API Key Error**
   - Make sure your `.env` file exists in the backend directory
   - Verify the GOOGLE_API_KEY is correctly set
   - Restart the backend server after updating the .env file

2. **CORS Issues**
   - Verify the backend is running on http://localhost:8000
   - Check that the frontend is making requests to the correct URL

3. **Module Not Found Errors**
   - Make sure you're in the correct directory
   - Verify all dependencies are installed
   - Check that your virtual environment is activated (backend)

### Getting Help

If you encounter any issues:
1. Check the backend logs for error messages
2. Verify all environment variables are set correctly
3. Ensure all dependencies are installed
4. Check that both servers are running on the correct ports

## Development

### Backend Development
- The main FastAPI application is in `backend/agent/code_generator_agent.py`
- Add new endpoints in this file
- Use `print` statements for debugging (visible in the terminal running uvicorn)

### Frontend Development
- React components are in `frontend/src/components`
- API services are in `frontend/src/services`
- TypeScript types are in `frontend/src/types`

## License

[Your chosen license] 