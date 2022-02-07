import queue
from random import randint
import sys

from matplotlib.style import available

#from numpy import full
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

        self.insp_comps = {1: [1], 2: [2,3]}
        self.maxBufferSize = 2

        # a dictionary to determine whether a workstation is idle 
        self.workstations_idle = {1: True, 2: True, 3: True}

        self.inspector_blocked = {1: False, 2: False}

        self.inspector_idle = {1: True, 2: True}

        self.inspector_responsibilities = {1: 1, 2: 2, 3: 2} # component: inspector

        self.Clock = 0.0

        self._FutureEventList = queue.PriorityQueue()

        self.service_time = ServiceTimes() # can be used to get the next service time for each inspector & workstation.

        self._arrival = 1
        self._departure = 2

        self.components_inspected = 0
        self.components_consumed = 0

        self.products_scheduled = 0
        self.num_skipped = 0



    def scheduleArrival(self, inspector_id):
        """ create arrival event to buffer """ 
        
        logging.info("Scheduling arrival for inspector %d", inspector_id)

        self.inspector_idle[inspector_id] = False

        arrivalTime = None
        if inspector_id == 1:
            comp_id = 1
            arrivalTime = self.service_time.get_C1_service_time()
        elif inspector_id == 2 and not self.inspector_blocked[2]:
            comp_id = randint(2,3)
            if (comp_id == 2):
                arrivalTime = self.service_time.get_C2_service_time()      
            else:
                arrivalTime = self.service_time.get_C3_service_time()             
        
        if arrivalTime == None:
            self.num_skipped += 1
            return

        arrivalTime += self.Clock

        self.components_inspected += 1

        evt = (arrivalTime, self._arrival, None, comp_id)

        self._FutureEventList.put(evt)
        print("added event to FEL: ", evt)
        

    def block_inspector(self, insp_id) -> bool:
        if not self.inspector_idle.get(insp_id):
            return True

        insp_comps = self.insp_comps.get(insp_id) # get the list of components that the inspector is responsible for
        print(f"inspector {insp_id} is responsible for {insp_comps}")
        for comp in insp_comps:
            buffers = self.buffers.get(comp)
            print(f"buffers in comp {comp} are: {buffers}")
            for elem in list(buffers.values()):
                print(f"elem = {elem}")
                if elem < 2:
                    return False
        
        return True


    def determine_target(self, comp_id: int):
        ''' Determine which buffer to add the component to '''
          
        if (comp_id == 1):
            c1_buffers = list(self.buffers.get(1).items())
            c1_buffers.sort(key= lambda x: (x[1], x[0]))
            return c1_buffers[0][0] # first tuple in list, first element in tuple = workstation id

        return comp_id
      

    def processArrival(self, comp_id: int):
        '''
        - Add it to the buffer
        - Check if the workstation can take it. 
        - block / unblock inspectors
        - schedule another arrival
        '''

        if (comp_id == 1):
            self.inspector_idle[1] = True

        # determine which buffer to put it in. target_buffer actually has which workstation to put it in
        target_buffer = self.determine_target(comp_id) 

        logging.info("processing arrival to buffer in workstation %d", target_buffer)
        
        # increase number of components in queue
        self.buffers.get(comp_id)[target_buffer] += 1 

  
    def schedule_departure(self, workstation_id: int):
        ''' Move components to the workstation and schedule their departure '''

        logging.info(" workstation %d: Components entering workstation. Scheduling departure.", workstation_id)
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
        self.products_scheduled += 1
        print("added departure event to FEL: ", evt)


    def check_workstation_available(self, workstation_id: int) -> bool:
        ''' Determine if a workstation can start processing a product '''

        is_idle = self.workstations_idle.get(workstation_id)
        if not is_idle:
            return False

        if workstation_id == 1 and self.buffers.get(1).get(1) > 0 :
            logging.info("Workstation 1 is available")
            return True
        elif workstation_id == 2 and self.buffers.get(1).get(2) > 0 and self.buffers.get(2).get(2) > 0:
                logging.info("Workstation 2 is available")
                return True
        elif workstation_id == 3 and self.buffers.get(1).get(3) > 0 and self.buffers.get(3).get(3) > 0:
            logging.info("Workstation 3 is available")
            return True

        return False
        

    def processDeparture(self, workstation_id: int):
        ''' Departure from the workstation'''

        # update workstation to idle
        self.workstations_idle[workstation_id] = True
        logging.info("Product is departing from workstation %d", workstation_id)

        if (workstation_id == 1):
            self.components_consumed += 1
        else:
            self.components_consumed += 2
         


logging_setup()
sim = Sim()

""" schedule first arrival for inspector 1. event is identified by a tuple (time, type, queue ID, Component)"""
""" Inspector 1 = 1, inspector2 = 2"""

sim.scheduleArrival(1)

#sim.scheduleArrival(2)

i = 0
while sim.components_inspected >= sim.components_consumed :
    print(i)
    i += 1
    print("FEL: ", sim._FutureEventList.queue)
    print("buffers: ", sim.buffers)

    for w_id in range(1,4):
        if sim.check_workstation_available(w_id):
            sim.schedule_departure(w_id)

    
    if sim.buffers.get(1).get(2) > 2 or sim.buffers.get(1).get(3) > 2:
        print("exceeding buffer size")
        break

    if not sim._FutureEventList.empty():
        evt = sim._FutureEventList.get()

        sim.Clock = evt[0]

        logging.info("event being processed: %s", str(evt))
        logging.info("time is: %f", sim.Clock)

        target_workstation = evt[2]
        comp_type = evt[3]

        if (evt[1] == sim._arrival): # arrival to buffer 
            sim.processArrival(comp_type)
        elif (evt[1] == sim._departure): # departure from workstation
            sim.processDeparture(target_workstation)
   
    
    if not sim.block_inspector(1):
        print("inspector not blocked")
        sim.scheduleArrival(1)  

    # """check event type"""
    print("Total components inspected = ", sim.components_inspected)
    print("Total products scheduled = ", sim.products_scheduled)


print("Total components inspected = ", sim.components_inspected)
print("Total products scheduled = ", sim.products_scheduled)
print("Num Skipped = ", sim.num_skipped)
