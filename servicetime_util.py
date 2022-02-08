
class ServiceTimes():
    '''
    Used to get the service time for the next component 
    '''

    def __init__(self):
        self.c1Filename = "data/servinsp1.dat"
        self.c2Filename = "data/servinsp22.dat"
        self.c3Filename = "data/servinsp23.dat"

        self.w1_filename = "data/ws1.dat"
        self.w2_filename = "data/ws2.dat"
        self.w3_filename = "data/ws3.dat"

        self.__c1Generator = (float(row.rstrip()) for row in open(self.c1Filename))
        self.__c2Generator = (float(row.rstrip()) for row in open(self.c2Filename)) # to change to list instead of generator, replace () with []
        self.__c3Generator = (float(row.rstrip()) for row in open(self.c3Filename))

        self.__w1Generator = (float(row.rstrip()) for row in open(self.w1_filename))
        self.__w2Generator = (float(row.rstrip()) for row in open(self.w2_filename))
        self.__w3Generator = (float(row.rstrip()) for row in open(self.w3_filename))

    def get_C1_service_time(self):
        ''' Read the next value in the file for C1 service times by Inspector 2 '''
        try:
            nxt = next(self.__c1Generator)
        except Exception:
            nxt = None
        return nxt

    def get_C2_service_time(self):
        ''' Read the next value in the file for C2 service times by Inspector 2 '''
        return next(self.__c2Generator)

    def get_C3_service_time(self):
        ''' Read the next value in the file for C3 service times by Inspector 2 '''
        return next(self.__c3Generator)

    def get_W1_service_time(self):
        ''' Read the next value in the file for W1 service times '''
        return next(self.__w1Generator)


    def get_W2_service_time(self):
        ''' Read the next value in the file for W2 service times '''
        return next(self.__w2Generator)

    def get_W3_service_time(self):
        ''' Read the next value in the file for W3 service times  '''
        return next(self.__w3Generator)