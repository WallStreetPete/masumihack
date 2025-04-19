from crewai import Agent, Crew, Task, LLM
from composio_crewai import ComposioToolSet, App
from crewai_tools import BraveSearchTool
import json
import time
import requests
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Load Apollo and Gmail toolsets
toolset = ComposioToolSet()
apollo_tools = toolset.get_tools(apps=[App.APOLLO])
gmail_tools = toolset.get_tools(apps=[App.GMAIL])

# Initialize Brave Search tool
brave_search = BraveSearchTool(n_results=3)

# Use a model with larger context window
llm = LLM(
    model="gpt-4-turbo",
    max_tokens=4000,
)

# Create agents
apollo_agent = Agent(
    role="Lead Prospector",
    goal="Find the right people using Apollo's people search and return results in JSON format",
    backstory="Expert at identifying and sourcing the right professionals for outreach in emerging technology sectors.",
    tools=apollo_tools,
    verbose=True,
    llm=llm
)

email_agent = Agent(
    role="Email Outreach Specialist",
    goal="Send personalized emails to contacts using Gmail API",
    backstory="Expert in crafting and sending professional outreach emails with high response rates.",
    tools=gmail_tools,
    verbose=True,
    llm=llm
)

# Define tasks
search_task = Task(
    description="""
    Search for venture capitalists and investors in the blockchain/web3 space using Apollo.
    
    IMPORTANT: When using the Apollo search tool, use a simpler query format to avoid 422 errors. 
    Only use the most essential parameters. For example:
    {"person_titles": ["Investor"], "q_keywords": "blockchain"}
    
    If you get an error, try a different combination of parameters or keywords.
    
    You MUST return your results in valid JSON format with the following structure:
    [
        {
            "first_name": "First Name",
            "last_name": "Last Name",
            "organization_name": "Company Name",
            "linkedin_url": "LinkedIn URL"
        },
        ...
    ]
    
    Find blockchain/web3 investors. If the Apollo API fails, compile a list from your general knowledge.
    """,
    agent=apollo_agent,
    expected_output="JSON array containing blockchain/web3 investors with their first name, last name, company, and linkedin URL",
    llm=llm
)

email_task = Task(
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
    agent=email_agent,
    expected_output="List of email sending status reports",
    llm=llm
)

# Assemble the crew
crew = Crew(
    agents=[apollo_agent, email_agent],
    tasks=[search_task, email_task],
    verbose=True,
    llm=llm
)

# Run the crew
result = crew.kickoff()

# Apollo API key for enrichment
api_key = os.getenv("APOLLO_API_KEY")

# Endpoint for people match
url = "https://api.apollo.io/api/v1/people/match?reveal_personal_emails=true"

# Set up headers
headers = {
    "accept": "application/json",
    "cache-control": "no-cache",
    "content-type": "application/json",
    "x-api-key": api_key
}

