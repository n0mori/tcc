import sys
import random
import datetime
import calendar
import time

traces = []
activities = {}
log = []
hour = 3600
deviation = 5
mean_time = 10


def generate_trace(case_id, trace, offset):
    for act in trace:
        elapsed_time = (activities[act] +
                        (random.randrange(-deviation, deviation)) * hour)

        tupl = (case_id, act, offset)
        log.append(tupl)

        offset += elapsed_time


def read_input():
    f = open(sys.argv[1])
    for line in f:
        trace = line.rstrip().split(' ')
        traces.append(trace)

        for act in trace:
            if act not in activities:
                duration = mean_time + random.randrange(-deviation, deviation)
                duration *= hour
                activities[act] = duration


def print_log(sorted_log):
    print("Case ID, Activity, Timestamp")
    for event in sorted_log:
        date = datetime.datetime.utcfromtimestamp(event[2])
        print(event[0], event[1], date, sep=',')


def gen_log(instances):
    offset = calendar.timegm(time.gmtime())
    for i in range(1, instances):
        random.shuffle(traces)

        generate_trace(i, traces[0], offset)

        offset += random.randrange(2, 5) * random.randrange(mean_time) * hour

    sorted_log = sorted(log, key=lambda event: event[2])

    print_log(sorted_log)


def main():
    read_input()
    gen_log(5000)


main()
