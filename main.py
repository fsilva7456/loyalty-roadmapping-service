import os
from typing import Dict, List, Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from openai import OpenAI
import json

app = FastAPI(title="Loyalty Program Roadmapping Service")

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class PreviousData(BaseModel):
    loyalty_program_design: Optional[str] = None
    financial_model: Optional[str] = None

class CurrentPromptData(BaseModel):
    existing_generated_output: str
    user_feedback: str

class RoadmapRequest(BaseModel):
    company_name: str
    previous_data: Optional[PreviousData] = None
    current_prompt_data: Optional[CurrentPromptData] = None
    other_input_data: Optional[Dict] = {}

class RoadmapPhase(BaseModel):
    name: str
    duration: str
    start_date: str
    key_milestones: List[str]
    deliverables: List[str]
    resource_requirements: List[str]
    dependencies: List[str]
    risks: List[str]

class RoadmapData(BaseModel):
    phases: List[RoadmapPhase]
    total_duration: str
    critical_dependencies: List[str]
    key_risks: List[str]

class RoadmapResponse(BaseModel):
    generated_output: str
    structured_data: Dict

def construct_system_prompt() -> str:
    return """
You are an expert in loyalty program implementation and project management.
Create a detailed implementation roadmap for a loyalty program, focusing on practical execution.

Consider:
1. Implementation phases and timelines
2. Technical and business milestones
3. Resource requirements and dependencies
4. Risk management and mitigation strategies
5. Previous program design and financial models (if provided)

Provide your response in two parts:
1. A detailed roadmap narrative including:
   - Executive summary
   - Phase-by-phase breakdown
   - Risk management approach
   - Key success factors

2. A structured JSON object with this schema:
{
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

Separate the two parts with [JSON_START] and [JSON_END] markers.
"""

def construct_user_prompt(
    company_name: str,
    loyalty_program_design: Optional[str] = None,
    financial_model: Optional[str] = None,
    existing_output: Optional[str] = None,
    feedback: Optional[str] = None
) -> str:
    prompt = f"Create an implementation roadmap for {company_name}'s loyalty program."
    
    if loyalty_program_design:
        prompt += f"\n\nProgram Design:\n{loyalty_program_design}"
    
    if financial_model:
        prompt += f"\n\nFinancial Model:\n{financial_model}"
    
    if existing_output and feedback:
        prompt += f"""
\n\nPrevious Roadmap:\n{existing_output}
\nPlease refine based on this feedback:\n{feedback}
"""
    
    return prompt

def extract_json_from_text(text: str) -> dict:
    try:
        start_marker = "[JSON_START]"
        end_marker = "[JSON_END]"
        json_str = text[text.find(start_marker) + len(start_marker):text.find(end_marker)].strip()
        return json.loads(json_str)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to parse structured data from response: {str(e)}"
        )

def generate_roadmap(
    company_name: str,
    loyalty_program_design: Optional[str] = None,
    financial_model: Optional[str] = None,
    existing_output: Optional[str] = None,
    feedback: Optional[str] = None
) -> tuple[str, dict]:
    """Generate implementation roadmap using OpenAI's API"""
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": construct_system_prompt()},
                {"role": "user", "content": construct_user_prompt(
                    company_name,
                    loyalty_program_design,
                    financial_model,
                    existing_output,
                    feedback
                )}
            ],
            temperature=0.7,
            max_tokens=2000
        )
        
        full_response = response.choices[0].message.content
        narrative = full_response[:full_response.find("[JSON_START]")].strip()
        structured_data = extract_json_from_text(full_response)
        
        return narrative, structured_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate", response_model=RoadmapResponse)
async def generate_analysis(request: RoadmapRequest):
    # Extract data from request
    loyalty_program_design = None
    financial_model = None
    if request.previous_data:
        loyalty_program_design = request.previous_data.loyalty_program_design
        financial_model = request.previous_data.financial_model
    
    existing_output = None
    feedback = None
    if request.current_prompt_data:
        existing_output = request.current_prompt_data.existing_generated_output
        feedback = request.current_prompt_data.user_feedback
    
    # Generate roadmap
    generated_text, structured_data = generate_roadmap(
        request.company_name,
        loyalty_program_design,
        financial_model,
        existing_output,
        feedback
    )
    
    # Prepare response
    return RoadmapResponse(
        generated_output=generated_text,
        structured_data=structured_data
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)