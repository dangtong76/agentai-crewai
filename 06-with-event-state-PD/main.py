from crewai.flow.flow import Flow, listen, start, router, and_, or_
from pydantic import BaseModel
import time

class MyState(BaseModel):
    user_id: int = 1
    is_admin: bool = False

class FirstFlow(Flow[MyState]):
    @start()
    def first_step(self):
        print(self.state.user_id)
        print('Hello')

    @listen(first_step)
    def second_step(self):
        MyState.is_admin = True
        MyState.user_id = 2
        print('World')

    @listen(first_step)
    def third_step(self):
        print('!')

    @listen(and_(second_step, third_step))
    def final_step(self):
        print('CrewAI')
    
    @router(final_step)
    def route(self):
        if MyState.user_id :
            return 'admin' # emit event 'even'
        elif MyState.user_id == False:
            return 'normal-user' # emit event 'odd'
        else:
            return 'None'
    
    @listen('admin')
    def handle_admin(self):
        print('admin')

    @listen('normal-user')
    def handle_normal_user(self):
        print('normal-user')


flow = FirstFlow()

flow.plot()

flow.kickoff()