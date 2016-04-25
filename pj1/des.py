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
    with open(sys.argv[1], 'rb') as f:
        data = f.read().split(' ')
        arrival_time_mean = float(data[0])
        service_time_mean = float(data[1])
        simulation_time = int(data[2])

    queue_list = []
    current_time = 0
    while current_time < simulation_time:
        current_time += generate_exponential_time(arrival_time_mean)
        queue_list.append(
            Customer(
                arrival_time=current_time,
                service_time=generate_exponential_time(service_time_mean)
            )
        )

    current_time = queue_list[0].arrival_time
    finish_list = []
    while current_time < simulation_time:

        if len(s1.serving) == 0 or len(s2.serving) == 0:
            # if at least one of the two servers is not busy ...
            c = queue_list.pop(0)
            c.start_service_time = current_time
            if len(s1.serving) == 0 and len(s2.serving) > 0:
                # assign the customer to the first server
                c.served_by = 1
                c.end_service_time = current_time + self.service_time
                s1.serving.append(c)
                if c.end_service_time < queue_list[0].arrival_time:
                    finish_list.append(s1.pop(0))
                    current_time = c.end_service_time
                else:
                    current_time = queue_list[0].arrival_time
            elif len(s1.serving) > 0 and len(s2.serving) == 0:
                # assign the customer to the second server
                c.served_by = 2
                c.end_service_time = current_time + self.service_time
                s2.serving.append(c)
                if c.end_service_time < queue_list[0].arrival_time:
                    finish_list.append(s2.pop(0))
                    current_time = c.end_service_time
                else:
                    current_time = queue_list[0].arrival_time
            else:
                # randomly assign the customer to one of the server
                if np.random.random() <= 0.5:
                    c.served_by = 1
                    c.end_service_time = current_time + self.service_time
                    s1.serving.append(c)
                    if c.end_service_time < queue_list[0].arrival_time:
                        finish_list.append(s1.pop(0))
                        current_time = c.end_service_time
                    else:
                        current_time = queue_list[0].arrival_time
                else:
                    c.served_by = 2
                    c.end_service_time = current_time + self.service_time
                    s2.serving.append(c)
                    if c.end_service_time < queue_list[0].arrival_time:
                        finish_list.append(s2.pop(0))
                        current_time = c.end_service_time
                    else:
                        current_time = queue_list[0].arrival_time

    """
    s1 = Staff()
    s2 = Staff()
    queue_list = []
    finish_list = []
    current_time = 0

    while current_time < simulation_time:
        queue_list.append(Customer(current_time + generate_exponential_time(arrival_time_mean)))

        if len(s1.serving) == 0 or len(s2.serving) == 0:
            # if at least one of the two servers is not busy ...
            c = queue_list.pop(0)
            c.start_service_time = current_time
            if len(s1.serving) == 0 and len(s2.serving) > 0:
                # assign the customer to the first server
                c.served_by = 1
                s1.serving.append(c)
                c.end_service_time = current_time + generate_exponential_time(service_time_mean)
                if c.end_service_time < queue_list[0].arrival_time:
                    finish_list.append(s1.pop(0))
                    current_time = c.end_service_time
                else:
                    current_time = queue_list[0].arrival_time
            elif len(s1.serving) > 0 and len(s2.serving) == 0:
                # assign the customer to the second server
                c.served_by = 2
                s2.serving.append(c)
            else:
                # randomly assign the customer to one of the server
                if np.random.random() <= 0.5:
                    c.served_by = 1
                    s1.serving.append(c)
                else:
                    c.served_by = 2
                    s2.serving.append(c)
    """


if __name__ == '__main__':
    main()
