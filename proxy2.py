import requests
import anthropic
import json
import os
import time

# Claude API setup
anthropic_client = anthropic.Anthropic(api_key="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")

def prompt_to_params_with_claude(prompt):
    system_prompt = """
You are an expert API wrapper for Proxycurl's person search endpoint.

Given a natural language prompt, return a clean JSON dictionary of the most relevant Proxycurl parameters.
Only include relevant fields, and follow these rules:

- When the user specifies multiple values for a single field (e.g. multiple schools or companies), use "OR" between them.
  Example: 'education_school_name': 'Caltech OR Massachusetts Institute of Technology'
- Do not use commas or the word "and" to separate values.
- Map city-level locations to 'city', and U.S. states or countries to 'region'.
- Do not explain your response. Only return raw JSON.

Allowed fields include:
'country', 'first_name', 'last_name', 'current_role_title', 'past_role_title',
'current_job_description', 'past_job_description', 'current_company_name',
'past_company_name', 'languages', 'city', 'industries',
'interests', 'skills'
""".strip()

    completion = anthropic_client.messages.create(
        model="claude-3-sonnet-20240229",
        max_tokens=512,
        temperature=0.3,
        system=system_prompt,
        messages=[{"role": "user", "content": prompt}]
    )

    try:
        return json.loads(completion.content[0].text)
    except Exception as e:
        print("Error parsing response:", e)
        return {}

# --- User input
user_prompt = input("Describe the person you're searching for: ")

# --- Generate params
params = prompt_to_params_with_claude(user_prompt)
print("Search params:", params)

# Add defaults
params.setdefault('country', 'US')
params.setdefault('page_size', '10')

# --- Proxycurl Search
api_key = 'tplpB_wWRHbhnBnwReBNtQ'
headers = {'Authorization': f'Bearer {api_key}'}
search_endpoint = 'https://nubela.co/proxycurl/api/v2/search/person'
enrich_endpoint = 'https://nubela.co/proxycurl/api/v2/linkedin'
email_endpoint = 'https://nubela.co/proxycurl/api/linkedin/profile/email'

search_response = requests.get(search_endpoint, params=params, headers=headers)
people = search_response.json().get("results", [])

enriched_final = []

for person in people:
    linkedin_url = person.get("linkedin_profile_url")
    if not linkedin_url:
        continue

    # --- General enrichment
    enrich_params = {
        "linkedin_profile_url": linkedin_url,
        "use_cache": "if-present",
        "fallback_to_cache": "on-error"
    }

    enrich_response = requests.get(enrich_endpoint, params=enrich_params, headers=headers)
    if enrich_response.status_code != 200:
        print(f"Enrichment failed for {linkedin_url}")
        continue

    profile_data = enrich_response.json()

    # --- Work email lookup
    email_params = {"linkedin_profile_url": linkedin_url}
    work_email = None
    try:
        email_response = requests.get(email_endpoint, params=email_params, headers=headers)
        if email_response.status_code == 200:
            work_email = email_response.json().get("email")
    except Exception as e:
        print(f"Error retrieving work email for {linkedin_url}: {e}")

    # Use work email if available, else fallback to personal
    email = work_email or profile_data.get("personal_email")

    # Extract name
    full_name = profile_data.get("full_name", "")
    first_name = full_name.split()[0] if full_name else None
    last_name = " ".join(full_name.split()[1:]) if full_name and len(full_name.split()) > 1 else None

    enriched_final.append({
        "first_name": first_name,
        "last_name": last_name,
        "job_title": profile_data.get("occupation"),
        "company": (
            profile_data.get("experiences", [{}])[0].get("company")
            if profile_data.get("experiences") else None
        ),
        "email": email
    })

    time.sleep(1)

# --- Final output
print(json.dumps(enriched_final, indent=2))
