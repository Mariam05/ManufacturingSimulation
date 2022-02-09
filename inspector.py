from typing import List
from component import *
from buffer import *
from util import *
from random import randint

class Inspector():
    def __init__(self, id: int, components: List[Component]):
        self.id = id
        self.components = components # the components it's responsible for
        self.idle = True # is it inspecting a component
        self.blocked = False

    def create_arrival_event(self, clock):
        comp = self.__get_component()
        insp_time = comp.get_next_service_time()
        if (insp_time == None):
            self.blocked = True
            return
        return (insp_time + clock, arrival, None, comp.type, self.id)

    def __get_component(self):
        num = len(self.components)
        rand_option = randint(0, num - 1)
        return self.components[rand_option]

    def is_blocked(self) -> bool:
        ''' Check if there's space in the buffers for the next component '''
        for comp in self.components:
            if not comp.check_space_in_buffers():
                return True
        return False