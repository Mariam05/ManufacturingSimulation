from component import Component
from typing import List

class Inspector():
    def __init__(self, id: int):
        self.id = id
        self.idle = True
        self.blocked = False    

    def setState(self, state: bool):
        self.idle = state
    

    def block(self):
        self.blocked = True
    
    # could also merge this with previous fn, 
    # but it might be better like this
    def unblock(self):
        self.blocked = False

    def getId(self):
        return self.id

    # def receiveComponent(self, component: Component):
    #     '''
    #     Handle case of when blocked. Set arrival time. If received properly, handle that. time.sleep(x) '''
        
    #     self.curr_component = component


class Inspector1(Inspector):
    def __init__(self, buffer):
        Inspector.__init__(self, 1)
        self.curr_component = None
        self.__c1Filename = "data/servinsp1.dat"
        self.__c1Generator = (row for row in open(self.__c1Filename))

    def getC1ServiceTime(self):
        ''' Read the next value in the file for C1 service times by Inspector 2 '''
        return next(self.__c1Generator)

    def start():
        ''' if not busy, then process next component. Once it's done, add it to buffer.  '''
        pass


class Inspector2(Inspector):
    def __init__(self):
        Inspector.__init__(self, 2)
        self.curr_component = None
        self.__c1Filename = "data/servinsp22.dat"
        self.__c2Filename = "data/servinsp23.dat"
        self.__c1Generator = (row for row in open(self.__c1Filename)) # to change to list instead of generator, replace () with []
        self.__c2Generator = (row for row in open(self.__c2Filename))

    def getC1ServiceTime(self):
        ''' Read the next value in the file for C2 service times by Inspector 2 '''
        return next(self.__c1Generator)

    def getC2ServiceTime(self):
        ''' Read the next value in the file for C3 service times by Inspector 2 '''
        return next(self.__c2Generator)

    def start():
        ''' if not busy, then process next component. Randomly decide which component to use. '''
        pass


