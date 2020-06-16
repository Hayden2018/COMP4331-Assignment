import numpy as np
from copy import copy

def load_data():
    f = open('train.csv', 'r')
    line = f.readline()
    headers = line.split(',')
    num_attr = len(headers)
    attr_map = [dict() for i in range(num_attr)]   # Mapping attribute strings to integers numpy use

    data = list()
    while True:
        line = f.readline()
        if len(line) == 0:
            break
        attrs = line.strip().split(',')
        for i in range(num_attr):
            if attrs[i] not in attr_map[i]:
                attr_map[i][attrs[i]] = len(attr_map[i])
            attrs[i] = attr_map[i][attrs[i]]
        data.append(attrs)

    f.close()
    data = np.array(data)
    label = data[:, -1]                 # The last column is the label
    return data[:, :-1], label, attr_map


def load_test(attr_map):
    f = open('test.csv', 'r')
    f.readline()
    num_attr = len(attr_map) - 1        # Exclude label

    test_data = list()
    while True:
        line = f.readline()
        if len(line) == 0:
            break
        attrs = line.strip().split(',')
        for i in range(num_attr):
            attrs[i] = attr_map[i][attrs[i]]
        test_data.append(attrs)

    f.close()
    test_data = np.array(test_data)
    return test_data


class Tree:

    def __init__(self, data, label, usage=None, value_num=None, split_info=False):
        
        self.prediction = dict()
        self.children = dict()
        self.split_attr = 0
        info = self.entropy(label)
        if info == 0:
            self.prediction = int(label[0])
            return 
        
        if usage is None or value_num is None:
            value_num = list()
            usage = list()
            for i in range(data.shape[1]):
                usage.append(0)
                value_num.append(max(data[:, i]) + 1)

        gain = list()
        for i, used in enumerate(usage):    # Loop through all attribute
            if used == 0:
                attr = data[:, i]
                v = value_num[i]            # Number of possible values in the the attribute
                e = 0                       # Entropy for this attribute
                for j in range(v):
                    selector = (attr == j)        # Boolean array indexing record with given value in the attribute
                    s_label = label[selector]
                    e += len(s_label) / len(attr) * self.entropy(s_label)
                if split_info:
                    gain.append(info - e)
                else:
                    gain.append((info - e) / (self.entropy(attr) + 0.01))
            else:
                gain.append(0)
        
        self.split_attr = np.argmax(gain)
        usage[self.split_attr] = 1
        attr = data[:, self.split_attr]
        v = value_num[self.split_attr]            # Number of possible values in the given attribute
        for i in range(v):
            selector = (attr == i)
            s_data = data[selector]               # Boolean array indexing record with given value in attribute i
            s_label = label[selector]
            if len(s_label) == 0:
                values, counts = np.unique(label, return_counts=True)
                self.prediction[i] = values[np.argmax(counts)]
            else:
                self.children[i] = Tree(s_data, s_label, copy(usage), value_num, split_info)

    def predict(self, x):
        if isinstance(self.prediction, int):
            return self.prediction
        else:
            s = x[self.split_attr]
            if s in self.children:
                return self.children[s].predict(x)
            else:
                return self.prediction[s]

    @staticmethod
    def entropy(x):
        values, counts = np.unique(x, return_counts=True)
        e = 0
        for c in counts:
            f = c / len(x)
            e -= f * np.log2(f)
        return e


if __name__ == '__main__':
    data, label, attr_map = load_data()
    n = round(len(data) * 0.8)
    train_data = data[:n]
    train_label = label[:n]
    val_data = data[n:]
    val_label = label[n:]
    tree = Tree(train_data, train_label, split_info=True)

    correct = 0
    for da, la in zip(val_data, val_label):
        y = tree.predict(da)
        if y == la:
            correct += 1

    acc = correct / len(val_data)
    print('Validation accuracy:', acc)

    test_data = load_test(attr_map)
    label2id = attr_map[-1]
    id2label = {v: k for k, v in label2id.items()}

    f = open('treePredict.txt', 'w')
    for da in test_data:
        y = tree.predict(da)
        y = id2label[y]
        f.write(y + '\n')
    f.close()