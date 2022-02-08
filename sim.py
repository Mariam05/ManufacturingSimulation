import queue
from random import randint
from typing import List

from servicetime_util import ServiceTimes # to use to get the next service time. 
import logging
from util import *

from workstation import Workstation
from buffer import Buffer
from component import *
from inspector import *


'''
Format of events is (time, type (arrival vs departure), target workstation, component_type)
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


    def scheduleArrival(self, inspector: Inspector):
        """ create arrival event to buffer """ 
        
        inspector_id = inspector.id
        logging.info("Scheduling arrival for inspector %d", inspector_id)
        inspector.idle = False
        evt = inspector.create_arrival_event(self.Clock)

        self._FutureEventList.put((evt.arrival_time, evt))
        print("added event to FEL: ", evt)


    def determine_target(self, comp_id: int):
        ''' Determine which buffer to add the component to '''
          
        if (comp_id == 1):
            c1_buffers = list(self.buffers.get(1).items())
            c1_buffers.sort(key= lambda x: (x[1], x[0]))
            return c1_buffers[0][0] # first tuple in list, first element in tuple = workstation id

        return comp_id
      

    def processArrival(self, evt: Event):
        ''' When a component arrives to a buffer. '''

        comp = evt.component
        buffer_entered = comp.enter_buffer()

        insp = evt.source
        insp.idle = True
        
        # comp_id = evt.component.type
        # if (comp_id == 1):
        #     self.inspector_idle[1] = True
        # else:
        #     self.inspector_idle[2] = True

        # # determine which buffer to put it in. target_buffer actually has which workstation to put it in
        # target_buffer = self.determine_target(comp_id) 

        logging.info("processing arrival to buffer in workstation %d", buffer_entered.wst_id)
        
        # increase number of components in queue
        # self.buffers.get(comp_id)[target_buffer] += 1 

  
    def schedule_departure(self, workstation: Workstation):
        ''' Move components to the workstation and schedule their departure '''

        workstation_id = workstation.id
        logging.info(" workstation %d: Components entering workstation. Scheduling departure.", workstation_id)

        evt = workstation.schedule_departure(self.Clock)
        # self.workstations_idle[workstation_id] = False

        # if workstation_id == 1:
        #     self.buffers.get(1)[1] -= 1 # decrease number of components in buffer 1, wst 1
            
        #     dept_time = self.Clock + self.service_time.get_W1_service_time()
            
        # elif workstation_id == 2:
        #     self.buffers.get(1)[2] -= 1
        #     self.buffers.get(2)[2] -= 1
        #     dept_time = self.Clock + self.service_time.get_W2_service_time()
            
        # else: 
        #     self.buffers.get(1)[3] -= 1
        #     self.buffers.get(3)[3] -= 1
        #     dept_time = self.Clock + self.service_time.get_W3_service_time()

        # evt = (dept_time, self._departure, workstation_id, None)

        self._FutureEventList.put(evt)
        self.products_scheduled += 1


    # def check_workstation_available(self, workstation_id: int) -> bool:
    #     ''' Determine if a workstation can start processing a product '''

    #     is_idle = self.workstations_idle.get(workstation_id)
    #     if not is_idle:
    #         return False

    #     if workstation_id == 1 and self.buffers.get(1).get(1) > 0 :
    #         logging.info("Workstation 1 is available")
    #         return True
    #     elif workstation_id == 2 and self.buffers.get(1).get(2) > 0 and self.buffers.get(2).get(2) > 0:
    #         logging.info("Workstation 2 is available")
    #         return True
    #     elif workstation_id == 3 and self.buffers.get(1).get(3) > 0 and self.buffers.get(3).get(3) > 0:
    #         logging.info("Workstation 3 is available")
    #         return True

    #     return False
        

    def processDeparture(self, evt: Event):
        ''' Departure from the workstation'''


        workstation = evt.target_wst
        workstation_id = workstation.id
        # update workstation to idle    
        workstation.process_departure()
        logging.info("Product is departing from workstation %d", workstation_id)

        if (workstation_id == 1):
            self.components_consumed += 1
        else:
            self.components_consumed += 2
         


logging_setup()

c1 = Component(1, "data/servinsp1.dat")
c2 = Component(1, "data/servinsp22.dat")
c3 = Component(1, "data/servinsp23.dat")

buffer11 = Buffer(1, 1)
buffer12 = Buffer(1, 2)
buffer13 = Buffer(1, 3)
buffer22 = Buffer(2, 2)
buffer33 = Buffer(3, 3)


insp1 = Inspector(id=1, components=[c1])
insp2 = Inspector(id =1, components=[c2, c3])

w1 = Workstation(1, [buffer11], "data/ws1.dat")
w2 = Workstation(1, [buffer12, buffer22], "data/ws2.dat")
w3 = Workstation(1, [buffer13, buffer33], "data/ws3.dat")

workstations = [w1, w2, w3]

sim = Sim()

sim.scheduleArrival(insp1)
# sim.scheduleArrival(2)

i = 0
while sim.components_inspected > sim.components_consumed :
    print(i)
    i += 1
    print("FEL: ", sim._FutureEventList.queue)
    print("buffers: ", sim.buffers)

    for wst in workstations:
        sim.schedule_departure(wst)

    if not sim._FutureEventList.empty():
        evt = sim._FutureEventList.get()

        sim.Clock = evt[0]

        logging.info("event being processed: %s", str(evt))
        logging.info("time is: %f", sim.Clock)

        event = evt[1]

        if (evt[1] == sim._arrival): # arrival to buffer 
            sim.processArrival(event)
        elif (evt[1] == sim._departure): # departure from workstation
            sim.processDeparture(event)
   
    
    if not insp1.is_blocked():
        sim.scheduleArrival(1)

    # if not sim.block_inspector(2):
    #     sim.scheduleArrival(2)

    # """check event type"""
    print("Total components inspected = ", sim.components_inspected)
    print("Total components consumed = ", sim.components_consumed)
    print("Total products scheduled = ", sim.products_scheduled)


print("Total components inspected = ", sim.components_inspected)
print("Total products scheduled = ", sim.products_scheduled)
print("Num Skipped = ", sim.num_skipped)
