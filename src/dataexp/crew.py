from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai.knowledge.source.pdf_knowledge_source import PDFKnowledgeSource
from typing import List
import os
from .tools.data_tool import get_column_names, execute_sql_on_csv, get_dataframe_info

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
    def data_engineer(self) -> Agent:
        return Agent(
            config=self.agents_config['data_engineer'], # type: ignore[index]
            verbose=True
        )
    
    @agent
    def sql_developer(self) -> Agent:
        return Agent(
            config=self.agents_config['sql_developer'], # type: ignore[index]
            verbose=True,
            tools=[get_column_names, get_dataframe_info]
        )

    @agent
    def sql_executor(self) -> Agent:
        return Agent(
            config=self.agents_config['sql_executor'], # type: ignore[index]
            verbose=True,
            tools=[execute_sql_on_csv]
        )
    
    # To learn more about structured task outputs,
    # task dependencies, and task callbacks, check out the documentation:
    # https://docs.crewai.com/concepts/tasks#overview-of-a-task
    @task
    def interpret_user_input_task(self) -> Task:
        return Task(
            config=self.tasks_config['interpret_user_input_task'], # type: ignore[index]
        )

    @task
    def run_sql_queries_task(self) -> Task:
        return Task(
            config=self.tasks_config['run_sql_queries_task'], # type: ignore[index]
            output_file='report.md'
        )
    
    @crew
    def crew(self) -> Crew:
        """Creates the Dataexp crew"""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge
        
        # Create knowledge sources
        knowledge_sources = []
        
        # Add PDF knowledge source for Titanic metadata
        titanic_meta_path = f'..\\..\\knowledge\\TitanicMETA.pdf'
        if os.path.exists(titanic_meta_path):
            titanic_meta_knowledge = PDFKnowledgeSource(
                file_path=titanic_meta_path,
                metadata={"source": "titanic_metadata", "type": "dataset_documentation"}
            )
            knowledge_sources.append(titanic_meta_knowledge)

        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            knowledge_sources=knowledge_sources,
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )
