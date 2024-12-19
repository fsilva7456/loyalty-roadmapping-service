# Loyalty Program Roadmapping Service

This FastAPI service generates implementation roadmaps for loyalty programs using OpenAI's GPT-4 model.

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
   export OPENAI_API_KEY='your-api-key-here'  # On Windows: set OPENAI_API_KEY=your-api-key-here
   ```

## Running the Service

1. Start the server:
   ```bash
   uvicorn main:app --reload
   ```

2. The service will be available at `http://localhost:8000`

## API Documentation

### Generate Roadmap Endpoint

`POST /generate`

Generates a detailed implementation roadmap for a loyalty program.

Request format:
```json
{
  "company_name": "string",
  "previous_data": {
    "loyalty_program_design": "string (if available)",
    "financial_model": "string (if available)"
  },
  "current_prompt_data": {
    "existing_generated_output": "string",
    "user_feedback": "string"
  },
  "other_input_data": {}
}
```

Response format:
```json
{
  "generated_output": "Detailed narrative roadmap...",
  "structured_data": {
    "roadmap": {
      "phases": [
        {
          "name": "Phase Name",
          "duration": "X weeks/months",
          "start_date": "Q1 2025",
          "key_milestones": ["milestone1", "milestone2"],
          "deliverables": ["deliverable1", "deliverable2"],
          "resource_requirements": ["requirement1", "requirement2"],
          "dependencies": ["dependency1", "dependency2"],
          "risks": ["risk1", "risk2"]
        }
      ],
      "total_duration": "X months",
      "critical_dependencies": ["dependency1", "dependency2"],
      "key_risks": ["risk1", "risk2"]
    }
  }
}
```

## Key Features

- Generates detailed implementation roadmaps using GPT-4
- Incorporates existing program design and financial models
- Supports iterative refinement through feedback
- Provides both narrative and structured outputs
- Includes comprehensive phase details:
  - Timelines and durations
  - Key milestones and deliverables
  - Resource requirements
  - Dependencies and risks

## Environment Variables

- `OPENAI_API_KEY`: Your OpenAI API key (required)

## Interactive API Documentation

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`
- OpenAPI JSON: `http://localhost:8000/openapi.json`