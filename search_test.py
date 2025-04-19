import requests
import json

# Apollo API key
api_key = "rZdS9o5gSyzGXDJkhpg2Zg"

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

# Run the script
if __name__ == "__main__":
    main()