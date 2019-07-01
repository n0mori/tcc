#!/usr/bin/env python3.7

import os
import re
from reader import get_traces
from gensim.models import Word2Vec
from sklearn.svm import OneClassSVM
from scipy.spatial import distance
import numpy as np


def train(filename, epochs=15):
    traces = get_traces("logs/" + filename)
    model = Word2Vec(traces, min_count=1, workers=12)
    print("training", filename)
    # deveria iterar o modelo? não sei, não são novas sentenças

    model.save("models/" + re.sub(r"\.csv", "", filename) + ".model")


def train_batch():
    for filenames in os.listdir("logs"):
        if re.search(r"\.csv", filenames):
            train(filenames)


def create_vectors(filename, vectors):
    model = Word2Vec.load(filename)

    trace_vectors = []
    for trace in vectors:
        v = np.array(model.wv[trace[0]])

        for word in trace[1:]:
            v = list(map(sum, zip(v, model.wv[word])))
        vec = np.array(v)
        vec = vec / len(trace)
        trace_vectors.append(v)
    return trace_vectors


def check_anomaly(vector, normal_traces):
    return " ".join(vector) not in normal_traces


# train_batch()
vectors = get_traces("logs/log1_anom_all_5.csv")
v = create_vectors("models/log1_anom_all_5.model", vectors)

ocsvm = OneClassSVM(kernel='rbf', nu=0.05)
classes = list(ocsvm.fit_predict(v))
print(classes.count(-1), classes.count(1))

anom_cases = [vectors[k] for k, x in enumerate(classes) if x == -1]

normal_traces = [line.strip('\n') for line in open("normal_pn1.txt", 'r')]

# teste = "SOLICITACAO AUTORIZACAO DISTR.DIRETORIA DISTR.SETOR ALT.SITUACAOP/EMEXECUCAO ALT.SITUACAOP/SUSPENSO CONCLUSAO".split(" ")
# print(check_anomaly(teste, normal_traces))
print([check_anomaly(t, normal_traces) for t in anom_cases])
