# MasumiCrew with Apollo Integration

This project is a template for CrewAI that includes an Apollo agent for people search functionality.

## Features

- Standard CrewAI template with researcher and reporting analyst agents
- Apollo agent for searching and finding people in specific industries
- JSON output format for Apollo search results

## Installation

1. Clone this repository
2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

### Running the Crew

To run the crew with default settings:

```bash
python -m masumi_crew.main
```

This will execute the crew with the following default parameters:
- Topic: AI LLMs
- Search Target: venture capitalists
- Industry: blockchain/web3
- Limit: 10 results

### Customizing the Search

You can modify the search parameters in the `main.py` file:

```python
inputs = {
    'topic': 'AI LLMs',
    'current_year': str(datetime.now().year),
    'search_target': 'venture capitalists',  # Change this to search for different types of people
    'industry': 'blockchain/web3',           # Change this to search in different industries
    'limit': 10                              # Change this to get more or fewer results
}
```

### Output

The Apollo search results will be saved to `apollo_results.json` in the following format:

```json
[
    {
        "first_name": "First Name",
        "last_name": "Last Name",
        "organization_name": "Company Name",
        "linkedin_url": "LinkedIn URL"
    },
    ...
]
```

## Apollo API Key

To use the Apollo agent, you need to have a valid Apollo API key. The `composio_crewai` package will handle the authentication for you.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
