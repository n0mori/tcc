#!/usr/bin/env python3.7
import re
import sklearn.svm as sk
import os
import Trace2Vec
import matplotlib.pyplot as plt
from gensim.models.doc2vec import Doc2Vec, TaggedDocument

files = ['output/' + x for x in os.listdir('output') if re.search(r"\.model$", x)]

for filename in files[:1]:
    model = Doc2Vec.load(filename)
    vectors = model.docvecs.vectors_docs
    svm = sk.OneClassSVM(kernel='linear')
    svm.fit(list(vectors))
    print(svm.predict(vectors))
    # print(filename, len(groups), groups.count(1), groups.count(-1))
    # word_vectors = read_wordvec('output/' + filename)
    # Trace2Vec.cluster(filename, vectorsize=16, clusterType="OCSVM")
    
