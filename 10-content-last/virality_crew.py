# 5
from crewai.project import CrewBase, agent, task, crew
from crewai import Agent, Task, Crew
from pydantic import BaseModel


class Score(BaseModel):
    score: int
    reason: str


@CrewBase
class ViralityCrew:

    @agent
    def virality_expert_agent(self):
        return Agent(
            config=self.agents_config["virality_expert_agent"]
        )

    @task
    def virality_expert_task(self):
        return Task(
            config=self.tasks_config["virality_expert_task"]
        )
    
    @crew
    def assemble_crew(self):
        return Crew(
            agents = self.agents,
            tasks=self.tasks,
            verbose=True,
        )