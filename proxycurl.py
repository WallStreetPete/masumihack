import requests

api_key = 'tplpB_wWRHbhnBnwReBNtQ'
headers = {'Authorization': 'Bearer ' + api_key}
api_endpoint = 'https://nubela.co/proxycurl/api/v2/search/person'
params = {
    'country': 'US',
    'current_role_title': 'founder',
    'current_job_description': 'education',
    'region': 'California',
    'city': 'Seattle OR Los Angeles',
    'page_size': '10',
}
response = requests.get(api_endpoint,
                        params=params,
                        headers=headers)

print(response.json())