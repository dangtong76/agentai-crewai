from crewai.flow.flow import Flow, listen, start, router, and_, or_
from pydantic import BaseModel
from crewai.agent import Agent # 1
from crewai import LLM # 10
from tools import web_search_tool # 3
from typing import List # 4.5
from dotenv import load_dotenv
load_dotenv()

class BlogPost(BaseModel): # 4 ↓
    title: str
    subtitle: str   
    sections: List[str] # go 4.5

class TweetPost(BaseModel): # 5 ↓
    content: str
    hashtags: str

class LinkedinPost(BaseModel): # 6 ↓
    hook: str
    content: str
    call_to_action: str

class Score(BaseModel):  # 14 ↓
    score: int = 0
    reason: str = ""

class ContentPipelineState(BaseModel):

    # inputs
    content_type: str =""
    topic: str = ""

    # internal state
    max_characters: int = 0
    score: int = 0
    research: str = ""  # ??
    score: Score | None = None # 15 

    # content # 9 ↓
    blog_post: BlogPost | None = None
    tweet_post: TweetPost | None = None
    linkedin_post: LinkedinPost | None = None

class ContentPipelineFlow(Flow[ContentPipelineState]):

    @start()
    def init_content_pipeline(self):
        if self.state.content_type not in ("tweet", "blog", "linkedin"):
            raise ValueError("유효하지 않은 컨텐츠 입니다.")
        
        if self.state.topic == "":
            raise ValueError("주제가 없습니다.")

        if self.state.content_type == "tweet":
            self.state.max_characters = 150
        elif self.state.content_type == "blog":
            self.state.max_characters = 800
        elif self.state.content_type == "linkedin":
            self.state.max_characters = 500
        

    @listen(init_content_pipeline)
    def conduct_research(self):
        print(f"조사시작: {self.state.topic} 에 대해 조사를 시작합니다.")
        researcher = Agent(                                         # 2 ↓
            role="조사 전문가",
            backstory="당신은 조사 전문가입니다. 조사 결과를 제공합니다.",
            goal=f"{self.state.topic} 에 대해 가능한 유용한 정보에 찾아서 조사를 시작합니다.",
            tools=[web_search_tool],
        )
        self.state.research = researcher.kickoff(
            f"{self.state.topic} 에 대해 가능한 유용한 정보에 찾아서 조사를 시작합니다."
        )                    # 2
    
    @router(conduct_research)
    def conduct_research_router(self):
        content_type = self.state.content_type

        if content_type == "blog":
            return "make_blog_post"
        elif content_type == "tweet":
            return "make_tweet_post"
        elif content_type == "linkedin": 
            return "make_linkedin_post"
        else:
            raise ValueError("유효하지 않은 컨텐츠 입니다.")

    @listen(or_("make_blog_post", "rewrite_blog_post"))
    # 블로그 작성(make_blog_post)을 AI 에게 요청 하든지, 
    # 이미 작성된 블로그가 작성된 상태(rewrite_blog_post)라면 AI 에게 보여주고 수정을 요청합니다.
    def handle_make_blog_post(self):
        print(f"블로그 포스트 작성: {self.state.topic} 에 대해 블로그 포스트를 작성합니다.")

        blog_post = self.state.blog_post  # 7 ↓

        llm = LLM(model="openai/gpt-4o-mini", response_format=BlogPost) # 11

        if blog_post is None:             # 12 ↓
            self.state.blog_post = llm.call(f"""
            다음의 research 결과를 바탕으로 {self.state.topic} 에 대한 블로그 포스트를 작성하세요
            
            <research>
            {self.state.research}
            </research>
            """)
        else:                               # 13 ↓  16. 나중에    {self.state.score.reason} 때문에 추가
            self.state.blog_post = llm.call(f"""
            니가 작성한 포스트는 {self.state.score.reason} 때문에 SEO(검색엔진 최적화)점수가 좋지 않아, {self.state.topic} 에 대한 블로그 포스트를 개선해서 작성해줘.
            
            <blog_post>
            {self.state.blog_post.model_dump_json()}
            <blog_post>

            다음의 research 결과를 이용해서 작성해.

            <research>
            {self.state.research}
            </research>
            """)
            

        if blog_post == "":             #8 ↓
            print("포스트 신규작성.")
        else:                           #9 ↓
            print("포스트 개선필요.")

    
    @listen(or_("make_tweet_post", "rewrite_tweet_post"))
    # 트윗 작성(make_tweet_post)을 AI 에게 요청 하든지, 
    # 이미 작성된 트윗이 작성된 상태(rewrite_tweet_post)라면 AI 에게 보여주고 수정을 요청합니다.
    def handle_make_tweet_post(self):
        print(f"트윗 포스트 작성: {self.state.topic} 에 대해 트윗 포스트를 작성합니다.")
    
    @listen(or_("make_linkedin_post", "rewrite_linkedin_post")) 
    # 링크드인 작성(make_linkedin_post)을 AI 에게 요청 하든지, 
    # 이미 작성된 링크드인이 작성된 상태(rewrite_linkedin_post)라면 AI 에게 보여주고 수정을 요청합니다.
    def handle_make_linkedin_post(self):
        print(f"링크드인 포스트 작성: {self.state.topic} 에 대해 링크드인 포스트를 작성합니다.")

    @listen(handle_make_blog_post)
    def check_seo(self):
        print(f"블로그 포스트 SEO 체크: {self.state.topic} 에 대해 SEO 체크를 시작합니다.")
        print(self.state.blog_post)
        print("================================================")
        print(self.state.research)

    
    @listen(or_(handle_make_tweet_post, handle_make_linkedin_post))
    def check_virality(self):
        print(f"트윗 또는 링크드인 포스트 화제성 체크: {self.state.topic} 에 대해 화제성 체크를 시작합니다.")

    @router(or_(check_seo, check_virality)) 
    def score_router(self):                 
        content_type = self.state.content_type 
        score = self.state.score 

        if score  > 8:            
            return "content_passed"
        else:
            if content_type == "blog":
                return "rewrite_blog_post"
            elif content_type == "tweet":
                return "rewrite_tweet_post"
            elif content_type == "linkedin":
                return "rewrite_linkedin_post"
            else:
                raise ValueError("유효하지 않은 컨텐츠 입니다.")

    @listen("content_passed") 
    def complete_content_pipeline(self):
        print(f"컨텐츠 파이프라인 완료: {self.state.topic} 에 대해 컨텐츠 파이프라인을 완료합니다.")
    

flow = ContentPipelineFlow()

# flow.plot() #17
flow.kickoff( # 18
    inputs={
        "content_type": "blog",
        "topic": "AI and Job Security",
    }
)
