from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from masumi_crew.tools.apollo_tool import ApolloSearchTool

# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

@CrewBase
class MasumiCrew():
    """MasumiCrew crew"""

    # Learn more about YAML configuration files here:
    # Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
    # Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    # If you would like to add tools to your agents, you can learn more about it here:
    # https://docs.crewai.com/concepts/agents#agent-tools
        
    @agent
    def apollo_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['apollo_agent'],
            tools=[ApolloSearchTool()],
            verbose=True,
            llm=LLM(model="deepseek/deepseek-chat", api_key="", temperature=1.5)
        )

    # To learn more about structured task outputs,
    # task dependencies, and task callbacks, check out the documentation:
    # https://docs.crewai.com/concepts/tasks#overview-of-a-task

    @task
    def apollo_search_task(self) -> Task:
        return Task(
            config=self.tasks_config['apollo_search_task'],
            output_file='apollo_results.json'
        )

    @crew
    def crew(self) -> Crew:
        """Creates the MasumiCrew crew"""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )
