from crewai.flow.flow import Flow, listen, start, router, and_, or_
from pydantic import BaseModel

class ContentPipelineState(BaseModel):
    content_type: str =""
    topic: str = ""


class ContentPipelineFlow(Flow[ContentPipelineState]):

    @start()
    def init_content_pipeline(self):
        print(self.state.content_type)
        print(self.state.topic)


flow = ContentPipelineFlow()

flow.kickoff(
    inputs={
        "content_type": "tweet",
        "topic": "AI and Job Security",
    }
)
