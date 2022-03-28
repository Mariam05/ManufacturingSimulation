from typing import List
from buffer import *
from util import *
from random import randint
import csv

class Inspector():
    def __init__(self, id: int, buffers: List[Buffer]):
        self.id = id
        self.idle = True # is it inspecting a component
        self.buffers = buffers
        self.done = False # indicates whether the inspector finished inspecting all components (used only for this iteration)
        self.processing_time = []
    
    def determine_target(self) -> Buffer:
        ''' Determine which buffer to add the component to '''

        # sort the buffers list first by the size of the buffer and then by the workstation id
        self.buffers.sort(key= lambda b: (b.size, b.wst_id))  
        return self.buffers[0] # return the first buffer in list (highest priority)
    
    def add_to_buffer(self):
        ''' Finish inspecting a component, add it to a bugger '''
        self.idle = True # set self to idle, so that it can start processing another component
        target_buffer = self.determine_target() # determine which buffer to place the component in
        target_buffer.add_to_buffer() # add the component to that buffer

    def proportion_of_time_idle(self, clock):
        service_time = 0; 
        for t in self.processing_time:
            service_time += t
            
        print("service time:  ", service_time, " Clock = " , clock)
        idle_time = (clock - service_time)/clock
        return idle_time
    
    def is_blocked(self) -> bool:
        ''' Determine whether or not the inspector can start processing another component. 
        An inspector can't process another component if it's blocked or busy'''
        if not self.idle: # if it's currently processing a component, then return True 
            return True

        for buffer in self.buffers:
            if not buffer.is_full(): # if there's space in a target buffer, return false
                return False
        return True

class Inspector1(Inspector):
    def __init__(self, buffers: List[Buffer]):
        Inspector.__init__(self,1, buffers)
        self.__c1Filename = "data-rv/servinsp1.dat"
        self.__c1Generator = (float(row.rstrip()) for row in open(self.__c1Filename)) # a generator to read the service times

    def get_next_service_time(self):
        ''' Read the next value in the file for C1 service times by Inspector 2 '''
        try:
            nxt = next(self.__c1Generator)
        except Exception: # an exception is thrown after the last service time is read
            nxt = None
            self.done = True
        return nxt

    def create_arrival_event(self, clock):
        ''' Creates an event tuple that indicates what component the inspector is inspecting and 
        when the inspector will finish inspecting it. (ie. when it will arrive to a buffer). 
        The clock parameter is the current simulation time. '''
        insp_time = self.get_next_service_time()
        if (insp_time == None):
            self.blocked = True
            return
        self.processing_time.append(insp_time)
        write_to_csv("quantities-data/insp1.csv",[insp_time, clock, clock+insp_time])
        return (insp_time + clock, arrival, None, 1, self.id)


class Inspector2(Inspector):
    def __init__(self, buffers: List[Buffer]):
        Inspector.__init__(self,2, buffers)
        self.__c2Filename = "data-rv/servinsp22.dat"
        self.__c3Filename = "data-rv/servinsp23.dat"
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
        ''' Creates an event tuple that indicates what component the inspector is inspecting and 
        when the inspector will finish inspecting it. (ie. when it will arrive to a buffer). 
        The clock parameter is the current simulation time. '''
        chosen_comp = randint(2, 3) # randomly determine whether the inspector will inspect C2 or C3
        if chosen_comp == 2:
            insp_time = self.get_next_C2_service_time()
        else:
            insp_time = self.get_next_C3_service_time()

        if (insp_time == None):
            self.blocked = True
            return
        self.processing_time.append(insp_time)
        write_to_csv("quantities-data/insp2.csv",[insp_time, clock, clock+insp_time])

        return (insp_time + clock, arrival, None, 1, self.id)
