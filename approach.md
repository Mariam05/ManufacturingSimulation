- at time x: 
  - arrival of C1 to inspector 1 
    - check which buffer we're adding the component to. 
    - If a buffer is full, don't accept arrival. else, determine which buffer to add to. 
    - add to FEL the departure of C1 =  arrival of C1 into the determined buffer
  - arrival of either C2 or C3 to inspector 2 
    - add to FEL the departure of C
    - 

- take next event in FEL:
  - if it's an arrival to buffer, then check if workstation can process it (if it's B1, then yes. If it's B2 or B3, check if the other buffer has an element)
  - if workstation is free, it will take the next one in the waiting queue (ie. buffer)

ArrivalToBuffer11, C1 => workstation1, C1
ArrivalToBuffer21, C1 => workstation2, C1
ArrivalToBuffer31, C1 => workstation3, C1
ArrivalTOBuffer22, C2 => workstation2, C2
ArrivalToBuffer33, C3 => workstation3, C3

Variables:
- one for each buffer (int) = # of components currently in buffer
- one for each workstation = whether it's busy or not *might not need
- one for each inspector (bool) = blocked or not.


- one clock will have to be shared between everyone. 
  - ex. Clock = 0. Arrival of C1. FEL = (ArrivalToBuffer11, C1, 10.16).
        Clock = 0. Arrival of C2. FEL = [(ArrivalToBuffer11, C1, 10.16), (ArrivalToBuffer22, C2, 15.24)]
        Clock = 10.16. FEL = [(DepartureFromWorkstation1, C1, 10.16 + 0.85 ), (ArrivalToBuffer11, C1, 10.16 + 13.508)]
