#!/usr/bin/env python3.7

from encode import create_vectors
from sklearn.svm import OneClassSVM
from sklearn.svm import SVC
from reader import get_traces
import numpy as np
import os
import re


def one_class(log_name, normal_traces):
    vectors = get_traces("logs/" + log_name + ".csv")
    v = create_vectors("models_size16/" + log_name + ".model", vectors)
    output_file = open("outputs/oc_" + log_name + ".txt", "w+")
    nus = [0.05, 0.1, 0.3, 0.5]

    for nu in nus:
        print(nu, file=output_file)
        ocsvm = OneClassSVM(kernel='linear', nu=nu)
        classes = list(ocsvm.fit_predict(v))
        print(classes.count(-1), classes.count(1), file=output_file)

        anom_cases = [vectors[k] for k, x in enumerate(classes) if x == -1]
        normal_cases = [vectors[k] for k, x in enumerate(classes) if x == 1]

        anom_checked = [is_normal(t, normal_traces) for t in anom_cases]
        normal_checked = [is_normal(t, normal_traces) for t in normal_cases]
        # print([k for k, x in enumerate(classes) if x == -1], [k for k, x in enumerate(classes) if x == 1])
        print("size:", len(anom_checked), "normal:", anom_checked.count(True), "anomaly:", anom_checked.count(False), file=output_file)
        print("size:", len(normal_checked), "normal:", normal_checked.count(True), "anomaly:", normal_checked.count(False), file=output_file)


def supervised(log_name, normal_traces):
    vectors = get_traces("logs/" + log_name + ".csv")
    v = create_vectors("models_size16/" + log_name + ".model", vectors)
    labels = np.array([1 if is_normal(trace, normal_traces) else -1 for trace in vectors])
    output_file = open("outputs/sv_" + log_name + ".txt", "w+")

    # Keeping the consistency for parsing the output file
    print(1, file=output_file)
    svc = SVC(kernel='linear')
    svc.fit(v, labels)
    classes = list(svc.predict(v))
    print(classes.count(-1), classes.count(1), file=output_file)

    anom_cases = [vectors[k] for k, x in enumerate(classes) if x == -1]
    normal_cases = [vectors[k] for k, x in enumerate(classes) if x == 1]

    anom_checked = [is_normal(t, normal_traces) for t in anom_cases]
    normal_checked = [is_normal(t, normal_traces) for t in normal_cases]
    # print([k for k, x in enumerate(classes) if x == -1], [k for k, x in enumerate(classes) if x == 1])
    print("size:", len(anom_checked), "normal:", anom_checked.count(True), "anomaly:", anom_checked.count(False), file=output_file)
    print("size:", len(normal_checked), "normal:", normal_checked.count(True), "anomaly:", normal_checked.count(False), file=output_file)


def batch():
    normal_traces1 = [line.strip('\n') for line in open("normal_pn1.txt", 'r')]
    normal_traces2 = [line.strip('\n') for line in open("normal_pn2.txt", 'r')]
    for filename in os.listdir("logs"):
        filename = re.sub(r"\.csv$", "", filename)
        if filename.startswith("log1"):
            one_class(filename, normal_traces1)
            if filename != "log1": supervised(filename, normal_traces1)
        elif filename.startswith("log2"):
            one_class(filename, normal_traces2)
            if filename != "log2": supervised(filename, normal_traces2)


def is_normal(vector, normal_traces):
    # if true, it is a normal behaviour
    return " ".join(vector) in normal_traces


batch()
