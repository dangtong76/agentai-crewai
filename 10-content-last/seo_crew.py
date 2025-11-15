# 5
from crewai.project import CrewBase, agent, task, crew
from crewai import Agent, Task, Crew


@CrewBase
class SeoCrew:

    @agent
    def seo_expert_agent(self):
        return Agent(
            config=self.agents_config["seo_expert_agent"]
        )

    @task
    def seo_expert_task(self):
        return Task(
            config=self.tasks_config["seo_expert_task"]
        )
    
    @crew
    def assemble_crew(self):
        return Crew(
            agents = self.agents,
            tasks=self.tasks,
            verbose=True,
        )