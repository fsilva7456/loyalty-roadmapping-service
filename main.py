import os
from typing import Dict, List, Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from openai import OpenAI
import json

app = FastAPI(title="Loyalty Program Roadmapping Service")

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class RoadmapPhase(BaseModel):
    name: str
    timeline: str
    key_objectives: List[str]
    technical_requirements: List[str]
    estimated_effort: str
    dependencies: List[str]

class PreviousData(BaseModel):
    customer_analysis: Optional[str] = None

class CurrentPromptData(BaseModel):
    existing_generated_output: str
    user_feedback: str

class RoadmapRequest(BaseModel):
    company_name: str
    previous_data: Optional[PreviousData] = None
    current_prompt_data: Optional[CurrentPromptData] = None
    other_input_data: Optional[Dict] = {}

class RoadmapResponse(BaseModel):
    generated_output: str
    structured_data: Dict

def construct_system_prompt() -> str:
    return """
You are an expert in loyalty program implementation and technical roadmapping. 
Create a detailed roadmap for implementing a loyalty program, including technical requirements and timelines.

Consider:
1. Technical infrastructure needs
2. Integration requirements
3. Implementation phases and dependencies
4. Resource requirements and timeline
5. Customer analysis context (if provided)

Provide your response in two parts:
1. A detailed roadmap in natural language
2. A structured JSON object containing implementation phases

Separate the two parts with [JSON_START] and [JSON_END] markers.
"""

def generate_roadmap(company_name: str, customer_analysis: Optional[str] = None) -> tuple[str, dict]:
    """Generate implementation roadmap using OpenAI's API"""
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": construct_system_prompt()},
                {"role": "user", "content": f"Create roadmap for {company_name}"}
            ],
            temperature=0.7,
            max_tokens=2000
        )
        
        full_response = response.choices[0].message.content
        roadmap = full_response[:full_response.find("[JSON_START]")].strip()
        structured_data = extract_json_from_text(full_response)
        
        return roadmap, structured_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate", response_model=RoadmapResponse)
async def generate_analysis(request: RoadmapRequest):
    customer_analysis = request.previous_data.customer_analysis if request.previous_data else None
    generated_text, structured_data = generate_roadmap(request.company_name, customer_analysis)
    return RoadmapResponse(generated_output=generated_text, structured_data=structured_data)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)