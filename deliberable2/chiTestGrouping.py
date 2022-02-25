import csv
import math

servinsp1 = [float(i.strip()) for i in open("servinsp1.dat").readlines()]
servinsp22 = [float(i.strip()) for i in open("servinsp22.dat").readlines()]
servinsp23 = [float(i.strip()) for i in open("servinsp23.dat").readlines()]

ws1 = [float(i.strip()) for i in open("ws1.dat").readlines()]
ws2 = [float(i.strip()) for i in open("ws2.dat").readlines()]
ws3 = [float(i.strip()) for i in open("ws3.dat").readlines()]

minEi = 5

lam = 0.097
n = 300
exp_fn = lambda x: n*lam*math.pow(math.e, -lam*x)

def calc_chi(observed, expected_fn):
    '''
    Returns a tuple (xo^2, k)
    '''
    expected = [expected_fn(i) for i in observed]
    # expected = [2.6,9.6,17.4,21.1,19.2,14.0,8.5,4.4,2.0,0.8,0.3,0.1] # for testing
    new_observed = []
    new_expected = []
    for i in range(1, len(observed)+1): 
        curr_o = observed[len(observed) - i]
        curr_e = expected[len(observed) - i]
        if curr_e < minEi and new_observed:
            new_observed.append(new_observed.pop() + curr_o)
            new_expected.append(new_expected.pop() + curr_e)
            
        else:
            new_observed.append(curr_o)
            new_expected.append(curr_e)

    new_observed.reverse()
    new_expected.reverse()
    
    xos = list(map((lambda oi, ei: math.pow(oi-ei, 2)/ei), new_observed, new_expected))
    # print(f"new_observed={new_observed}. \nnew_expected={new_expected} \nxos={xos}")
    xo = float("{:.3f}".format(sum(xos)))
    
    return (xo, len(new_observed))

# obs = [12,10,19,17,19,6,7,5,5,3,3,1] # for testing
print(f"component 1: {calc_chi(servinsp1, exp_fn)}")
print(f"component 2: {calc_chi(servinsp22, exp_fn)}")
print(f"component 3: {calc_chi(servinsp23, exp_fn)}")
print(f"workstation 1: {calc_chi(ws1, exp_fn)}")
print(f"workstation 2: {calc_chi(ws2, exp_fn)}")
print(f"workstation 3: {calc_chi(ws3, exp_fn)}")