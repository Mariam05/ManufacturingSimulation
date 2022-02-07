import queue
from random import randint

from numpy import full
from servicetime_util import ServiceTimes # to use to get the next service time. 
import logging
from util import *

'''
Format of events is (time, type (arrival vs departure), target workstation, component_type)
(wst_id, cpt_id)
'''

class Sim():
    def __init__(self):
        # a dictionary to hold the amount of components in the buffers
        # format is {component_type: {workstation: number of components in buffer }}
        self.buffers = {1: {1: 0, 2:0, 3:0}, 
                        2: {2: 0}, 3: {3: 0} } 

        self.maxBufferSize = 2

        # a dictionary to determine whether a workstation is idle 
        self.workstations_idle = {1: False, 2: False, 3: False}

        self.inspector_blocked = {1: False, 2: False}

        self.inspector_responsibilities = {1: 1, 2: 2, 3: 2}

        self.Clock = 0.0

        self._FutureEventList = queue.PriorityQueue()

        self.end = False # indicate whether the simulation has ended. 
        self.service_time = ServiceTimes() # can be used to get the next service time for each inspector & workstation.

        self._arrival = 1
        self._departure = 2


    def scheduleArrival(self, inspector_id):
        """ create arrival event to buffer """ 
        
        logging.info("Scheduling arrival for inspector %d", inspector_id)

        if inspector_id == 1 and not self.inspector_blocked[1]:
            comp_id = 1
            arrivalTime = self.Clock + self.service_time.get_C1_service_time()
        elif inspector_id == 2 and not self.inspector_blocked[2]:
            comp_id = randint(2,3)
            if (comp_id == 2):
                arrivalTime = self.Clock + self.service_time.get_C2_service_time()
            else:
                arrivalTime = self.Clock + self.service_time.get_C3_service_time()
        else:
            return
       
        target_wst = self.determine_target(comp_id)
        evt = (arrivalTime, self._arrival, target_wst, comp_id)

        self._FutureEventList.put(evt)
        print("added event to FEL: ", evt)
        

    def determine_target(self, comp_id: int):
        ''' Determine which buffer to add the component to '''
          
        if (comp_id == 1):
            c1_buffers = list(self.buffers.get(1).items())
            c1_buffers.sort(key= lambda x: (x[1], x[0]))
            return c1_buffers[0][0] # first tuple in list, first element in tuple = workstation id

        return comp_id
      

    def processArrival(self, workstation_id: int, comp_id: int):
        '''
        - Add it to the buffer
        - Check if the workstation can take it. 
        - block / unblock inspectors
        - schedule another arrival
        '''
        
        # increase number of components in queue
        self.buffers.get(comp_id)[workstation_id] += 1 

        wst_available = self.check_workstation_available(workstation_id)

        if wst_available:
            self.schedule_departure(workstation_id)

        # check the status of the buffers and block / unblock inspectors as necessary/
        self.check_buffer_capacities()
        
        self.scheduleArrival(self.inspector_responsibilities[comp_id])


    def check_buffer_capacities(self):
        ''' Check buffers for each component. If all the buffers for one component are full, then block that inspector. '''
        
        for comp_id in self.buffers:
            all_full = True
            buffers = self.buffers.get(comp_id)
            for elem in list(buffers.values()):
                if elem != 2:
                    all_full = False

            inspector_responsible = self.inspector_responsibilities.get(comp_id)

            if all_full: # block the inspector responsible for that component
                self.inspector_blocked[inspector_responsible] = True
                logging.info("Blocking inspector %d", inspector_responsible)
            else:
                if self.inspector_blocked[inspector_responsible] == True:
                    self.inspector_blocked[inspector_responsible] = False
                    logging.info("Unblocking inspector %d", inspector_responsible)
            

    def schedule_departure(self, workstation_id: int):
        ''' Move components to the workstation and schedule their departure '''

        self.workstations_idle[workstation_id] = False

        if workstation_id == 1:
            self.buffers.get(1)[1] -= 1 # decrease number of components in buffer 1, wst 1
            dept_time = self.Clock + self.service_time.get_W1_service_time()
        elif workstation_id == 2:
            self.buffers.get(1)[2] -= 1
            self.buffers.get(2)[2] -= 1
            dept_time = self.Clock + self.service_time.get_W2_service_time()
        else: 
            self.buffers.get(1)[3] -= 1
            self.buffers.get(3)[3] -= 1
            dept_time = self.Clock + self.service_time.get_W3_service_time()

        evt = (dept_time, self._departure, workstation_id, None)

        self._FutureEventList.put(evt)
        print("added departure event to FEL: ", evt)


    def check_workstation_available(self, workstation_id: int) -> bool:
        ''' Determine if a workstation can start processing a product '''

        is_idle = self.workstations_idle.get(workstation_id)
        if not is_idle:
            return False

        if workstation_id == 1:
            logging.info("Workstation 1 is available")
            return True
        elif workstation_id == 2: # buffer for C1, and a buffer for C2
            if self.buffers.get(1).get(2) > 0 and self.buffers.get(2).get(2) > 0:
                logging.info("Workstation 2 is available")
                return True
        else: # buffer for C1, buffer for C3
            if self.buffers.get(1).get(3) > 0 and self.buffers.get(3).get(3) > 0:
                logging.info("Workstation 3 is available")
                return True

        return False
        

    def processDeparture(self, workstation_id: int):
        ''' Departure from the workstation'''

        # update workstation to idle
        self.workstations_idle[workstation_id] = True
        logging.info("Scheduling departure of product from workstation")



        # check if it can create another product. 

        
        """ if there are still Components in queue, schedule next departure"""    


logging_setup()
sim = Sim()

""" schedule first arrival for inspector 1. event is identified by a tuple (time, type, queue ID, Component)"""
""" Inspector 1 = 1, inspector2 = 2"""
sim.scheduleArrival(1)
# sim.scheduleArrival(2)

while not sim._FutureEventList.empty():
    print("FEL: ", sim._FutureEventList.queue)
    evt = sim._FutureEventList.get()

    sim.Clock = evt[0]

    logging.info("event being processed: %s", str(evt))
    logging.info("time is: %f", sim.Clock)

    target_workstation = evt[2]
    comp_type = evt[3]

    """ check event type"""
    if (evt[1] == sim._arrival): # arrival to buffer 
        sim.processArrival(target_workstation, comp_type)
    elif (evt[1] == sim._departure): #departure from workstation
        sim.processDeparture(target_workstation)

logging.info("Future event list is empty")

