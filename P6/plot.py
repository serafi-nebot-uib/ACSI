import arff
import numpy as np
import matplotlib.pyplot as plt

COLORS = ["pink", "lightgreen", "cyan", "lightblue", "orange"]

def euclidean_3():
  centroids = [(1336.4717, 0.0024), (2285.3503, 0.0041), (1982.7224, 0.0027)] 

  with open("data/euclidean-3.arff", "r") as f:
    dataset = arff.load(f)
    _, req, proc, queue, cluster = zip(*dataset["data"])
    cluster = [int("".join(filter(str.isdigit, a))) for a in cluster]
    colors = [COLORS[a] for a in cluster]

    cx, cy = zip(*centroids)

    fig, ax = plt.subplots(figsize=(12, 8))

    ax.set_xlabel("requests/s")
    ax.set_ylabel("ProcessTime")
    ax.scatter(req, proc, label="ProessTime", c=colors, s=10)
    ax.scatter(cx, cy, label="centroids", color="black", s=100, marker="x", linewidth=3)

    fig.tight_layout()
    plt.show()

def euclidean_5():
  centroids = [(1331.6731, 0.0021), (2307.2647, 0.0046), (1335.0028, 0.0029), (2240.304, 0.0036), (1940.6533, 0.0026)]

  with open("data/euclidean-5.arff", "r") as f:
    dataset = arff.load(f)
    _, req, proc, queue, cluster = zip(*dataset["data"])
    cluster = [int("".join(filter(str.isdigit, a))) for a in cluster]
    colors = [COLORS[a] for a in cluster]

    cx, cy = zip(*centroids)

    fig, ax = plt.subplots(figsize=(12, 8))

    ax.set_xlabel("requests/s")
    ax.set_ylabel("ProcessTime")
    ax.scatter(req, proc, label="ProessTime", c=colors, s=10)
    ax.scatter(cx, cy, label="centroids", color="black", s=100, marker="x", linewidth=3)

    fig.tight_layout()
    plt.show()

def manhattan_3():
  centroids = [(1319.1447, 0.0022), (2273.9313, 0.0039), (1948.303, 0.0027)]

  with open("data/manhattan-3.arff", "r") as f:
    dataset = arff.load(f)
    _, req, proc, queue, cluster = zip(*dataset["data"])
    cluster = [int("".join(filter(str.isdigit, a))) for a in cluster]
    colors = [COLORS[a] for a in cluster]

    cx, cy = zip(*centroids)

    fig, ax = plt.subplots(figsize=(12, 8))

    ax.set_xlabel("requests/s")
    ax.set_ylabel("ProcessTime")
    ax.scatter(req, proc, label="ProessTime", c=colors, s=10)
    ax.scatter(cx, cy, label="centroids", color="black", s=100, marker="x", linewidth=3)

    fig.tight_layout()
    plt.show()

# euclidean_3()
# euclidean_5()
manhattan_3()
