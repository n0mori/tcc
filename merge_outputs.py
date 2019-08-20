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
            print(line[0], line[1], line[8], round(accuracy, 2),
                  sep=',', file=output)


def average():
    dir = "outputs/"
    files = [open(f"{dir}acc{i}.csv", "r") for i in range(1, 11)]
    readers = [csv.reader(f, delimiter=',') for f in files]
    with open(f"{dir}avg.csv", "w+") as output:
        while True:
            try:
                rows = [next(row) for row in readers]
            except StopIteration:
                break
            accuracies = [float(r[3]) for r in rows]
            method = rows[0][1] + rows[0][2] if rows[0][1] == "oc" else rows[0][1]
            average = sum(accuracies) / len(accuracies)
            average = round(average, 2)
            print(rows[0][0], method, average, sep=',', file=output)


average()
