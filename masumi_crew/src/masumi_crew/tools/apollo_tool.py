from crewai.tools import BaseTool
from typing import Type, List, Dict, Any, Optional
from pydantic import BaseModel, Field
import json
from composio_crewai import ComposioToolSet, App


class ApolloSearchInput(BaseModel):
    """Input schema for ApolloSearchTool."""
    query: str = Field(..., description="The search query to find people in Apollo.")
    limit: Optional[int] = Field(10, description="Maximum number of results to return.")


class ApolloSearchTool(BaseTool):
    name: str = "Apollo People Search"
    description: str = (
        "Search for people using Apollo's database. Useful for finding professionals, "
        "investors, or decision-makers in specific industries or companies."
    )
    args_schema: Type[BaseModel] = ApolloSearchInput

    def _run(self, query: str, limit: int = 3) -> str:
        # Initialize the Apollo toolset
        toolset = ComposioToolSet()
        tools = toolset.get_tools(apps=[App.APOLLO])
        
        # Use the Apollo search tool
        apollo_tool = tools[0]  # Assuming the first tool is the search tool
        
        # Execute the search
        result = apollo_tool.run(query=query, limit=limit)
        
        # Apollo API key for enrichment
        api_key = ""

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
                    
                    enriched_contacts.append(enriched_contact)
                    print(f"Enriched contact: {full_name}")
                    
                except Exception as e:
                    print(f"Error enriching contact {full_name}: {e}")
                    # If enrichment fails, add the original contact
                    enriched_contacts.append(contact)
            
            # Print the final enriched contacts
            return json.dumps(enriched_contacts, indent=2)
            
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

            return json.dumps([], indent=2)