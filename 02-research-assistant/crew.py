import dotenv
import os
from datetime import datetime
dotenv.load_dotenv()

from crewai import Agent, Task, Crew, LLM
from crewai.project import CrewBase, agent, task, crew
from crewai_tools import SerperDevTool, FileReadTool, FileWriterTool, ScrapeWebsiteTool

# 환경변수 로드
RESEARCH_MODEL = os.getenv("RESEARCH_MODEL")
RESEARCH_MODEL_URL = os.getenv("RESEARCH_MODEL_URL")

ANALYST_MODEL = os.getenv("ANALYST_MODEL")
ANALYST_MODEL_URL = os.getenv("ANALYST_MODEL_URL")

WRITER_MODEL = os.getenv("WRITER_MODEL")
WRITER_MODEL_URL = os.getenv("WRITER_MODEL_URL")

TRANSLATOR_MODEL = os.getenv("TRANSLATOR_MODEL")
TRANSLATOR_MODEL_URL = os.getenv("TRANSLATOR_MODEL_URL")

# 타임스탬프 생성
timestamp = datetime.now().strftime("%Y%m%d-%H%M")  # 예: 20251013-1430


# 모델 생성 함수
def create_agent_with_model(config, model_name, model_url, tools):
    """
    모델 URL 유무에 따라 온라인/오프라인 모델 자동 선택
    - model_url 있음 → LLM 객체 생성 (오프라인)
    - model_url 없음 → 문자열 전달 (온라인, 자동 감지)
    """
    agent_kwargs = {
        "config": config,
        "tools": tools
    }
    if model_url:
        # 오프라인 모델: base_url 지정
        agent_kwargs["llm"] = LLM(
            model=model_name, 
            base_url=model_url
        )
    else:
        # 온라인 모델: 자동 감지
        agent_kwargs["model"] = model_name
    
    return Agent(**agent_kwargs)


@CrewBase

class ResearchCrew:
    

    @agent
    def research_specialist_agent(self):
        return create_agent_with_model(
            config=self.agents_config["research_specialist_agent"],
            model_name=RESEARCH_MODEL,
            model_url=RESEARCH_MODEL_URL,
            tools=[SerperDevTool(), ScrapeWebsiteTool()]
        )
    
    @task
    def research_specialist_task(self):
        return Task(
            config=self.tasks_config["research_specialist_task"]
        )
    

    @agent
    def data_analyst_agent(self):
        return create_agent_with_model(
            config=self.agents_config["data_analyst_agent"],
            model_name=ANALYST_MODEL,
            model_url=ANALYST_MODEL_URL,
            tools=[]
        )
    
    @task
    def data_analyst_task(self):
        return Task(
            config=self.tasks_config["data_analyst_task"]
        )


    @agent
    def content_writer_agent(self):
        return create_agent_with_model(
            config=self.agents_config["content_writer_agent"],
            model_name=WRITER_MODEL,
            model_url=WRITER_MODEL_URL,
            tools=[]
        )
    
    @task
    def content_writer_task(self):
        return Task(
            config=self.tasks_config["content_writer_task"]
        )   
    
    @agent
    def translator_agent(self):
        return create_agent_with_model(
            config=self.agents_config["translator_agent"],
            model_name=TRANSLATOR_MODEL,
            model_url=TRANSLATOR_MODEL_URL,
            tools=[]
        )
    
    @task
    def translator_task(self):
        return Task(
            config=self.tasks_config["translator_task"]
        )
    
    @crew
    def assemble_crew(self):
        return Crew(
            agents = self.agents,
            tasks=self.tasks,
            verbose=True,
        )
# 모델 설정 상태 출력
print("=" * 80)
print("🚀 Starting Crew with following model configurations:")
print("=" * 80)
print(f"📝 Research : {RESEARCH_MODEL:20s} {'🏠 Offline @ ' + RESEARCH_MODEL_URL if RESEARCH_MODEL_URL else '☁️  Online (auto-detect)'}")
print(f"📊 Analyst  : {ANALYST_MODEL:20s} {'🏠 Offline @ ' + ANALYST_MODEL_URL if ANALYST_MODEL_URL else '☁️  Online (auto-detect)'}")
print(f"✍️  Writer   : {WRITER_MODEL:20s} {'🏠 Offline @ ' + WRITER_MODEL_URL if WRITER_MODEL_URL else '☁️  Online (auto-detect)'}")
print(f"🌏 Translator: {TRANSLATOR_MODEL:20s} {'🏠 Offline @ ' + TRANSLATOR_MODEL_URL if TRANSLATOR_MODEL_URL else '☁️  Online (auto-detect)'}")
print(f"⏰ Timestamp : {timestamp}")
print("=" * 80)
print()

# 파일명 안전하게 변환
safe_name = lambda m: m.replace("/", "_").replace(":", "_") if m else "default"

ResearchCrew().assemble_crew().kickoff(
    inputs={
        "topic": "AI and Job Security", 
        "research_specialist_model_name": f"{timestamp}_{safe_name(RESEARCH_MODEL)}",
        "data_analyst_model_name": f"{timestamp}_{safe_name(ANALYST_MODEL)}",
        "content_writer_model_name": f"{timestamp}_{safe_name(WRITER_MODEL)}",
        "translator_model_name": f"{timestamp}_{safe_name(TRANSLATOR_MODEL)}"
    }
)