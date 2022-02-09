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