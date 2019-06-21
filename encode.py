#!/usr/bin/env python3.7

import Trace2Vec as t2v
import os

vectorsize=16
for filename in os.listdir('logs/xes'):
    t2v.learn(filename,vectorsize)
