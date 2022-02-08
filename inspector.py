from typing import List
from component import *
from buffer import *
from util import *
from event import *
from random import randint

class Inspector():
    def __init__(self, id: int, components: List[Component], buffers: List[Buffer]):
        self.id = id
        self.components = components # the components it's responsible for
        self.idle = True # is it inspecting a component
        self.blocked = False
        self.buffers = buffers

    def create_arrival_event(self, clock):
        comp = self.__get_component()
        insp_time = comp.get_next_service_time()
        return Event(insp_time + clock, arrival, None, comp, self)

    def __get_component(self) -> Component:
        num = len(self.components)
        rand_option = randint(0, num - 1)
        return self.components[rand_option]

    def is_blocked(self) -> bool:
        ''' Check if there's space in the buffers for the next component '''
        for comp in self.components:
            if not comp.check_space_in_buffers():
                return True
        return False