import numpy as np

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


class Bayes:

    def __init__(self, data, label):
        label_num = max(label) + 1         # Number of possible label values
        attr_num = data.shape[1]           # Number of attribute in data
        max_value_num = np.max(data) + 1   # Maximum number of different values in any given attribute
        self.cond_prob = np.ones([label_num, attr_num, max_value_num]) * 0.0001     # Array storing conditional probability
        self.class_prob = list()                                                    # Probability of each label class
        for i in range(label_num):
            selector = (label == i)
            s_data = data[selector]
            self.class_prob.append(len(s_data) / len(data))
            for j in range(attr_num):
                for k in range(max_value_num):
                    selector = (s_data[:, j] == k)
                    self.cond_prob[i, j, k] += np.sum(selector) / len(selector)


    def predict(self, x):
        label_prob = list()
        for i, c in enumerate(self.class_prob):
            prob = c
            for j, k in enumerate(x):
                prob *= self.cond_prob[i, j, k]
            label_prob.append(prob)
        return np.argmax(label_prob)


if __name__ == '__main__':
    data, label, attr_map = load_data()
    n = round(len(data) * 0.8)
    train_data = data[:n]
    train_label = label[:n]
    val_data = data[n:]
    val_label = label[n:]
    classifier = Bayes(train_data, train_label)

    correct = 0
    for da, la in zip(val_data, val_label):
        y = classifier.predict(da)
        if y == la:
            correct += 1

    acc = correct / len(val_data)
    print('Validation accuracy:', acc)

    test_data = load_test(attr_map)
    label2id = attr_map[-1]
    id2label = {v: k for k, v in label2id.items()}

    f = open('bayesPredict.txt', 'w')
    for da in test_data:
        y = classifier.predict(da)
        y = id2label[y]
        f.write(y + '\n')
    f.close()