# Parse the initial results
try:
    # Try to parse the result as JSON
    initial_contacts = json.loads(str(result))
    print("\nInitial Apollo Search Results (JSON):\n")
    print(json.dumps(initial_contacts, indent=2))
    
    # Enrich each contact using the Apollo people match API
    enriched_contacts = []
    
    for contact in initial_contacts:
        full_name = f"{contact.get('first_name', '')} {contact.get('last_name', '')}"
        organization = contact.get('organization_name', '')
        
        # Prepare domain - handle possible None values
        if organization:
            # Extract domain from organization name more carefully
            domain_parts = organization.lower().split()
            if len(domain_parts) > 0:
                domain = domain_parts[0].replace(",", "").replace(".", "")
                if domain:  # Only add .com if we have a domain
                    domain += ".com"
            else:
                domain = ""
        else:
            domain = ""
        
        # Create payload for Apollo people match API
        payload = {"name": full_name}
        
        # Only add domain if we have a non-empty one
        if domain:
            payload["domain"] = domain
            
        # Add organization if available
        if organization:
            payload["organization_name"] = organization
        
        try:
            # Call Apollo people match API with retry logic
            max_retries = 3
            for retry in range(max_retries):
                try:
                    response = requests.post(url, headers=headers, json=payload)
                    if response.status_code == 200:
                        match_result = response.json()
                        break
                    elif response.status_code == 429:  # Rate limit
                        wait_time = min(2 ** retry, 8)  # Exponential backoff
                        print(f"Rate limited. Waiting {wait_time} seconds before retry.")
                        time.sleep(wait_time)
                    else:
                        print(f"API error: {response.status_code} - {response.text}")
                        if retry == max_retries - 1:
                            match_result = {"person": None}
                        else:
                            time.sleep(1)
                except Exception as e:
                    print(f"Request error: {e}")
                    if retry == max_retries - 1:
                        match_result = {"person": None}
                    else:
                        time.sleep(1)
            
            # Combine original contact with enriched data
            enriched_contact = contact.copy()
            
            # Extract relevant fields from API response
            if match_result.get('person'):
                person_data = match_result.get('person', {})
                
                # Add enriched data to the contact
                enriched_contact['email'] = person_data.get('email')
                enriched_contact['phone'] = person_data.get('phone')
                enriched_contact['title'] = person_data.get('title')
                enriched_contact['seniority'] = person_data.get('seniority')
                enriched_contact['personal_emails'] = person_data.get('personal_emails')
                enriched_contact['city'] = person_data.get('city')
                enriched_contact['state'] = person_data.get('state')
                enriched_contact['country'] = person_data.get('country')
                
                # Add company information if available
                if person_data.get('organization'):
                    org_data = person_data.get('organization', {})
                    enriched_contact['company_size'] = org_data.get('size')
                    enriched_contact['company_industry'] = org_data.get('industry')
                    enriched_contact['company_website'] = org_data.get('website_url')
            
            # Perform Brave Search for additional context
            try:
                search_query = f"{organization}"
                search_results = brave_search.run(search_query=search_query)
                enriched_contact['brave_search_results'] = search_results
                print(f"Added Brave Search results for: {full_name}")
                # Add delay to respect rate limit of 1 request per second
                time.sleep(1)
            except Exception as e:
                print(f"Error performing Brave Search for {full_name}: {e}")
                enriched_contact['brave_search_results'] = []
                # Still add delay even if search fails
                time.sleep(1)
            
            enriched_contacts.append(enriched_contact)
            print(f"Enriched contact: {full_name}")
            
        except Exception as e:
            print(f"Error enriching contact {full_name}: {e}")
            # If enrichment fails, add the original contact
            enriched_contacts.append(contact)
    
    # Print the final enriched contacts
    print("\nEnriched Contacts (JSON):\n")
    print(json.dumps(enriched_contacts, indent=2))
    
    # Save enriched contacts to a file
    with open("enriched_contacts.json", "w") as f:
        json.dump(enriched_contacts, f, indent=2)
    
    # Pass enriched contacts to the email task
    email_task.input = json.dumps(enriched_contacts)
    
    # Run the email task
    email_result = email_agent.execute_task(email_task)
    print("\nEmail Sending Results:\n")
    print(email_result)
    
except json.JSONDecodeError as e:
    # If the result isn't valid JSON, print the raw result
    print(f"\nResult was not in valid JSON format: {e}. Raw result:")
    print(result)
    
    # Try to extract JSON using regex as a fallback
    import re
    json_pattern = r'\[\s*\{.*\}\s*\]'
    json_match = re.search(json_pattern, str(result), re.DOTALL)
    
    if json_match:
        try:
            json_str = json_match.group(0)
            parsed_result = json.loads(json_str)
            print("\nExtracted JSON successfully but could not enrich contacts:")
            print(json.dumps(parsed_result, indent=2))
        except json.JSONDecodeError:
            print("Extracted text is not valid JSON")

# ─────────────────────────────────────────────────────────────────────────────
# FastAPI Setup
# ─────────────────────────────────────────────────────────────────────────────
import uvicorn
import uuid
from fastapi import FastAPI, Query
from pydantic import BaseModel
from datetime import datetime, timezone
from typing import List, Optional

# Initialize FastAPI
app = FastAPI()

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

# 1) Start Job (MIP-003: /start_job)
@app.post("/start_job")
async def start_job(request_body: StartJobRequest):
    """
    Initiates a job with specific input data.
    Fulfills MIP-003 /start_job endpoint.
    """
    if not os.getenv("OPENAI_API_KEY"):
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

    # Here you invoke your crew
    crew = Crew(
        agents=[apollo_agent, email_agent],
        tasks=[search_task, email_task],
        verbose=True,
        llm=llm
    )
    result = crew.kickoff()

    # Store result as if we immediately completed it (placeholder)
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
    if not os.getenv("OPENAI_API_KEY"):
        print("Error: OPENAI_API_KEY is missing. Please check your .env file.")
        return

    crew = Crew(
        agents=[apollo_agent, email_agent],
        tasks=[search_task, email_task],
        verbose=True,
        llm=llm
    )
    result = crew.kickoff()
    print("\nCrew Output:\n", result)

if __name__ == "__main__":
    import sys

    # If 'api' argument is passed, start the FastAPI server
    if len(sys.argv) > 1 and sys.argv[1] == "api":
        print("Starting FastAPI server...")
        uvicorn.run(app, host="0.0.0.0", port=8000)
    else:
        main() 