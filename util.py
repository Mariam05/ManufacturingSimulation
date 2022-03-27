'''
This file has shared variables and general utility functions 
that execute general logic shared by multiple classes or files
'''
import logging


def logging_setup():
    format = "%(asctime)s.%(msecs)03d: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                            datefmt="%H:%M:%S")
    logging.getLogger().setLevel(logging.INFO)

arrival = 1
departure = 2


def write_to_file(filename, data):
    ''' A utility function that takes a filename and appends the data to the last line in the file. '''
    with open(filename, "a") as reader:
        reader.write(data)
 