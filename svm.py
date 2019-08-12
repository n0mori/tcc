#!/usr/bin/env python3.7

from encode import create_vectors
from sklearn.svm import OneClassSVM
from sklearn.svm import SVC
from reader import get_traces
import numpy as np
import os
import re
from random import shuffle


def one_class(log_name, vectors, train, test, normal_traces, output_file):
    nus = [0.05, 0.1, 0.3, 0.5]

    for nu in nus:
        print(log_name, nu)
        ocsvm = OneClassSVM(kernel='linear', nu=nu)
        ocsvm.fit(train)
        classes = list(ocsvm.predict(test))

        anom_cases = [vectors[k] for k, x in enumerate(classes) if x == -1]
        normal_cases = [vectors[k] for k, x in enumerate(classes) if x == 1]

        anom_checked = [is_normal(t, normal_traces) for t in anom_cases]
        normal_checked = [is_normal(t, normal_traces) for t in normal_cases]

        print(log_name, 
            "oc", 
            len(anom_checked), 
            anom_checked.count(True), 
            anom_checked.count(False), 
            len(normal_checked), 
            normal_checked.count(True), 
            normal_checked.count(False),
            nu, file=output_file, sep=",")


def supervised(log_name, vectors, train, test, normal_traces, labels, output_file):

    svc = SVC(kernel='linear')
    svc.fit(train, labels)
    classes = list(svc.predict(test))

    anom_cases = [vectors[k] for k, x in enumerate(classes) if x == -1]
    normal_cases = [vectors[k] for k, x in enumerate(classes) if x == 1]

    anom_checked = [is_normal(t, normal_traces) for t in anom_cases]
    normal_checked = [is_normal(t, normal_traces) for t in normal_cases]
    print(log_name, 
          "sv", 
          len(anom_checked), 
          anom_checked.count(True), 
          anom_checked.count(False), 
          len(normal_checked), 
          normal_checked.count(True), 
          normal_checked.count(False), file=output_file, sep=",")


def batch(output_name):
    normal_traces1 = [line.strip('\n') for line in open("normal_pn1.txt", 'r')]
    normal_traces2 = [line.strip('\n') for line in open("normal_pn2.txt", 'r')]
    output_file = open("outputs/" + output_name + ".csv", "w+")
    print("log,method,size0,normal0,anom0,size1,normal1,anom1,nu", file=output_file)
    for filename in os.listdir("logs"):
        filename = re.sub(r"\.csv$", "", filename)

        if filename == "xes": continue

        vectors = get_traces("logs/" + filename + ".csv")
        v = create_vectors("models_size16/" + filename + ".model", vectors)

        shuffle(v)

        limit = int(len(vectors) * 0.7)
        train, test = v[:limit], v[limit:]
        

        if filename.startswith("log1"):
            labels = np.array([1 if is_normal(trace, normal_traces1) else -1 for trace in vectors[:limit]])
            one_class(filename, vectors, train, test, normal_traces1, output_file)
            if filename != "log1": supervised(filename, vectors, train, test, normal_traces1, labels, output_file)
        elif filename.startswith("log2"):
            labels = np.array([1 if is_normal(trace, normal_traces2) else -1 for trace in vectors[:limit]])
            one_class(filename, vectors, train, test, normal_traces2, output_file)
            if filename != "log2": supervised(filename, vectors, train, test, normal_traces2, labels, output_file)


def is_normal(vector, normal_traces):
    # if true, it is a normal behaviour
    return " ".join(vector) in normal_traces


for i in range(1,11):
    batch("output" + str(i))
