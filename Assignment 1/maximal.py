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
maximal = [True for i in range(L)] # First assume maxial
for i in range(L):
    s = set(items[i])
    for j in range(L):
        if i == j:
            continue
        elif s.issubset(set(items[j])):
            maximal[i] = False # Set to false if frequent superset found
            break              # Leave the loop earlier for speed sake

# Store the result in a text file
f = open('maximal.txt', 'w')
n = 0
for i, m in zip(items, maximal):
    if m:
        f.write(str(i) + '\n')
        n += 1
print('Thre are in total', n, 'maximal frequent item sets')