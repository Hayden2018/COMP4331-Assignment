from copy import deepcopy
from itertools import combinations
from time import time

# Class definition for Hashtree node
class Node:

    def __init__(self, max_node_size, depth, max_depth, num_child=37):
        self.size_limit = max_node_size
        self.items = list()
        self.counter = list()
        self.num_child = num_child
        self.depth = depth
        self.max_depth = max_depth
        self.children = None
        self.n = 0

    # Function for spliting the node
    def split(self):
        node = Node(self.size_limit, self.depth + 1, self.max_depth, self.num_child)
        self.children = [deepcopy(node) for i in range(self.num_child)]
        for r in self.items:
            n = r[self.depth]
            h = n % self.num_child       # Hash function
            self.children[h].store(r)
        self.items = None
        self.counter = None

    # Store a candidate itemsets into the tree
    def store(self, r):
        if self.children is None:
            self.items.append(r)
            self.counter.append(0)
            if len(self.items) > self.size_limit and self.depth < self.max_depth:
                self.split()
        else:
            n = r[self.depth]
            h = n % self.num_child        # Hash function
            self.children[h].store(r)
            
    # Process a transaction r and increase the frequency of corresponding item in the tree
    def scan(self, r):
        if len(r) < self.max_depth:
            pass
        elif self.children is None:
            back = r[self.depth:]
            front = r[:self.depth]
            for c in combinations(back, self.max_depth - self.depth):
                for i, e in enumerate(self.items):
                    if e == front + list(c):
                        self.counter[i] += 1
        else:
            i = self.depth
            while i <= (len(r) - self.max_depth + self.depth):
                n = r[i]
                h = n % self.num_child     # Hash function
                s = r[:self.depth] + r[i:]
                self.children[h].scan(s)
                i += 1

    # Iterators that iterate through the candidate itesets stored in the tree
    def traverse(self):
        if self.children is None:
            for z in zip(self.items, self.counter):
                yield z
        else:
            for c in self.children:
                for i in c.traverse():
                    yield i

# For testing purpose
if __name__ == "__main__":
    root = Node(3, 0, 3, 3)
    root.store([1, 4, 5])
    root.store([1, 3, 6])
    root.store([1, 2, 4])
    root.store([4, 5, 7])
    root.store([1, 2, 5])
    root.store([1, 5, 9])
    root.store([4, 5, 8])
    root.store([2, 3, 4])
    root.store([5, 6, 7])
    root.store([3, 4, 5])
    root.store([3, 5, 6])
    root.store([3, 5, 7])
    root.store([6, 8, 9])
    root.store([3, 6, 7])
    root.store([3, 6, 8])
    root.store([1, 2, 6])
    root.scan([1, 2, 3, 5, 6])
    for s, c in root.traverse():
        print(s, 'Count:', c)
