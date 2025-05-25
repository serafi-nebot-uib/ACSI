#!/usr/bin/env python3

import arff
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

COLORS = ["pink", "lightgreen", "cyan", "lightblue", "orange"]

def load(path):
  with open(path, "r") as f:
    dataset = arff.load(f)
    _, req, proc, queue, send, cluster = zip(*dataset["data"])
    cluster = [int("".join(filter(str.isdigit, a))) for a in cluster]
    colors = [COLORS[a] for a in cluster]
    return (np.array(x) for x in (req, proc, queue, send, cluster, colors))


def euclidean_3():
  centroids = [(1334.5201, 0.0024), (2286.4463, 0.0041), (1978.8568, 0.0027)]

  cx, cy = zip(*centroids)
  req, proc, queue, send, cluster, colors = load("data/euclidean-3.arff")

  fig, ax = plt.subplots(figsize=(12, 8))

  ax.set_xlabel("requests/s")
  ax.set_ylabel("ProcessTime")
  ax.scatter(req, proc, label="ProessTime", c=colors, s=10)
  ax.scatter(cx, cy, label="centroids", color="black", s=100, marker="x", linewidth=3)

  fig.tight_layout()
  plt.show()

def euclidean_5():
  centroids = [(1937.8234, 0.0026), (2308.9958, 0.0046), (1324.4458, 0.0029), (1336.1735, 0.0021), (2237.3672 ,0.0036)]

  cx, cy = zip(*centroids)
  req, proc, queue, send, cluster, colors = load("data/euclidean-5.arff")

  fig, ax = plt.subplots(figsize=(12, 8))

  ax.set_xlabel("requests/s")
  ax.set_ylabel("ProcessTime")
  ax.scatter(req, proc, label="ProessTime", c=colors, s=10)
  ax.scatter(cx, cy, label="centroids", color="black", s=100, marker="x", linewidth=3)

  fig.tight_layout()
  plt.show()

def manhattan_3():
  centroids = [(1318.2887, 0.0022), (2274.1332, 0.0039), (1948.3173, 0.0027)]

  cx, cy = zip(*centroids)
  req, proc, queue, send, cluster, colors = load("data/manhattan-3.arff")

  fig, ax = plt.subplots(figsize=(12, 8))

  ax.set_xlabel("requests/s")
  ax.set_ylabel("ProcessTime")
  ax.scatter(req, proc, label="ProessTime", c=colors, s=10)
  ax.scatter(cx, cy, label="centroids", color="black", s=100, marker="x", linewidth=3)

  fig.tight_layout()
  plt.show()

def manhattan_3_diff():
  centroids_m = [(1318.2887, 0.0022), (2274.1332, 0.0039), (1948.3173, 0.0027)]
  cx_m, cy_m = zip(*centroids_m)
  req_m, proc_m, queue_m, send_m, cluster_m, colors_m = load("data/manhattan-3.arff")

  centroids_e = [(1334.5201, 0.0024), (2286.4463, 0.0041), (1978.8568, 0.0027)]
  cx_e, cy_e = zip(*centroids_e)
  req_e, proc_e, queue_e, send_e, cluster_e, colors_e = load("data/euclidean-3.arff")

  mask_eq = cluster_m == cluster_e
  mask_diff = cluster_m != cluster_e
  # ymin, ymax = np.min(proc_m), np.max(proc_m)

  fig, ax = plt.subplots(figsize=(12, 8))

  ax.set_xlabel("requests/s")
  ax.set_ylabel("ProcessTime")
  ax.scatter(req_m[mask_eq], proc_m[mask_eq], label="ProessTime", c=colors_m[mask_eq], s=2)
  ax.scatter(req_m[mask_diff], proc_m[mask_diff], label="ProessTime", c=colors_m[mask_diff], s=20)
  ax.scatter(cx_e, cy_e, label="centroids", color="gray", s=100, marker="x", linewidth=3)
  ax.scatter(cx_m, cy_m, label="centroids", color="black", s=100, marker="x", linewidth=3)

  # size = 0.0001
  #
  # for xi, yi, cl, cr in zip(req_m[mask_diff], proc_m[mask_diff], colors_e[mask_diff], colors_m[mask_diff]):
  #   left_square = patches.Rectangle((xi - size, yi - size), size, 2*size, facecolor=cl, edgecolor="black")
  #   right_square = patches.Rectangle((xi, yi - size), size, 2*size, facecolor=cr, edgecolor="black")
  #   ax.add_patch(left_square)
  #   ax.add_patch(right_square)

  # ax.set_ylim(ymin, ymax)
  # ax.set_aspect('equal')

  fig.tight_layout()
  plt.show()

euclidean_3()
euclidean_5()
manhattan_3()
manhattan_3_diff()
