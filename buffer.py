class Buffer():
    def __init__(self, comp_type: int, wst_id: int):
        self.CAPACITY = 2 # the number of components that can fit in the queue
        self.size = 0 # the number of components in the queue
        self.component_type = comp_type # what kind of component it holds
        self.wait_times = [] # how long a component waited in the buffer. the size of this list should be the amount of components that went into the buffer. 
        self.wst_id = wst_id # the workstation that the buffer belongs to
        self.running_capacity = 0

    def is_full(self) -> bool:
        ''' Determines if there's space in the buffer '''
        if self.size < self.CAPACITY:
            return False
        return True

    def is_empty(self) -> bool:
        ''' Return true if the buffer is empty '''
        if self.size > 0:
            return False
        return True

    def add_to_buffer(self):
        ''' Add a component to the buffer '''
        self.size += 1
        if self.size > 2:
            raise Exception("buffer is overflowing")

    def remove_from_buffer(self):
        ''' Remove a component from the buffer '''
        self.size -= 1

    def update_capacity(self):
        ''' To be called with every event '''
        self.running_capacity += self.size