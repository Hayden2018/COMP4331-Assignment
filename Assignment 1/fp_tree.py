from copy import copy
from time import time

# Class definition for FP Tree node
class Node:

    def __init__(self, record, head_dict, parent, freq=1):
        self.c = record[0]
        self.f = freq
        self.head_dict = head_dict
        self.parent = parent
        self.next = None

        if self.c in head_dict:
            head = head_dict[self.c]
            while head.next is not None:
                head = head.next
            head.next = self
        else:
            head_dict[self.c] = self
        
        self.children = dict()
        if len(record) > 1:
            record = record[1:]
            self.children[record[0]] = Node(record, head_dict, self, freq)
        
    # Store a transaction record into the FP Tree
    def store(self, record, freq=1):
        self.f += freq
        record = record[1:]   
        if len(record) != 0:
            r = record[0]
            if r in self.children:
                self.children[r].store(record, freq)
            else:
                self.children[r] = Node(record, self.head_dict, self, freq)  


# Preprocess transaction data into the form required by FP Tree
def preprocess(transactions, minsup):

    # Count items frequency
    count = dict()
    for t, f in transactions:
        for item in t:
            if item in count:
                count[item] += f
            else:
                count[item] = f

    # Delete items that do not reach minimum support
    for item in copy(count):
        if count[item] < minsup:
            del count[item]

    # Make sure that the order of items are sorted according to their frequency
    output = list()
    for t, f in transactions:
        record = list()
        for n in t:
            if n in count:
                record.append(n)
        if len(record) != 0:
            record = sorted(record, key=lambda x: count[x], reverse=True)
            output.append((record, f))

    candidates = list(count.keys())
    candidates = sorted(candidates, key=lambda x: count[x])
    return output, candidates

# Algorithm recursively grow FP Tree to mine frequent item sets
def mine(transactions, minsup, prefix):

    transactions, candidates = preprocess(transactions, minsup)
    root_dict = dict()
    head_dict = dict()

    # Filling in the root node
    for t, f in transactions:
        r = t[0]
        if r in root_dict:
            root_dict[r].store(t, f)
        else:
            root_dict[r] = Node(t, head_dict, None, f)
        
    freq_patterns = list()
    for c in candidates:
        freq_patterns.append(prefix+[c])
        node = head_dict[c]
        conditional_base = list()
        while node is not None:
            up = node.parent
            freq = node.f
            base = list()
            while up is not None:
                base.append(up.c)
                up = up.parent
            if len(base) > 0:
                conditional_base.append((base, freq))
            node = node.next
        if len(conditional_base) > 0:
            fp = mine(conditional_base, minsup, prefix+[c]) # Recursively creating FP tree 
            freq_patterns += fp

    return freq_patterns

# Read the dataset
f = open('dataset.txt', 'r')
transactions = list()
for line in f.readlines():
    items = line.strip().split(' ')
    items = [int(i) for i in items]
    transactions.append((items, 1))

start = time() # For recording running time of the algorthm
freq_patterns = mine(transactions, 400, list())
print('Time used:', time() - start)

# Store the result in a text file
f = open('frequent.txt', 'w')
for p in freq_patterns:
    f.write(str(p) + '\n')
print('Thre are', len(freq_patterns), 'frequent itemsets in total')
