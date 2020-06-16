from time import time
import numpy as np
import matplotlib.pyplot as plt
from collections import deque

f = open('a3dataset.txt', 'r')

data = []
for line in f.readlines():
    x1, x2 = eval(line)
    data.append([x1, x2])

data = np.array(data)

def dbscan(data, eps, minpt):
    N, D = data.shape
    core = []                       # Index of core points
    neighbour = {}                  # Index of neighbour of core points
    index = np.arange(N)
    for i in range(N):
        selector = (np.linalg.norm(data - data[i], axis=1) < eps)
        if selector.sum() >= minpt:
            core.append(i)
            neighbour[i] = index[selector].tolist()

    group = [-1 for i in range(N)]
    k = 0
    for i, n in zip(core, neighbour):
        if group[i] < 0:
            stack = []
            stack.append(i)
            while len(stack) != 0:
                c = stack.pop()
                group[c] = k
                for j in neighbour[c]:
                    if (group[j] < 0) and (j in core):    
                        stack.append(j)                   # Store neighboring core point for further processing
                    else:
                        group[j] = k                      # Add border point to cluster
            k += 1
    print('There are', k, 'groups')
    return group

t = time()
group = dbscan(data, 1, 4)
print('The algorithm runs for:', time() - t)

color_map = {
    0: 'b',
    1: 'g',
    2: 'r',	
    3: 'c',
    4: 'm',
    5: 'y'
}

for i, g in enumerate(group):
    if g == -1:
        group[i] = 'black'
    else:
        group[i] = color_map[g % 6]
plt.scatter(data[:, 0], data[:, 1], c=group, s=10)
plt.show()