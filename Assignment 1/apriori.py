from copy import copy
from itertools import product
from time import time
import re

# Import the hash tree class written in another file
from hashtree import Node

# Restore prime representations to their original form
def to_normal(X, map_dict):
    output = list()
    for r in X:
        r = [map_dict[i] for i in r]
        output.append(r)
    return output

# Helper function return the product of all elements in a list
def multiply(x):
    m = 1
    for i in x:
        if i != 0:
            m = m * i
    return m

# Joining frequent itemsets of size n with frequent elements to produce candidate itemsets of size n + 1
# Modular of prime product is used for subset checking
def increment(base, candidates):
    output = list()
    exist = set()
    for b in base:
        bm = multiply(b)
        for c in candidates:
            if bm % c == 0:
                continue
            elif bm * c not in exist:
                x = sorted(b + [c])
                output.append(x)
                exist.add(bm * c)
    return output


# Apply a mapping dictionary to dataset
def preprocess(transactions, map_dict):
    output = list()
    for t in transactions:
        record = list()
        for n in t:
            if n in map_dict:
                record.append(map_dict[n])
        if len(record) != 0:
            output.append(record)
    return output


# The apriori algortihm using hash tree
def apriori(transactions, primes, minsup):

    # Count items frequency
    count = dict()
    for t in transactions:
        for item in t:
            if item in count:
                count[item] += 1
            else:
                count[item] = 1

    # Delete items that do not reach minimum support
    for item in copy(count):
        if count[item] < minsup:
            del count[item]

    # Create frequent itemset of size one
    candidates = sorted(count.keys())
    freq_counts = [count[c] for c in candidates]

    # Create mapping to prime numbers
    map_dict = {c: p for c, p in zip(candidates, primes)}
    inv_map = {v: k for k, v in map_dict.items()}

    # Apply prime mapping to dataset
    candidates = [map_dict[c] for c in candidates]
    base = [[c] for c in candidates]
    data = preprocess(transactions, map_dict)
    
    size = 1
    freq_patterns = copy(base)
    while True:
        size += 1
        frequent = list()
        counts = list()
        base = increment(base, candidates)  # generate new candidate itemsets
        root = Node(12, 0, size)            # Create the root node of the hash tree
        for b in base:
            root.store(b)
        for record in data:                 # Scan the data base
            root.scan(record)
        for item, freq in root.traverse():  # Iterate through the hash tree check candidate frequency
            if freq >= minsup:         
                frequent.append(item)
                counts.append(freq)
        if len(frequent) == 0:
            break                       # Break the loop if no more frequent item sets generated
        else:
            freq_patterns += frequent
            freq_counts += counts
            base = frequent             # prepare for larger itemsets candidate generation

    # Convert back to original form
    freq_patterns = to_normal(freq_patterns, inv_map)
    return freq_patterns, freq_counts


# Read the dataset
f = open('dataset.txt', 'r')
transactions = list()
for line in f.readlines():
    items = line.strip().split(' ')
    items = [int(i) for i in items]
    transactions.append(items)

# Read pre-stored prime number
f = open('primes.txt', 'r')
primes = list()
for line in f.readlines():
    prime = re.split('\s+', line.strip())
    prime = [int(p) for p in prime]
    primes += prime

start = time() # For recording running time of the algorthm
freq_patterns, freq_counts = apriori(transactions, primes, 400)
print('Time used:', time() - start)

# Store the result in a text file
f = open('frequent.txt', 'w')
for p in zip(freq_patterns, freq_counts):
    f.write(str(p) + '\n')
print('Thre are', len(freq_patterns), 'frequent itemsets in total')