import csv

# read flash.dat to a list of lists
servinsp1 = [float(i.strip()) for i in open("servinsp1").readlines()]
servinsp22 = [float(i.strip()) for i in open("servinsp22").readlines()]
servinsp22 = [float(i.strip()) for i in open("servinsp23").readlines()]

ws1 = [float(i.strip()) for i in open("ws1").readlines()]
ws2 = [float(i.strip()) for i in open("ws2").readlines()]
ws3 = [float(i.strip()) for i in open("ws3").readlines()]

minEi = 5
# data = [2.6, 9.6, 17.4, 21.1, 19.2, 14, 8.5, 4.4, 2, 0.8, 0.3, 0.1]

def group(data):
    new_lst = []
    for i in range(1, len(data)+1): 
        curr = float(data[len(data) - i])
        if curr < minEi and new_lst:
            new_lst.append(float(new_lst.pop() + curr))
        else:
            new_lst.append(curr)

    return new_lst.reverse()
