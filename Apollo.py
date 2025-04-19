from crewai import Agent, Crew, Task, LLM
from composio_crewai import ComposioToolSet, Action, App
import json

# Load Apollo toolset
toolset = ComposioToolSet()
tools = toolset.get_tools(apps=[App.APOLLO])

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

# Define a task with JSON output format
search_task = Task(
    description="""
    Search for venture capitalists and investors in the blockchain/web3 space using Apollo.
    
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
    
    Find at least 10 qualified blockchain/web3 investors.
    """,
    agent=apollo_agent,
    expected_output="JSON array containing at least 10 qualified blockchain/web3 investors with their first name, last name, company, location, and linkedin URL",
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

# Ensure the result is properly formatted JSON
try:
    # Try to parse the result as JSON
    parsed_result = json.loads(result)
    print("\n Apollo People Search Results (JSON):\n")
    print(json.dumps(parsed_result, indent=2))
    
    # Save to file (optional)
    with open("blockchain_investors.json", "w") as f:
        json.dump(parsed_result, f, indent=2)
    print("\nResults saved to blockchain_investors.json")
    
except json.JSONDecodeError:
    # If the result isn't valid JSON, print the raw result
    print("\Result was not in valid JSON format. Raw result:")
    print(result)