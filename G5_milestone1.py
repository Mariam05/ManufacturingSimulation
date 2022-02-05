#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

SYSC4005 Project Simulation

@author: Sarah Jaber 
@author: Mariam Almalki
@author: Hussain Al-Baidhani
"""

from random import randint
import numpy as np
from scipy.stats import expon
from scipy.stats import norm
import matplotlib.pyplot as plt
import queue
from dataclasses import dataclass, field
from typing import Any

@dataclass(order = True)
class PrioritizedItem:
    priority: float
    item: Any=field(compare = False)

class ComponentQueue(object):

    """ queue length is 2 for buffer queue and 0 for inspector queue """ 
    def __init__(self, queueID, queueMaxLength):
        self._arrival = 1
        self._departure = 2
        self._MeanServiceTime = 3.2
        self._SIGMA = 0.6

        self._QueueLength = 0
        self._QueueLengthTime =[[0, 0.0]]
        self._NumberInService = 0
        self._InService = []
        self._LastEventTime = 0.0
        self._TotalBusy = 0.0
        self._MaxQueueLength = queueMaxLength
        self._SumResponseTime = 0.0
        self._NumberOfDepartures = 0
        self._LongService = 0
        self._TotalComponents = 0
        self._Clock = 0.0
        self._Queue = []
        self._QueueID = queueID
    

    def put(self, comp, clock):
        """ add a component into queue"""
        
        """ update clock"""
        self._Clock = clock    
        
        """ start service if server empty """
        if self._NumberInService == 0:
            self._NumberInService = 1
            self._InService.append(comp)
            depart = self.scheduleDeparture(comp)
            """ add to queue if server busy"""
        else:
            self._Queue.append(comp)
            self._QueueLength += 1
        
            """ update statistics"""
            self._QueueLengthTime.append([self._QueueLength, self._Clock])
            self._TotalBusy += (self._Clock - self._LastEventTime)
            depart = None
                    
            """ Adjust max queue length statistics"""
            """ if the queue is the inspector queue """
            if (self._QueueID == 0 or self._QueueID==1):           
                if (self._MaxQueueLength < self._QueueLength):
                    self._MaxQueueLength = self._QueueLength
            
        self._LastEventTime = self._Clock
        return depart
                       
        
    def get(self, clock):
        
        """ get component from the server of the queue"""
        cust = self._InService.pop(0)
        
        """ update clock"""
        self._Clock = clock
        
        """ if queue is not empty, schedule next departure"""
        if ( self._QueueLength > 0):
            """ move component from queue to service"""
            
            cust1 = self._Queue.pop(0)
            self._InService.append(cust1)
            
            self._QueueLength -= 1
 
            """ schedule departure for head-of-line component"""
            depart = self.scheduleDeparture(cust1)
            self._QueueLengthTime.append([self._QueueLength, self._Clock])
        
        else:
            self._NumberInService = 0
            depart = None
            
        """ update statistics"""
        
        response = clock - cust[0]
        self._SumResponseTime += response
        if response > 4.0:
            self._LongService += 1
        self._TotalBusy += (self._Clock - self._LastEventTime)
        self._NumberOfDepartures += 1
        self._LastEventTime = self._Clock
        self._TotalComponents += 1
        return cust, depart        

    def scheduleDeparture(self, cust):
        ServiceTime = self.getServiceTime()
        depart = (self._Clock + ServiceTime, self._departure, self._QueueID, cust)
        return depart         
        
    def getServiceTime(self):
        """ assume service time follow Normal distribution"""
        ServiceTime = norm.rvs(loc = self._MeanServiceTime, scale = self._SIGMA)
        while (ServiceTime < 0):
            ServiceTime = norm.rvs(loc = self._MeanServiceTime, scale = self._SIGMA)
        return ServiceTime
 
        
    def qReportGeneration(self, clock):
        RHO = self._TotalBusy/clock
        if self._NumberOfDepartures != 0:
            AVGR = self._SumResponseTime/self._NumberOfDepartures
            PC4 = self._LongService/self._NumberOfDepartures
        else: 
            AVGR = 0
            PC4 = 0
        
        print("\n STATISTICS OF QUEUE {}:".format(self._QueueID))
        print("\n MEAN SERVICE TIME: ", self._MeanServiceTime)
        print("\n STANDARD DEVIATION OF SERVICE TIMES: ", self._SIGMA)
        print("\n NUMBER OF ComponentS SERVED: ", self._NumberOfDepartures)
        print("\n SERVER UTILIZATION: {0:.2f}".format(RHO))
        print("\n MAXIMUM LINE LENGTH: ", self._MaxQueueLength)
        print("\n AVERAGE RESPONSE TIME: {0:.2f} MINUTES".format(AVGR))
        print("\n PROPORTION WHO SPEND FOUR MINUTES OR MORE IN SYSTEM: {0:.2f}".format(PC4))
        print("\n SIMULATION RUN LENGTH: {0:.2f} MINUTES".format(self._Clock))
        print("\n NUMBER OF DEPARTURES: ", self._NumberOfDepartures)       
        
        y, x = zip(*self._QueueLengthTime)

        plt.step(x,y, where ='post')
        plt.xlabel("Time (Minutes)")
        plt.ylabel("Queue Length")
        plt.title('Queue Length vs. Time for Queue {}'.format(self._QueueID))
        plt.show()


class Sim(object):
    
    def __init__(self):
        self._arrival = 1
        self._departure = 2
        self._MeanInterArrivalTime = 4.5
        self._TotalComponents = 10
        self._Clock = 0.0
        self._NumberOfSystemDepartures = 0
        """ keep track of the total number of components in the simulation """
        self._ComponentCount = 0 
        """ ComponentID is either 1 , 2 or 3 """
        self._ComponentID = 0
        self._QueueID = 0
        """ one for each inspector and one for W1, two for W2, two for W3"""
        self._NumberOfQueues = 7
        self._QList = []
        
        """ create a future event list"""
        self._FutureEventList = queue.PriorityQueue()
        
        
        """ create FIFO queues for holding components """ 
        """Insepctor 1 = 0, Inspector2 =  1, W1 = 2, W2= C1 3, C2 4, W3 = C1 5 C2 6"""
        for i in range(self._NumberOfQueues):
            self._QList.append(ComponentQueue(self._QueueID))
            self._QueueID += 1


    def scheduleArrival(self, queueID):
        """ create arrival event """ 
        arrivalTime = self._Clock + expon.rvs(scale = self._MeanInterArrivalTime)
        comp = (arrivalTime, self._ComponentID)
        if (self._ComponentID ==1):
            self._ComponentID = randint(2,3); 
        else: 
            self._ComponentID = 1
        evt = (arrivalTime, self._arrival, queueID, cust)
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
    
    def reportSGeneration(self):
        for i in range(self._NumberOfQueues):
            self._QList[i].qReportGeneration(self._Clock)
     
        
""" set seed for random numer generator"""

seed = input('Enter your seed:')

np.random.seed((int(seed)))
               
""" create simulation instance"""
ms = Sim()

""" schedule first arrival for inspector 1. event is identified by a tuple (time, type, queue ID, Component)"""
ms.scheduleArrival(0)
"""schedule first arrival for inspector 2"""
ms.scheduleArrival(1)

while (ms._NumberOfSystemDepartures < ms._TotalComponents):
    """ get imminent event"""
    evt = ms._FutureEventList.get()

    """ update clock"""
    ms._Clock = evt[0]
    #print("Queue ID:", evt)
    
    """ check event type"""
    if ( evt[1] == ms._arrival):
 
        """ get Component info. Component is identified by a tuple (creation time, ComponentID)"""
        cust = evt[3]
        ms.processArrival(cust, 0)
        
        """ schedule next arrival"""
        ms.scheduleArrival(0)            
    else:
        """ process departure at the queue to be left"""
        cust = ms.processDeparture(evt, evt[2])
        
        """ if Component is leaving queue 0, send it to queue 2, 3 or 5 respectively and based on the shortest queue"""
        if (evt[2] == 0):
            length2 = ms._QList[2]._QueueLength
            length3 = ms._QList[3]._QueueLength
            length5 = ms._QList[5]._QueueLength
            min = min(length2,length3, length5)
            if( min == 2):
                """block inspector 1"""
            elif ((ms._QList[2]._QueueLength)==(ms._QList[3]._QueueLength) and (ms._QList[3]._QueueLength) == (ms._QList[4]._QueueLength)): 
                ms.processArrival(cust, 2)
            else: 
                """shortest queue """
                """ms.processArrival(cust, 1)"""
        
        else:
            """ tracking total number of Components leaving the system"""
            ms._NumberOfSystemDepartures += 1
   

ms.reportSGeneration()


