from crewai import Agent, Crew, Task, LLM
from composio_crewai import ComposioToolSet, Action, App
from crewai_tools import BraveSearchTool
import json
import time
import requests
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Load Apollo toolset
toolset = ComposioToolSet()
tools = toolset.get_tools(apps=[App.APOLLO])

# Initialize Brave Search tool
brave_search = BraveSearchTool(n_results=3)

# Use a model with larger context window
llm = LLM(
    model="gpt-4-turbo",
    max_tokens=4000,
)

# Create an agent with the Apollo search tool
apollo_agent = Agent(
    role="Lead Prospector",
    goal="Find the right people using Apollo's people search and return results in JSON format",
    backstory="Expert at identifying and sourcing the right professionals for outreach in emerging technology sectors.",
    tools=tools,
    verbose=True,
    llm=llm
)

# Define a task with JSON output format - with simplified search parameters
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

# Assemble the crew
crew = Crew(
    agents=[apollo_agent],
    tasks=[search_task],
    verbose=True,
    llm=llm
)

# Run it!
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