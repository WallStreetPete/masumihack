import os
import uvicorn
import uuid
from dotenv import load_dotenv
from fastapi import FastAPI, Query
from pydantic import BaseModel
from datetime import datetime, timezone
from typing import List, Optional
from crewai import Agent, Crew, Task, LLM
from composio_crewai import ComposioToolSet, App
from crewai_tools import BraveSearchTool

# Load environment variables
load_dotenv()

# Retrieve OpenAI API Key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize FastAPI
app = FastAPI()

# Add root endpoint that redirects to docs
@app.get("/")
async def root():
    return {"message": "Welcome to Apollo Email Crew API", "docs_url": "http://localhost:8000/docs"}

# Temporary in-memory job store (DO NOT USE IN PRODUCTION)
jobs = {}

# Pydantic Models
class KeyValuePair(BaseModel):
    key: str
    value: str

class StartJobRequest(BaseModel):
    text: str

class ProvideInputRequest(BaseModel):
    job_id: str

class ApolloEmailCrew:
    def __init__(self):
        self.toolset = ComposioToolSet()
        self.apollo_tools = self.toolset.get_tools(apps=[App.APOLLO])
        self.gmail_tools = self.toolset.get_tools(apps=[App.GMAIL])
        self.brave_search = BraveSearchTool(n_results=3)
        
        self.llm = LLM(
            model="gpt-4-turbo",
            max_tokens=4000,
        )
        
        self.apollo_agent = Agent(
            role="Lead Prospector",
            goal="Find the right people using Apollo's people search and return results in JSON format",
            backstory="Expert at identifying and sourcing the right professionals for outreach in emerging technology sectors.",
            tools=self.apollo_tools,
            verbose=True,
            llm=self.llm
        )
        
        self.email_agent = Agent(
            role="Email Outreach Specialist",
            goal="Send personalized emails to contacts using Gmail API",
            backstory="Expert in crafting and sending professional outreach emails with high response rates.",
            tools=self.gmail_tools,
            verbose=True,
            llm=self.llm
        )
        
        self.search_task = Task(
            description="""
            Seed-stage investors focused on B2B SaaS with $500K-$1M check sizes

            IMPORTANT: When using the Apollo search tool, use a simpler query format to avoid 422 errors. 
            Only use the most essential parameters. For example:
            {"person_titles": ["Investor"], "q_keywords": "b2b"}
            
            If the Apollo API fails, compile a list from your general knowledge.
            Please make sure most of them have an email, if not, try not to return it.
            """,
            agent=self.apollo_agent,
            expected_output="""
            If you get an error, try a different combination of parameters or keywords.

            You MUST return your results in valid JSON format with the following structure:
            [
                {
                    "first_name": "First Name",
                    "title": "Title",
                    "seniority": "Seniority",
                    "last_name": "Last Name",
                    "organization_name": "Company Name",
                    "linkedin_url": "LinkedIn URL",
                    "email": "Email Address",
                    "description": "Description"
                },
                ...
            ]

            If you don't have access to any of the fields just generate a fake one for it. for email just do first_name + last_name + @organization_name.com
            DONT RETURN ANYTHING ELSE. ONLY THE JSON.
            """,
            llm=self.llm
        )
        
        self.email_task = Task(
            description="""
            Send personalized emails to each contact in the enriched contacts list.
            
            For each contact, create a personalized email that includes:
            1. Their name and company
            2. A brief introduction
            3. The value proposition
            4. A clear call to action
            
            Use the GMAIL_SEND_EMAIL tool with the following parameters:
            - user_id: 'me'
            - recipient_email: The contact's email
            - subject: Personalized subject line
            - body: The email content
            - is_html: true
            
            Return a status report for each email sent.
            """,
            agent=self.email_agent,
            expected_output="""List of email sending status reports, output in JSON format ONLY. DON'T RETURN ANYTHING ELSE {
               "email_content": "Email content",
               "status": "success"
            }""",
            llm=self.llm
        )
        
        self.crew = Crew(
            agents=[self.apollo_agent, self.email_agent],
            tasks=[self.search_task, self.email_task],
            verbose=True,
            llm=self.llm
        )
    
    def execute(self, inputs=None):
        return self.crew.kickoff(inputs)
        

# 1) Start Job (MIP-003: /start_job)
@app.post("/start_job")
async def start_job(request_body: StartJobRequest):
    """
    Initiates a job with specific input data.
    Fulfills MIP-003 /start_job endpoint.
    """
    if not OPENAI_API_KEY:
        return {"status": "error", "message": "Missing OpenAI API Key. Check your .env file."}

    # Generate unique job & payment IDs
    job_id = str(uuid.uuid4())
    payment_id = str(uuid.uuid4())  # Placeholder, in production track real payment

    # For demonstration: set job status to 'awaiting payment'
    jobs[job_id] = {
        "status": "awaiting payment",
        "payment_id": payment_id,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "input_data": request_body.text,
        "result": None
    }

    # Initialize and execute crew
    crew = ApolloEmailCrew()
    inputs = {"text": request_body.text}
    result = crew.execute(inputs)

    # Store result
    jobs[job_id]["status"] = "completed"
    jobs[job_id]["result"] = result

    return {
        "status": "success",
        "job_id": job_id,
        "payment_id": payment_id
    }

# 2) Check Job Status (MIP-003: /status)
@app.get("/status")
async def check_status(job_id: str = Query(..., description="Job ID to check status")):
    """
    Retrieves the current status of a specific job.
    Fulfills MIP-003 /status endpoint.
    """
    if job_id not in jobs:
        return {"error": "Job not found"}

    job = jobs[job_id]
    return {
        "job_id": job_id,
        "status": job["status"],
        "result": job["result"]
    }

# 3) Provide Input (MIP-003: /provide_input)
@app.post("/provide_input")
async def provide_input(request_body: ProvideInputRequest):
    """
    Allows users to send additional input if a job is in an 'awaiting input' status.
    Fulfills MIP-003 /provide_input endpoint.
    """
    job_id = request_body.job_id

    if job_id not in jobs:
        return {"status": "error", "message": "Job not found"}

    return {"status": "success"}

# 4) Check Server Availability (MIP-003: /availability)
@app.get("/availability")
async def check_availability():
    """
    Checks if the server is operational.
    Fulfills MIP-003 /availability endpoint.
    """
    return {
        "status": "available",
        "message": "The server is running smoothly."
    }

# 5) Retrieve Input Schema (MIP-003: /input_schema)
@app.get("/input_schema")
async def input_schema():
    """
    Returns the expected input schema for the /start_job endpoint.
    Fulfills MIP-003 /input_schema endpoint.
    """
    schema_example = {
        "input_data": [
            {"key": "text", "value": "string"}
        ]
    }
    return schema_example

# Main logic if called as a script
def main():
    if not OPENAI_API_KEY:
        print("Error: OPENAI_API_KEY is missing. Please check your .env file.")
        return

    crew = ApolloEmailCrew()
    inputs = {"text": "The impact of AI on the job market"}
    result = crew.execute(inputs)
    print("\nCrew Output:\n", result)

if __name__ == "__main__":
    import sys

    # If 'api' argument is passed, start the FastAPI server
    if len(sys.argv) > 1 and sys.argv[1] == "api":
        print("Starting FastAPI server...")
        print("API is now listening at http://localhost:8000")
        print("API documentation available at http://localhost:8000/docs")
        uvicorn.run(app, host="0.0.0.0", port=8000)
    else:
        main() 