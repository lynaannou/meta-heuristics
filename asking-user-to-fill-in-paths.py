import numpy as np
import random
from math import exp

# --- Get cities from user ---
user_input = input("Give names of cities, separated by spaces: ")
nom_villes = np.array(user_input.split())
nbr_villes = len(nom_villes)

# --- Initialize matrix ---
distances = np.zeros((nbr_villes, nbr_villes))

# --- Fill upper triangle with distances ---
for i in range(nbr_villes):
    for j in range(i + 1, nbr_villes):
        d = float(input(f"Give distance between {nom_villes[i]} and {nom_villes[j]}: "))
        distances[i, j] = d
        distances[j, i] = d

print("\nFull distance matrix:")
print(distances)

upper = np.triu(distances, k=1)
print("\nUpper triangle matrix (used for random search):")
print(upper)

# --- Random search for minimal path ---
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

print("\nBest random path found:")
print(" → ".join(nom_villes[best_path]))
print(f"Total distance: {s0}")

# --- Local search for minimal path ---
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

print("\nBest local path found:")
print(" → ".join(nom_villes[path]))
print(f"Total distance: {s0}")

# ---- Tabu Search on Random Search ----
tabu_list = []
s0 = float("+inf")
best_path = None

j = 500
while j > 0:
    s = 0
    path = np.random.permutation(nbr_villes)
    
    # Convert to tuple to allow list membership check
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

print("\nBest random path found (tabu added to this method):")
print(" → ".join(nom_villes[best_path]))
print(f"Total distance: {s0}")
print("\nAll paths registered in the tabu list:")
for i, t_path in enumerate(tabu_list, start=1):
    city_names = " → ".join(nom_villes[list(t_path)])
    print(f"{i:03d}: {city_names}")

# ---- Tabu Search on Local Search ----
j = 500
path = np.arange(nbr_villes)
i = 0
s0 = 0
tabu_list = []

# Compute initial distance
for k in range(nbr_villes - 1):
    a, b = path[k], path[k + 1]
    s0 += distances[a, b]

# Add initial path to tabu list
path_tuple = tuple(path)
tabu_list.append(path_tuple)

while j > 0:
    temp_path = path.copy()
    # Swap two positions symmetrically to create a neighbor
    temp_path[i], temp_path[-(i + 1)] = temp_path[-(i + 1)], temp_path[i]
    temp_path_tuple = tuple(temp_path)

    if temp_path_tuple not in tabu_list:
        s = 0
        for k in range(nbr_villes - 1):
            a, b = temp_path[k], temp_path[k + 1]
            s += distances[a, b]

        if s < s0:
            s0 = s
            path = temp_path.copy()  # update best path

        tabu_list.append(temp_path_tuple)

    # Move to next index cyclically
    i = (i + 1) % (nbr_villes // 2)
    j -= 1

print("\nBest local path found (tabu applied):")
print(" → ".join(nom_villes[path]))
print(f"Total distance: {s0}")

print("\nAll paths registered in the tabu list:")
for idx, t_path in enumerate(tabu_list, start=1):
    city_names = " → ".join(nom_villes[list(t_path)])
    print(f"{idx:03d}: {city_names}")


#---- Recuit Simulé ----
path = np.arange(nbr_villes)
s0 = 0

# Compute initial distance
for k in range(nbr_villes - 1):
    a, b = path[k], path[k + 1]
    s0 += distances[a, b]

best = s0
best_path = path.copy()

t0 = 500
alpha = 0.99
i = 0  # index for swapping

while t0 > 0.1:  # small cutoff to avoid infinite loop
    temp_path = path.copy()
    temp_path[i], temp_path[-(i + 1)] = temp_path[-(i + 1)], temp_path[i]
    
    # Compute distance of neighbor
    s = 0
    for k in range(nbr_villes - 1):
        a, b = temp_path[k], temp_path[k + 1]
        s += distances[a, b]

    delta_e = s - s0
    
    # Accept new state if better or probabilistically worse
    if delta_e < 0 or random.random() < exp(-delta_e / t0):
        s0 = s
        path = temp_path.copy()

    # Update best found
    if s0 < best:
        best = s0
        best_path = path.copy()

    # Decrease temperature
    t0 *= alpha

    # Cycle index
    i = (i + 1) % (nbr_villes // 2)

print("\nBest local path found (Recuit Simulé):")
print(" → ".join(nom_villes[best_path]))
print(f"Total distance: {best}")