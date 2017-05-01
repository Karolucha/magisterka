from sklearn import metrics
from sklearn.cluster import KMeans
from sklearn.decomposition import TruncatedSVD
from sklearn.feature_extraction.text import TfidfTransformer, TfidfVectorizer
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import Normalizer
from sklearn.neural_network import BernoulliRBM
import numpy as np
from pyclustering.nnet.som import som
from pyclustering.cluster.kmeans import kmeans
from learn.reader import get_train, read_articles, example_article
from kohonen import kohonen
from pyclustering.cluster.syncsom import syncsom
from pyclustering.cluster import cluster_visualizer
from pyclustering.nnet.cnn import cnn_network, cnn_visualizer
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

network = syncsom(X, 2, 2, 0.9);
(dyn_time, dyn_phase) = network.process(True, 0.999);
# network.show_sync_layer();
clusters = network.get_clusters();
visualizer = cluster_visualizer();
visualizer.append_clusters(clusters, X);
visualizer.show();


# kmeans_instance = kmeans(X, [[ 0.93036182, -0.20536988, -0.17834053,  0.03102577,  0.01767965, -0.06377806, 0.22167392, -0.077218]]);
#
# kmeans_instance.process();
# clusters = kmeans_instance.get_centers();
# print(clusters)
#
# network = som(5, 5, X, 100);
#
# network.train();
# network.show_network();


# rbm = BernoulliRBM(random_state=0, verbose=True)
# print(rbm)
# pyclustering.
# rbm.fit(X)
# scores = rbm.score_samples(X[10:35])
# print(scores)
# # predictions = rbm.predict(X[10:35])
# # print(predictions)
# print(dir(rbm))