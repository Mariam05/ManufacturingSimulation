'''
This file has shared variables and general utility functions 
that execute general logic shared by multiple classes or files
'''
import logging
import csv


def logging_setup():
    format = "%(asctime)s.%(msecs)03d: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                            datefmt="%H:%M:%S")
    logging.getLogger().setLevel(logging.INFO)

arrival = 1
departure = 2

NUM_OF_REPLICATIONS = 5
INIT_PHASE = 0.51

def write_to_file(filename, data):
    ''' A utility function that takes a filename and appends the data to the last line in the file. '''
    with open(filename, "a") as reader:
        reader.write(data)
        reader.write("\n")
 
def delete_file_contents(filename):
    ''' Will erase the previous contents of a file '''
    open(filename, "w").close()

def write_to_csv(filename, row):
    with open(filename, 'a', newline='') as f:
        # create the csv writer
        writer = csv.writer(f)

        # write a row to the csv file
        writer.writerow(row)