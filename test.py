import requests
import json

# Apollo API key
api_key = "l-UG2w5z1LeZOzJya2JWBg"

# People Search endpoint
search_url = "https://api.apollo.io/api/v1/mixed_people/search"

# Set up headers
headers = {
    "accept": "application/json",
    "Cache-Control": "no-cache",
    "Content-Type": "application/json",
    "x-api-key": api_key
}

# Search payload - parameters for finding blockchain/web3 investors
search_payload = {
    "person_titles": ["Investor", "Venture Capitalist"],
    "q_keywords": "blockchain web3",
    "page": 1,
    "per_page": 10
}

# Function to search for people
def search_apollo_people():
    try:
        # Make the API call
        response = requests.post(search_url, headers=headers, json=search_payload)
        print(f"Search API Response Status: {response.status_code}")
        
        if response.status_code == 200:
            # Parse the response
            search_results = response.json()
            
            # Extract people from the response
            if 'people' in search_results:
                people = search_results['people']
                
                # Format the results as needed
                formatted_results = []
                
                for person in people:
                    # Extract basic information
                    contact = {
                        "first_name": person.get('first_name', ''),
                        "last_name": person.get('last_name', ''),
                        "organization_name": person.get('organization_name', ''),
                        "linkedin_url": person.get('linkedin_url', '')
                    }
                    
                    formatted_results.append(contact)
                
                return formatted_results
            else:
                print("No people found in search results.")
                return []
        else:
            print(f"Search API Error: {response.status_code} - {response.text}")
            return []
            
    except Exception as e:
        print(f"Error in search_apollo_people: {e}")
        return []

# Function to enrich a contact using the people/match endpoint
def enrich_contact(contact):
    try:
        # People Match endpoint
        match_url = "https://api.apollo.io/api/v1/people/match?reveal_personal_emails=true"
        
        full_name = f"{contact.get('first_name', '')} {contact.get('last_name', '')}"
        organization = contact.get('organization_name', '')
        
        # Create payload for the match API
        match_payload = {
            "name": full_name
        }
        
        # Add organization if available
        if organization:
            match_payload["organization_name"] = organization
        
        # Make the API call
        response = requests.post(match_url, headers=headers, json=match_payload)
        print(f"Enrichment API Response Status for {full_name}: {response.status_code}")
        
        if response.status_code == 200:
            match_result = response.json()
            
            # Create enriched contact with original data
            enriched_contact = contact.copy()
            
            # Extract person data from API response
            if match_result.get('person'):
                person_data = match_result.get('person', {})
                
                # Add enriched data fields
                enriched_contact['email'] = person_data.get('email')
                enriched_contact['phone'] = person_data.get('phone')
                enriched_contact['title'] = person_data.get('title')
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
            
            return enriched_contact
        else:
            print(f"Enrichment API Error: {response.status_code} - {response.text}")
            return contact
            
    except Exception as e:
        print(f"Error in enrich_contact for {contact.get('first_name', '')} {contact.get('last_name', '')}: {e}")
        return contact

# Main function to run the script
def main():
    # Search for contacts
    print("Searching for blockchain/web3 investors...")
    contacts = search_apollo_people()
    
    if not contacts:
        print("No contacts found. Exiting.")
        return
    
    print(f"\nFound {len(contacts)} contacts.")
    print(json.dumps(contacts, indent=2))
    
    # Enrich each contact
    print("\nEnriching contacts...")
    enriched_contacts = []
    
    for contact in contacts:
        print(f"\nEnriching {contact.get('first_name', '')} {contact.get('last_name', '')}...")
        enriched_contact = enrich_contact(contact)
        enriched_contacts.append(enriched_contact)
    
    # Output the final enriched results
    print("\nEnriched Contacts (JSON):")
    print(json.dumps(enriched_contacts, indent=2))
    
    # Optionally save to a file
    # with open("enriched_blockchain_investors.json", "w") as f:
    #     json.dump(enriched_contacts, f, indent=2)
    # print("\nResults saved to enriched_blockchain_investors.json")

# Run the script
if __name__ == "__main__":
    main()