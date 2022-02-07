import queue
from servicetime_util import ServiceTimes # to use to get the next service time. 
class Sim():
    def __init__(self):
        self.buffer_11 = 0
        self.buffer_21 = 0
        self.buffer_22 = 0
        self.buffer_31 = 0
        self.buffer_33 = 0
        
        self._clock = 0

        self._FutureEventList = queue.PriorityQueue()



