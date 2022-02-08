from typing import List
from buffer import *

class Component():
    def __init__(self, type: int, filename: str, buffers: List[Buffer]) -> None:
        self.type = type # 1, 2, or 3
        self.filename = filename # the filename that holds its service times
        self.__time_generator = (float(row.rstrip()) for row in open(self.filename))
        self.buffers = buffers

    def get_next_service_time(self):
        ''' Read the next value in the file for C1 service times by Inspector 2 '''
        try:
            nxt = next(self.__time_generator)
        except Exception:
            nxt = None
        return nxt

    def check_space_in_buffers(self) -> bool:
        ''' Return true if there space in it's buffers. False otherwise. '''
        for buffer in self.buffers:
            if not buffer.is_full():
                return True
        return False

    def determine_target(self) -> Buffer:
        # c1_buffers = list(self.buffers.get(1).items())
        self.buffers.sort(key= lambda b: (b.size, b.wst_id))
        return self.buffers[0] # first tuple in list, first element in tuple = workstation id
    
    def enter_buffer(self):
        target = self.determine_target()
        target.add_to_buffer()
        return target
        