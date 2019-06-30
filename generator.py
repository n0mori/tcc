#!/usr/bin/env python3.7

import sys
import random
import datetime


def rotate(lst, n):
    return lst[-n:] + lst[:-n]


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
        normal_traces.append(trace)

        for act in trace:
            if act not in activities:
                duration = mean_time + random.randrange(-deviation, deviation)
                duration *= hour
                activities[act] = duration

    f = open(sys.argv[2])
    for line in f:
        trace = line.rstrip().split(' ')
        anom_traces.append(trace)

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


def gen_log(instances, anomaly=0):
    anoms = [x for x in range(instances)]
    random.shuffle(anoms)
    thresh = int(instances * anomaly / 100)
    anoms = anoms[:thresh]

    offset = starting_date
    for i in range(1, instances):

        random.shuffle(anom_traces)
        random.shuffle(normal_traces)

        if i in anoms:
            generate_trace(i, anom_traces[0], offset)
        else:
            generate_trace(i, normal_traces[0], offset)

        offset += random.randrange(2, 5) * random.randrange(mean_time) * hour

    sorted_log = sorted(log, key=lambda event: event[2])

    print_log(sorted_log)


def generate_anomalies(output=False):
    anom_traces = []
    for trace in normal_traces:
        # Skips
        for i in range(len(trace)):
            for j in range(0, len(trace)):
                for k in range(0, len(trace)):
                    anom = ""
                    for m in range(0, len(trace)):
                        if i == m or j == m or k == m:
                            continue
                        anom += trace[m] + " "
                    anom_traces.append(anom)

        # Inserts
        random_pool = ['DESENVOLVER', 'ENTREGAR', 'GERAR', 'PAGAMENTO']
        for i in range(len(trace)):
            for j in range(0, len(trace)):
                for k in range(0, len(trace)):
                    anom = ""
                    random.shuffle(random_pool)
                    for m in range(0, len(trace)):
                        if i == m or j == m or k == m:
                            random_pool = rotate(random_pool, 1)
                            anom += random_pool[0] + " "
                        anom += trace[m] + " "
                    anom_traces.append(anom)

        # Reworks
        for i in range(len(trace)):
            for j in range(len(trace)):
                anom = ""
                for m in range(len(trace)):
                    if m == j:
                        anom += trace[i] + " "
                    anom += trace[m] + " "
                anom_traces.append(anom)

        # Early e Late
        for i in range(len(trace)):
            for j in range(0, len(trace)):
                newt = trace.copy()
                newt[i], newt[j] = newt[j], newt[i]
                anom = ""
                for act in newt:
                    anom += act + " "
                anom_traces.append(anom)

    my_set = set(anom_traces)
    anom_traces = list(my_set)

    if output:
        for trace in anom_traces:
            print(trace)
    return anom_traces


normal_traces = []
anom_traces = []
activities = {}
log = []
hour = 3600
deviation = 5
mean_time = 10
starting_date = 1557970191

read_input()

gen_log(5000, int(sys.argv[3]))
# generate_anomalies(True)
