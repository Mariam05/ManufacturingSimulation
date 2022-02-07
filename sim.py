import queue
from servicetime_util import ServiceTimes # to use to get the next service time. 
class Sim():
    def __init__(self):
        self.buffer_11 = 0
        self.buffer_21 = 0
        self.buffer_22 = 0
        self.buffer_31 = 0
        self.buffer_33 = 0
        self.maxBufferSize = 2
        self.worstation1_idle = False
        self.worstation2_idle = False
        self.workstation3_idle = False
        self.inspector1_idle = False
        self.inspector2_idle = False
        self.inspector3_idle = False
        self.Clock = 0.0
        self.__Inspector11Filename = "data/servinsp1.dat"
        self.__Inspector1Generator = (row for row in open(self.__Inspector1Filename))

        
        self._clock = 0

        self._FutureEventList = queue.PriorityQueue()

    def scheduleArrival(self, queueID):
        """ create arrival event """ 
        arrivalTime = self._Clock + next(self.__Inspector1Generator)
        comp = (arrivalTime, self._ComponentID)
        if (self._ComponentID ==1):
            self._ComponentID = randint(2,3); 
        else: 
            self._ComponentID = 1
        evt = (arrivalTime, self._arrival, queueID, comp)
        self._FutureEventList.put(evt)

    def processArrival(self, cust, queueID):
        
        """ add Component to Component queue"""
        depart = self._QList[queueID].put(cust, self._Clock)
        
        """ check if the Component needs to start service immediately""" 
        if depart is not None:
            self._FutureEventList.put(depart)          
        
        
    def processDeparture(self, evt, queueID):
        
        """ get the Component """
        cust, depart = self._QList[queueID].get(self._Clock)
        
        """ if there are still Components in queue, schedule next departure"""    
        if depart is not None:
            self._FutureEventList.put(depart)
        
        return cust

sim = Sim()

""" schedule first arrival for inspector 1. event is identified by a tuple (time, type, queue ID, Component)"""
""" Inspector 1 = 0, inspector2 = 1"""
sim.scheduleArrival(0)





