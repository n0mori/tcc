#!/usr/bin/env python3.7

import os
from reader import get_traces
from gensim.models import Word2Vec


def train(filename):
    traces = get_traces(filename)
