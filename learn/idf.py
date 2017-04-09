
from __future__ import print_function

from time import time
import sys
import os
import numpy as np
import scipy.sparse as sp
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

from sklearn.datasets import load_mlcomp
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import SGDClassifier
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
from sklearn.naive_bayes import MultinomialNB

from learn.reader import get_train, read_articles
print(__doc__)

vectorizer = TfidfVectorizer(encoding='latin1')
vectorizer.build_preprocessor()
x_rows = get_train(read_articles('doz'))
X_train = vectorizer.fit_transform(get_train(read_articles('doz')))
assert sp.issparse(X_train)
# y_train = news_train.target
true_k = np.unique(X_train).shape[0]
print("Extracting features from the dataset using the same vectorizer")
X_test = vectorizer.transform(x_rows)
print("n_samples: %d, n_features: %d" % X_test.shape)
# print("document", X_test)
km = KMeans(n_clusters=true_k, init='k-means++', max_iter=100, n_init=1)
km.fit(X_train.shape)
order_centroids = km.cluster_centers_.argsort()[:, ::-1]
terms = vectorizer.get_feature_names()
# print(terms)
print(order_centroids)
for i in range(1):
    print("Cluster %d:" % i, end='')
    for ind in order_centroids[i, :10]:
        print(' %s' % terms[ind], end='')
# def benchmark(clf_class, params, name):
#     print("parameters:", params)
#     t0 = time()
#     clf = clf_class(**params).fit(X_train, y=None)
#     print("done in %fs" % (time() - t0))
#
#     if hasattr(clf, 'coef_'):
#         print("Percentage of non zeros coef: %f"
#               % (np.mean(clf.coef_ != 0) * 100))
#     print("Predicting the outcomes of the testing set")
#     t0 = time()
#     pred = clf.predict(X_test)
#     print("done in %fs" % (time() - t0))
#
#     print("Classification report on test set for classifier:")
#     print(clf)
#     print()
#     print(classification_report(y_test, pred,
#                                 target_names=news_test.target_names))
#
#     cm = confusion_matrix(y_test, pred)
#     print("Confusion matrix:")
#     print(cm)
#
#     # Show confusion matrix
#     plt.matshow(cm)
#     plt.title('Confusion matrix of the %s classifier' % name)
#     plt.colorbar()


# print("Testbenching a linear classifier...")
# parameters = {
#     'loss': 'hinge',
#     'penalty': 'l2',
#     'n_iter': 50,
#     'alpha': 0.00001,
#     'fit_intercept': True,
# }
#
# benchmark(SGDClassifier, parameters, 'SGD')
#
