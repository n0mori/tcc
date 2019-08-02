#!/usr/bin/env python3.7

import os
import re
from reader import get_traces
from gensim.models import Word2Vec
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
