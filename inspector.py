from typing import List
from buffer import *
from util import *
from random import randint

class Inspector():
    def __init__(self, id: int, buffers: List[Buffer]):
        self.id = id
        self.idle = True # is it inspecting a component
        self.buffers = buffers
        self.done = False
    
    def determine_target(self) -> Buffer:
        self.buffers.sort(key= lambda b: (b.size, b.wst_id))
        return self.buffers[0] # first tuple in list, first element in tuple = workstation id
    
    def add_to_buffer(self):
        self.idle = True
        target_buffer = self.determine_target()
        target_buffer.add_to_buffer()

class Inspector1(Inspector):
    def __init__(self, buffers: List[Buffer]):
        Inspector.__init__(self,1, buffers)
        self.__c1Filename = "data/servinsp1.dat"
        self.__c1Generator = (float(row.rstrip()) for row in open(self.__c1Filename))

    def get_next_service_time(self):
        ''' Read the next value in the file for C1 service times by Inspector 2 '''
        try:
            nxt = next(self.__c1Generator)
        except Exception:
            nxt = None
            self.done = True
        return nxt

    def create_arrival_event(self, clock):
        insp_time = self.get_next_service_time()
        if (insp_time == None):
            self.blocked = True
            return
        return (insp_time + clock, arrival, None, 1, self.id)

    def is_blocked(self):
        if not self.idle:
            return True

        for buffer in self.buffers:
            if not buffer.is_full():
                return False
        return True


class Inspector2(Inspector):
    def __init__(self, buffers: List[Buffer]):
        Inspector.__init__(self,2, buffers)
        self.__c2Filename = "data/servinsp22.dat"
        self.__c3Filename = "data/servinsp23.dat"
        self.__c2Generator = (float(row.rstrip()) for row in open(self.__c2Filename))
        self.__c3Generator = (float(row.rstrip()) for row in open(self.__c3Filename))

    def get_next_C2_service_time(self):
        ''' Read the next value in the file for C1 service times by Inspector 2 '''
        try:
            nxt = next(self.__c2Generator)
        except Exception:
            nxt = None
            self.done = True
        return nxt

    def get_next_C3_service_time(self):
        ''' Read the next value in the file for C1 service times by Inspector 2 '''
        try:
            nxt = next(self.__c3Generator)
        except Exception:
            nxt = None
            self.done = True
        return nxt

    def create_arrival_event(self, clock):
        chosen_comp = randint(2, 3)
        if chosen_comp == 2:
            insp_time = self.get_next_C2_service_time()
        else:
            insp_time = self.get_next_C3_service_time()

        if (insp_time == None):
            self.blocked = True
            return
        return (insp_time + clock, arrival, None, 1, self.id)

    def is_blocked(self) -> bool:
        if not self.idle:
            return True
        for buffer in self.buffers:
            if buffer.is_full():
                return True
        return False
