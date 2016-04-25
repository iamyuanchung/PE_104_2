import sys

import numpy as np


class Customer(object):

    def __init__(self, arrival_time, start_service_time, service_time):
        self.arrival_time = arrival_time
        self.start_service_time = start_service_time
        self.service_time = service_time
        self.end_service_time = self.start_service_time + self.service_time
        self.waiting_time = self.start_service_time - self.arrival_time


def generate_exponential_time(mean):
    return np.log(np.random.random()) / -mean

def main():
    """ Usage:

      >> python ./des.py input.txt

    """
    with open(sys.argv[1], 'rb') as f:
        data = f.read().split(' ')
        arrival_time_mean = float(data[0])
        service_time_mean = float(data[1])
        simulation_time = int(data[2])

    t = 0
    Customers = []

    while t < simulation_time:

        # calculate arrival time and service time for the new customer
        if len(Customers) == 0:
            arrival_time = generate_exponential_time(arrival_time_mean)
            start_service_time = arrival_time
        else:
            arrival_time += generate_exponential_time(arrival_time_mean)
            start_service_time = max(arrival_time, Customers[-1].end_service_time)

        service_time = generate_exponential_time(service_time_mean)

        Customers.append(Customer(arrival_time, start_service_time, service_time))

        # increment clock till next end of service
        t = arrival_time


if __name__ == '__main__':
    main()
