import queue
from typing import Dict, List

import logging
from util import *

from workstation import Workstation
from buffer import Buffer
from inspector import *


'''
Format of events is (time, type (arrival vs departure), target workstation, component_type, inspector_id)
'''

class Sim():
    '''
    The simulation class to coordinate the arrival and departure of components from the different entities.
    '''

    def __init__(self, inspectors: Dict[int, Inspector], workstations: Dict[int, Workstation]):
        self.inspectors = inspectors
        self.workstations = workstations

        self.Clock = 0.0

        self._FutureEventList = queue.PriorityQueue()

        # variables to hold operation statistics
        self.components_inspected = 0
        self.components_consumed = 0
        self.products_produced = 0
        self.product1_produced=0; 
        self.product2_produced=0; 
        self.product3_produced=0; 


        self.total_comp_in_buffers = 0


    def scheduleArrival(self, inspector: Inspector):
        """ create arrival event to buffer """ 
        
        inspector_id = inspector.id
        logging.info("Scheduling arrival for inspector %d", inspector_id)
        inspector.idle = False
        evt = inspector.create_arrival_event(self.Clock)

        if not evt == None:
            self.components_inspected += 1
            self._FutureEventList.put(evt)
            print("added event to FEL: ", evt)


    def processArrival(self, evt: tuple):
        ''' When a component arrives to a buffer. '''

        insp_id = evt[4]
        insp = self.inspectors.get(insp_id)

        insp.add_to_buffer()
        
        logging.info("processing arrival to buffer in workstation ")

  
    def schedule_departure(self, workstation: Workstation):
        ''' Move components to the workstation and schedule their departure '''

        workstation_id = workstation.id
        logging.info(" workstation %d: Components entering workstation. Scheduling departure.", workstation_id)

        evt = workstation.schedule_departure(self.Clock)
      
        self._FutureEventList.put(evt)

    def processDeparture(self, evt: tuple):
        ''' Process a departure from the workstation'''

        workstation_id = evt[2]
       
        workstation = self.workstations.get(workstation_id)
      
        workstation.process_departure()
        logging.info("Product is departing from workstation %d", workstation_id)

        self.products_produced += 1
        if (workstation_id == 1):
            self.product1_produced+=1 
            self.components_consumed += 1
        elif (workstation_id == 2):
            self.product2_produced+=1
            self.components_consumed += 2
        else:
            self.product3_produced+=1
            self.components_consumed += 2
         
    def check_buffer_sizes(self):
        for buffer in all_buffers:
            self.total_comp_in_buffers += buffer.size


# setup a custom logging format
logging_setup()


# while # of replications
    # reset everything

# initialize all components
buffer11 = Buffer(1, 1)
buffer12 = Buffer(1, 2)
buffer13 = Buffer(1, 3)
buffer22 = Buffer(2, 2)
buffer33 = Buffer(3, 3)

all_buffers = [buffer11, buffer12, buffer13, buffer22, buffer33]

insp1 = Inspector1(buffers=[buffer11, buffer12, buffer13])
insp2 = Inspector2(buffers=[buffer22, buffer33])

w1 = Workstation(1, [buffer11], "data-rv/ws1.dat")
w2 = Workstation(2, [buffer12, buffer22], "data-rv/ws2.dat")
w3 = Workstation(3, [buffer13, buffer33], "data-rv/ws3.dat")

workstations = [w1, w2, w3]

sim = Sim(inspectors={1: insp1, 2: insp2}, 
            workstations={1: w1, 2: w2, 3: w3})

# start the inspectors
sim.scheduleArrival(insp1)
sim.scheduleArrival(insp2)

i = 0
end = False
num_of_events = 0

while not end :
    print(i)
    i += 1
    print("FEL: ", sim._FutureEventList.queue)
    print(f"buffers: \n \t  W1B1: {buffer11.size} , W2B1: {buffer12.size}, W2B2: {buffer22.size}, W3B1: {buffer13.size}, W3B3: {buffer33.size} ")

    # for each workstation, check if it can start processing a product
    for wst in workstations:
        if wst.is_available():
            sim.schedule_departure(wst)

    # process the next event in the FEL
    if not sim._FutureEventList.empty():
        evt = sim._FutureEventList.get()

        # check buffer capacities. create a variable that keeps track of number of events
        sim.check_buffer_sizes()
        num_of_events += 1

        sim.Clock = evt[0]

        logging.info("event being processed: %s", str(evt))
        logging.info("time is: %f", sim.Clock)

        if (evt[1] == arrival): # arrival to buffer 
            sim.processArrival(evt)
        elif (evt[1] == departure): # departure from workstation
            sim.processDeparture(evt)
   
    # schedule the next arrival of a component to the buffer if the inspector isn't blocked
    if not insp1.is_blocked():
        sim.scheduleArrival(insp1)

    if not insp2.is_blocked():
        sim.scheduleArrival(insp2)

    # the simulation ends if either both inspectors are done, or one is done and the other is blocked
    end = (insp1.done and insp2.done) or (insp1.done and insp2.is_blocked()) or (insp2.done and insp1.is_blocked())
    print("Total components inspected = ", sim.components_inspected)
    print("Total components consumed = ", sim.components_consumed)
    print("Average buffer capacity = ", sim.total_comp_in_buffers / num_of_events /5 )
    print("products produced: ", sim.products_produced )
    print("Average product throughput = ", sim.products_produced / sim.Clock )
    print("product 1 produced: ", sim.product1_produced )
    print("Average product 1 throughput = ", sim.product1_produced / sim.Clock )
    print("product 2 produced: ", sim.product2_produced )
    print("Average product 2 throughput = ", sim.product2_produced / sim.Clock )
    print("product 3 produced: ", sim.product3_produced )
    print("Average product 3 throughput = ", sim.product3_produced / sim.Clock )
    print("Workstation 1 proportion of time busy: ", sim.workstations.get(1).get_proportion_idle_time(sim.Clock) )
    print("Workstation 2 proportion of time busy: ", sim.workstations.get(2).get_proportion_idle_time(sim.Clock) )
    print("Workstation 3 proportion of time busy: ", sim.workstations.get(3).get_proportion_idle_time(sim.Clock) )





