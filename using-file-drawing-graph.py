import numpy as np
import random
from math import exp
import math as m
import pandas as pd
import matplotlib.pyplot as plt


def draw_path(path, nom_villes, x_villes, y_villes, title="Path Visualization", color="red"):
    plt.figure(figsize=(8,6))
    plt.scatter(x_villes, y_villes, color='skyblue', s=80)

    for i in range(len(path) - 1):
        plt.plot(
            [x_villes[path[i]], x_villes[path[i+1]]],
            [y_villes[path[i]], y_villes[path[i+1]]],
            color=color, linewidth=2
        )

    for i, city in enumerate(nom_villes):
        plt.text(x_villes[i] + 0.15, y_villes[i] + 0.15, city, fontsize=8)

    plt.title(title)
    plt.xlabel("X (km)")
    plt.ylabel("Y (km)")
    plt.grid(True)
    plt.show()


df = pd.read_csv(r"C:\Users\HP\Downloads\algeria_20_cities_xy.csv")

nom_villes = df["city"].values
nbr_villes = len(nom_villes)
x_villes = df["x_km"].values
y_villes = df["y_km"].values

plt.figure(figsize=(8,6))
plt.scatter(x_villes, y_villes, color='dodgerblue', s=80)
for i, city in enumerate(nom_villes):
    plt.text(x_villes[i] + 0.1, y_villes[i] + 0.1, city, fontsize=9)
plt.title("Algeria – City Coordinates")
plt.xlabel("X (km)")
plt.ylabel("Y (km)")
plt.grid(True)
plt.show()

distances = np.zeros((nbr_villes, nbr_villes))
for i in range(nbr_villes):
    for j in range(i + 1, nbr_villes):
        dx = x_villes[i] - x_villes[j]
        dy = y_villes[i] - y_villes[j]
        d = m.sqrt(dx**2 + dy**2)
        distances[i, j] = d
        distances[j, i] = d

print("\nFull distance matrix:")
print(distances)

upper = np.triu(distances, k=1)
print("\nUpper triangle matrix (used for random search):")
print(upper)

s0 = float("+inf")
best_path = None
j = 500
while j > 0:
    s = 0
    path = np.random.permutation(nbr_villes)
    for k in range(nbr_villes - 1):
        a, b = path[k], path[k + 1]
        s += distances[a, b]
    if s < s0:
        s0 = s
        best_path = path
    j -= 1
draw_path(best_path, nom_villes, x_villes, y_villes, title="Random Search", color="orange")
print("\nBest random path found:")
print(" → ".join(nom_villes[best_path]))
print(f"Total distance: {s0}")

j = 500
path = np.arange(nbr_villes)
i = 0
s0 = 0
for k in range(nbr_villes - 1):
    a, b = path[k], path[k + 1]
    s0 += distances[a, b]
while j > 0:
    temp_path = path.copy()
    temp_path[i], temp_path[-(i + 1)] = temp_path[-(i + 1)], temp_path[i]
    s = 0
    for k in range(nbr_villes - 1):
        a, b = temp_path[k], temp_path[k + 1]
        s += distances[a, b]
    if s < s0:
        s0 = s
        path = temp_path
    i = (i + 1) % nbr_villes
    j -= 1
draw_path(path, nom_villes, x_villes, y_villes, title="Local Search", color="green")
print("\nBest local path found:")
print(" → ".join(nom_villes[path]))
print(f"Total distance: {s0}")

tabu_list = []
s0 = float("+inf")
best_path = None
j = 500
while j > 0:
    s = 0
    path = np.random.permutation(nbr_villes)
    path_tuple = tuple(path)
    if path_tuple not in tabu_list:
        for k in range(nbr_villes - 1):
            a, b = path[k], path[k + 1]
            s += distances[a, b]
        if s < s0:
            s0 = s
            best_path = path
        tabu_list.append(path_tuple)
    j -= 1
draw_path(best_path, nom_villes, x_villes, y_villes, title="Random Search (Tabu)", color="purple")
print("\nBest random path found (tabu added to this method):")
print(" → ".join(nom_villes[best_path]))
print(f"Total distance: {s0}")

j = 500
path = np.arange(nbr_villes)
i = 0
s0 = 0
tabu_list = []
for k in range(nbr_villes - 1):
    a, b = path[k], path[k + 1]
    s0 += distances[a, b]
path_tuple = tuple(path)
tabu_list.append(path_tuple)
while j > 0:
    temp_path = path.copy()
    temp_path[i], temp_path[-(i + 1)] = temp_path[-(i + 1)], temp_path[i]
    temp_path_tuple = tuple(temp_path)
    if temp_path_tuple not in tabu_list:
        s = 0
        for k in range(nbr_villes - 1):
            a, b = temp_path[k], temp_path[k + 1]
            s += distances[a, b]
        if s < s0:
            s0 = s
            path = temp_path.copy()
        tabu_list.append(temp_path_tuple)
    i = (i + 1) % (nbr_villes // 2)
    j -= 1
draw_path(path, nom_villes, x_villes, y_villes, title="Local Search (Tabu)", color="blue")
print("\nBest local path found (tabu applied):")
print(" → ".join(nom_villes[path]))
print(f"Total distance: {s0}")

path = np.arange(nbr_villes)
s0 = 0
for k in range(nbr_villes - 1):
    a, b = path[k], path[k + 1]
    s0 += distances[a, b]
best = s0
best_path = path.copy()
t0 = 500
alpha = 0.99
i = 0
while t0 > 0.1:
    temp_path = path.copy()
    temp_path[i], temp_path[-(i + 1)] = temp_path[-(i + 1)], temp_path[i]
    s = 0
    for k in range(nbr_villes - 1):
        a, b = temp_path[k], temp_path[k + 1]
        s += distances[a, b]
    delta_e = s - s0
    if delta_e < 0 or random.random() < exp(-delta_e / t0):
        s0 = s
        path = temp_path.copy()
    if s0 < best:
        best = s0
        best_path = path.copy()
    t0 *= alpha
    i = (i + 1) % (nbr_villes // 2)
draw_path(best_path, nom_villes, x_villes, y_villes, title="Recuit Simulé", color="red")
print("\nBest local path found (Recuit Simulé):")
print(" → ".join(nom_villes[best_path]))
print(f"Total distance: {best}")
