import inspect
import queue
from random import randint
from typing import Dict, List

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
    def __init__(self, inspectors: Dict[int, Inspector], workstations: Dict[int, Workstation], components: Dict[int, Component]):
        self.inspectors = inspectors
        self.workstations = workstations
        self.components = components

        self.Clock = 0.0

        self._FutureEventList = queue.PriorityQueue()

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

        self.components_inspected += 1

        self._FutureEventList.put(evt)
        print("added event to FEL: ", evt)


    def processArrival(self, evt: tuple):
        ''' When a component arrives to a buffer. '''

        comp_id = evt[3]
        comp = self.components.get(comp_id)
        buffer_entered = comp.enter_buffer()

        insp_id = evt[4]
        insp = self.inspectors.get(insp_id)

        # insp = evt[4] # the inspector
        insp.idle = True
        
        logging.info("processing arrival to buffer in workstation %d", buffer_entered.wst_id)

  
    def schedule_departure(self, workstation: Workstation):
        ''' Move components to the workstation and schedule their departure '''

        workstation_id = workstation.id
        logging.info(" workstation %d: Components entering workstation. Scheduling departure.", workstation_id)

        evt = workstation.schedule_departure(self.Clock)
      
        self._FutureEventList.put(evt)



    def processDeparture(self, evt: tuple):
        ''' Departure from the workstation'''


        workstation_id = evt[2]
        print("evt = ", evt)
        print("")
        workstation = self.workstations.get(workstation_id)
        # update workstation to idle
        # 
        # workstation = evt[2]
        # print("evt[2] = ", workstation)
        # workstation_id = workstation.id    
        workstation.process_departure()
        logging.info("Product is departing from workstation %d", workstation_id)

        if (workstation_id == 1):
            self.components_consumed += 1
        else:
            self.components_consumed += 2
         


logging_setup()


buffer11 = Buffer(1, 1)
buffer12 = Buffer(1, 2)
buffer13 = Buffer(1, 3)
buffer22 = Buffer(2, 2)
buffer33 = Buffer(3, 3)

c1 = Component(1, "data/servinsp1.dat", [buffer11, buffer12, buffer13])
c2 = Component(1, "data/servinsp22.dat", [buffer22])
c3 = Component(1, "data/servinsp23.dat", [buffer33])


insp1 = Inspector(id=1, components=[c1])
insp2 = Inspector(id =1, components=[c2, c3])

w1 = Workstation(1, [buffer11], "data/ws1.dat")
w2 = Workstation(1, [buffer12, buffer22], "data/ws2.dat")
w3 = Workstation(1, [buffer13, buffer33], "data/ws3.dat")

workstations = [w1, w2, w3]

sim = Sim(inspectors={1: insp1, 2: insp2}, 
            workstations={1: w1, 2: w2, 3: w3},
            components={1: c1, 2: c2, 3: c3})

sim.scheduleArrival(insp1)
# sim.scheduleArrival(2)

i = 0
while True :
    print(i)
    i += 1
    # print("FEL: ", sim._FutureEventList.queue)

    for wst in workstations:
        sim.schedule_departure(wst)

    if not sim._FutureEventList.empty():
        evt = sim._FutureEventList.get()

        sim.Clock = evt[0]

        logging.info("event being processed: %s", str(evt))
        logging.info("time is: %f", sim.Clock)

        if (evt[1] == arrival): # arrival to buffer 
            sim.processArrival(evt)
        elif (evt[1] == departure): # departure from workstation
            sim.processDeparture(evt)
   
    
    if not insp1.is_blocked():
        sim.scheduleArrival(insp1)

    # if not sim.block_inspector(2):
    #     sim.scheduleArrival(2)

    # """check event type"""
    print("Total components inspected = ", sim.components_inspected)
    print("Total components consumed = ", sim.components_consumed)


print("Total components inspected = ", sim.components_inspected)
print("Total products scheduled = ", sim.products_scheduled)
print("Num Skipped = ", sim.num_skipped)
