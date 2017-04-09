from sklearn import metrics
from sklearn.cluster import KMeans
from sklearn.decomposition import TruncatedSVD
from sklearn.feature_extraction.text import TfidfTransformer, TfidfVectorizer
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import Normalizer

import numpy as np

from learn.reader import get_train, read_articles, example_article

dataset = get_train(read_articles('dr_medi'))
# labels = dataset.target
# true_k = np.unique(dataset).shape[0]
true_k = np.unique(dataset[:8]).shape[0]

vectorizer = TfidfVectorizer()
# X = vectorizer.fit_transform(dataset)
X = vectorizer.fit_transform(get_train(read_articles('dr_medi')))
print(X.shape)
svd = TruncatedSVD(true_k)
lsa = make_pipeline(svd, Normalizer(copy=False))

X = lsa.fit_transform(X)

km = KMeans(init='k-means++', max_iter=100)
km.fit(X)

print(km.labels_)
# print(km.predict())
print(km.cluster_centers_)
terms = vectorizer.get_feature_names()
print('terms', terms)
original_space_centroids = svd.inverse_transform(km.cluster_centers_)
order_centroids = original_space_centroids.argsort()[:, ::-1]
# for i in range(true_k):
for i in range(8):
    print("Cluster %d:" % i, end='')
    # for ind in order_centroids[i, :8]:
    for ind in order_centroids[i, :10]:
        print(' %s' % terms[ind], end='')
    print()
#
# print("Homogeneity: %0.3f" % metrics.homogeneity_score(X, km.labels_))
# print("Completeness: %0.3f" % metrics.completeness_score(X, km.labels_))
# print("V-measure: %0.3f" % metrics.v_measure_score(X, km.labels_))


# article = example_article('doz')
article = ['katar alergia']
X = vectorizer.fit_transform(article)
true_k = np.unique(article).shape[0]
vectorizer = TfidfVectorizer()
# X = vectorizer.fit_transform(dataset)
X = vectorizer.fit_transform(article)
print(X.shape)
svd = TruncatedSVD(true_k)
lsa = make_pipeline(svd, Normalizer(copy=False))

X = lsa.fit_transform(X)

prediction = km.predict(X)
# print(prediction)

def vectorize_data(X):
    X = vectorizer.fit_transform(X)
    X = lsa.fit_transform(X)
    return X