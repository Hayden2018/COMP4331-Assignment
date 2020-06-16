from time import time
import numpy as np
import matplotlib.pyplot as plt

f = open('a3dataset.txt', 'r')

data = []
for line in f.readlines():
    x1, x2 = eval(line)
    data.append([x1, x2])

data = np.array(data)

def k_mean(data, k):
    np.random.seed(int(time()))
    N, D = data.shape
    high = [np.max(data[:, i]) for i in range(D)]
    low = [np.min(data[:, i]) for i in range(D)]
    means = [np.random.uniform(low, high) for i in range(k)]   # Randomly initialize means
    means = np.array(means)
    
    group = np.zeros(N)
    distance = np.zeros([N, k])

    while True:
        for i in range(k):
            distance[:, i] = np.linalg.norm(data - means[i], axis=1)  # Compute distance between mean and data points
        new_group = np.argmin(distance, axis=1)                       # Assign data points to cluster
        if (new_group != group).sum() == 0:
            return group                                              # End algorithm if no more changes in clustering
        else:
            group = new_group
            for j in range(k):
                selector = (group == j)
                means[j, :] = np.mean(data[selector], axis=0)         # Update the means

t = time()
group = k_mean(data, 9)
print('The algorithm runs for:', time() - t)

plt.scatter(data[:, 0], data[:, 1], c=group, s=10)
plt.show()