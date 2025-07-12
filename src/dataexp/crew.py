from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai.knowledge.source.text_file_knowledge_source import TextFileKnowledgeSource
from crewai.knowledge.source.string_knowledge_source import StringKnowledgeSource
from typing import List
import os

# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

@CrewBase
class Dataexp():
    """Dataexp crew"""

    agents: List[BaseAgent]
    tasks: List[Task]

    # Learn more about YAML configuration files here:
    # Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
    # Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
    
    # If you would like to add tools to your agents, you can learn more about it here:
    # https://docs.crewai.com/concepts/agents#agent-tools
    @agent
    def researcher(self) -> Agent:
        return Agent(
            config=self.agents_config['researcher'], # type: ignore[index]
            verbose=True
        )

    @agent
    def reporting_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['reporting_analyst'], # type: ignore[index]
            verbose=True
        )
    
    @agent
    def python_developer(self) -> Agent:
        return Agent(
            config=self.agents_config['python_developer'], # type: ignore[index]
            verbose=True
        )

    # To learn more about structured task outputs,
    # task dependencies, and task callbacks, check out the documentation:
    # https://docs.crewai.com/concepts/tasks#overview-of-a-task
    @task
    def research_task(self) -> Task:
        return Task(
            config=self.tasks_config['research_task'], # type: ignore[index]
        )

    @task
    def reporting_task(self) -> Task:
        return Task(
            config=self.tasks_config['reporting_task'], # type: ignore[index]
            output_file='report.md'
        )
    
    @task
    def convert_to_dataframe_task(self) -> Task:
        return Task(
            config=self.tasks_config['convert_to_dataframe_task'], # type: ignore[index]
            output_file='report_japanese.md'
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Dataexp crew"""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge
        
        # Create knowledge sources
        knowledge_sources = []
        
        # Add text file knowledge source
        user_preference_path = f'..\\..\\knowledge\\user_preference.txt'
        if os.path.exists(user_preference_path):
            user_preference_knowledge = TextFileKnowledgeSource(
                file_path=user_preference_path,
                metadata={"source": "user_preferences", "type": "user_context"}
            )
            knowledge_sources.append(user_preference_knowledge)

        # Add string-based knowledge
        string_knowledge = StringKnowledgeSource(
            content="Additional context: The user is an AI Engineer interested in AI Agents, based in San Francisco.",
            metadata={"source": "direct_context", "type": "user_info"}
        )
        knowledge_sources.append(string_knowledge)

        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            knowledge_sources=knowledge_sources,
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )
