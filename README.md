# Loyalty Program Roadmapping Service

This FastAPI service generates loyalty program roadmaps and implementation strategies using OpenAI's GPT-4 model.

## Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/fsilva7456/loyalty-roadmapping-service.git
   cd loyalty-roadmapping-service
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up your OpenAI API key:
   ```bash
   export OPENAI_API_KEY='your-api-key-here'
   ```

## Running the Service

1. Start the server:
   ```bash
   uvicorn main:app --reload
   ```

2. The service will be available at `http://localhost:8000`

## API Documentation

- API documentation is available at `http://localhost:8000/docs`
- OpenAPI specification is available at `http://localhost:8000/openapi.json`

### Generate Roadmap Endpoint

`POST /generate`

Example request:
```json
{
  "company_name": "Example Corp",
  "previous_data": {
    "customer_analysis": "Customer analysis details..."
  },
  "current_prompt_data": {
    "existing_generated_output": "Previous roadmap...",
    "user_feedback": "Focus more on technical implementation timeline"
  },
  "other_input_data": {}
}
```

## Key Features

- Uses OpenAI's GPT-4 model for roadmap generation
- Provides both narrative roadmap and structured phase data
- Integrates customer analysis context
- Supports iterative refinement through feedback
- Input validation using Pydantic
- Error handling and API monitoring

## Environment Variables

- `OPENAI_API_KEY`: Your OpenAI API key (required)
