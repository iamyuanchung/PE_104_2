""" Requirements:

  0. Two servers and single queue
  1. Two servers have the same service rate
  2. FIFO queue
  3. Infinite queue capacity
  4. Inter-arrival and service time: i.i.d. and exponential distribution

"""
import sys

import numpy as np


class Customer(object):

    def __init__(self, arrival_time, service_time):
        self.arrival_time = arrival_time
        self.service_time = service_time
        self.start_service_time = None
        self.end_service_time = None
        self.served_by = None
        # waiting time = self.start_service_time - self.arrival_time
        # system time = self.end_service_time - self.arrival_time


class Staff(object):

    def __init__(self):
        self.serving = []


def generate_exponential_time(mean):
    return np.log(np.random.random()) / -mean

def main():
    """ Usage:

      >> python ./des.py input.txt

    """
    # read in the input file
    with open(sys.argv[1], 'rb') as f:
        data = f.read().split(' ')
        arrival_time_mean = float(data[0])
        service_time_mean = float(data[1])
        simulation_time = int(data[2])

    # run the simulation
    

    # output the final statistics
    total_waiting_time = 0.
    total_system_time = 0.
    for c in customer_list:
        total_waiting_time += (c.start_service_time - c.arrival_time)
        total_system_time += (c.end_service_time - c.arrival_time)
    print 'Average waiting time: %f' % total_waiting_time / len(customer_list)
    print 'Average system time: %f' % total_system_time / len(customer_list)


if __name__ == '__main__':
    main()
