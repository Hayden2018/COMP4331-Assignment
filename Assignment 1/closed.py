# Read the frequent itemsets from text file
f = open('frequent.txt', 'r')
items = list()
frequency = list()
for line in f.readlines():
    if len(line) > 2:
        i, f = eval(line)
        items.append(i)
        frequency.append(f)

L = len(frequency)
closed = [True for i in range(L)] # First assume closed
for i in range(L):
    s = set(items[i])
    for j in range(L):
        if i == j:
            continue
        elif s.issubset(set(items[j])) and frequency[i] == frequency[j]:
            maximal[i] = False # Set to false if superset of same frequency found
            break              # Leave the loop earlier for speed sake

# Store the result in a text file
f = open('closed.txt', 'w')
n = 0
for i, m in zip(items, closed):
    if m:
        f.write(str(i) + '\n')
        n += 1
print('Thre are in total', n, 'closed frequent item sets')