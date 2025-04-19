from crewai import Agent, Crew, Task
from composio_crewai import ComposioToolSet, Action, App

toolset = ComposioToolSet()
tools = toolset.get_tools(
    actions=[Action.GITHUB_STAR_A_REPOSITORY_FOR_THE_AUTHENTICATED_USER]
)

tools = toolset.get_tools(apps=[App.APOLLO])

class ResearchCrew:
    def __init__(self, verbose=True):
        self.verbose = verbose
        self.crew = self.create_crew()

    def create_crew(self):
        researcher = Agent(
            role='Research Analyst',
            goal='Find and analyze key information',
            backstory='Expert at extracting information',
            verbose=self.verbose
        )

        writer = Agent(
            role='Content Summarizer',
            goal='Create clear summaries from research',
            backstory='Skilled at transforming complex information',
            verbose=self.verbose
        )

        # Create GitHub agent
        crewai_agent = Agent(
            role="GitHub Agent",
            goal="Star GitHub repositories using APIs",
            backstory="Takes GitHub actions on behalf of users",
            verbose=True,
            tools=tools
        )

        # Now assign the task — AFTER the agent exists
        github_task = Task(
            description="Star a repo composiohq/composio on GitHub",
            agent=crewai_agent,
            expected_output="Status of the operation"
        )

        # Define crew
        crew = Crew(
            agents=[researcher, writer, crewai_agent],
            tasks=[
                Task(
                    description='Research: {text}',
                    expected_output='Detailed research findings about the topic',
                    agent=researcher
                ),
                Task(
                    description='Write summary',
                    expected_output='Clear and concise summary of the research findings',
                    agent=writer
                ),
                github_task
            ]
        )

        return crew