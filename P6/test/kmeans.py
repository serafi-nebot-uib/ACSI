import numpy as np
from tinygrad.tensor import Tensor

class KMeans:
  def __init__(self, n_clusters=3, max_iters=100, tol=1e-4):
    self.n_clusters = n_clusters
    self.max_iters = max_iters
    self.tol = tol
    self.centroids = None

  def fit(self, X):
    # X: numpy array of shape (n_samples, n_features)
    n_samples, n_features = X.shape
    # Initialize centroids randomly from data points
    indices = np.random.choice(n_samples, self.n_clusters, replace=False)
    centroids = Tensor(X[indices])  # (k, features)

    for i in range(self.max_iters):
      # Compute distances: expand and compute L2 squared
      # X_tensor: (n_samples, features), centroids: (k, features)
      X_tensor = Tensor(X)  # (n_samples, features)
      # Expand dims for broadcast: (n_samples, 1, features) and (1, k, features)
      X_exp = X_tensor.reshape(n_samples, 1, n_features)
      C_exp = centroids.reshape(1, self.n_clusters, n_features)
      # Compute squared distances and assign clusters
      dists = ((X_exp - C_exp) ** 2).sum(axis=2)  # (n_samples, k)
      labels = dists.argmin(axis=1)  # (n_samples,)

      # Update centroids
      new_centroids = []
      for k in range(self.n_clusters):
        mask = (labels == k).expand_dims(1)  # (n_samples, 1)
        count = mask.sum() + 1e-8
        # Sum of points in cluster k
        cluster_sum = (X_tensor * mask).sum(axis=0)
        new_centroids.append(cluster_sum / count)
      new_centroids = Tensor.stack(new_centroids, axis=0)  # (k, features)

      # Check convergence
      shift = ((centroids - new_centroids) ** 2).sum().item()
      centroids = new_centroids
      if shift < self.tol:
        print(f"Converged at iteration {i}")
        break

    self.centroids = centroids
    self.labels_ = labels.numpy()
    return self

  def predict(self, X):
    X_tensor = Tensor(X)
    n_samples, n_features = X.shape
    X_exp = X_tensor.reshape(n_samples, 1, n_features)
    C_exp = self.centroids.reshape(1, self.n_clusters, n_features)
    dists = ((X_exp - C_exp) ** 2).sum(axis=2)
    labels = dists.argmin(axis=1)
    return labels.numpy()

if __name__ == "__main__":
  # Example usage with synthetic data
  from sklearn.datasets import make_blobs

  X, y_true = make_blobs(n_samples=300, centers=4, cluster_std=0.60, random_state=0)

  kmeans = KMeans(n_clusters=4, max_iters=100)
  kmeans.fit(X)
  y_pred = kmeans.labels_

  # Visualize results
  import matplotlib.pyplot as plt
  plt.scatter(X[:, 0], X[:, 1], c=y_pred)
  centroids = kmeans.centroids.numpy()
  plt.scatter(centroids[:, 0], centroids[:, 1], s=200, alpha=0.75, marker="X")
  plt.title("K-Means Clustering with tinygrad")
  plt.show()

