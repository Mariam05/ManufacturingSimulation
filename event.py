from component import *
class Event():
    def __init__(self, arrival_time:float,  type: int, target_wst: int, component: Component, insp_id: int) -> None:
        self.type = type # 1 = arrival and 2 = departure
        self.target_wst = target_wst
        self.component = component
        self.arrival_time = arrival_time
        self.source = insp_id # which inspector initiated it

    # def toString(self):
    #     return (self.arrival_time, self.type, self.)