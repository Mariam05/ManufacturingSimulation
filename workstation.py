from buffer import Buffer
from typing import List
from util import *

class Workstation():
    def __init__(self, id: int, buffers: List[Buffer], filename: str) -> None:
        self.id = id
        self.buffers = buffers
        self.idle = True
        self.processing_time = [] # the times that it took to process components. we can add them all up and subtract from the total time to get the idle time
        self.filename = filename # filename with processing
        self.__time_generator = (float(row.rstrip()) for row in open(self.filename)) # generator to get service times

    def get_next_service_time(self):
        ''' Read the next value in the file for C1 service times by Inspector 2 '''
        try:
            nxt = next(self.__time_generator)
        except Exception: # end of file reached
            nxt = None
        return nxt

    def is_available(self) -> bool:
        ''' Returns whether the workstation can start assembling a product '''
        buffer_occupied = [not b.is_empty() for b in self.buffers]
        return all(buffer_occupied) and self.idle

    def schedule_departure(self, clock):  
        ''' Remove components from the buffer and schedule the departure of a product from the workstation '''
        self.idle = False # if a departure is being scheduled, then the workstation is busy
        dept_time = clock + self.get_next_service_time()
        for buffer in self.buffers:
            buffer.remove_from_buffer() # remove the components from the buffer
        evt = (dept_time, departure, self.id, None, None)
        return evt

    def process_departure(self):
        ''' Handles a product leaving the workstation'''
        self.idle = True
        