from workstation import *
from component import *


class Event():
    from inspector import Inspector
    def __init__(self, arrival_time:float,  type: int, target_wst: Workstation, component: Component, source: Inspector) -> None:
        self.type = type # 1 = arrival and 2 = departure
        self.target_wst = target_wst
        self.component = component
        self.arrival_time = arrival_time
        self.source = source