#!/usr/bin/env python3.7

import csv

fields = ['log', 'method', 'nu', 'accuracy']

def calculate_accuracy(ifile, ofile):
    with open(ifile, "r") as csvfile, open(ofile, "w+") as output:
        reader = csv.reader(csvfile, delimiter=',')
        next(reader)
        for line in reader:
            tp = float(line[4])
            fp = float(line[3])
            fn = float(line[7])
            tn = float(line[6])
            accuracy = (tp + tn) / (tp + tn + fp + fn)
            print(line[0], line[1], line[8], round(accuracy, 2), sep=',', file=output)


for i in range(1,11):
    dir = "outputs/"
    calculate_accuracy(dir + "output" + str(i) + ".csv", dir + "acc" + str(i) + ".csv")
