import pandas as pd
import numpy as np
import math

dataset = pd.read_csv("../data.csv")
features = [feat for feat in dataset]
features.remove("weather")

class Input:
    def __init__(self, temp, humidity, wind):
        self.temp = temp
        self.humidity = humidity
        self.wind = wind

class Node:
    def __init__(self):
        self.children = []
        self.value = ""
        self.isLeaf = False
        self.pred = ""


def entropy(data):
    sunny = 0.0
    rain = 0.0
    overcast = 0.0
    for _, row in data.iterrows():
        if row["weather"] == "Sunny":
            sunny += 1
        elif row["weather"] == "Rain":
            rain += 1
        else:
            overcast += 1
    p_sunny = sunny / (sunny + rain + overcast)
    p_rain = rain / (sunny + rain + overcast)
    p_overcast = overcast /(sunny + rain + overcast)
    if(p_sunny == 0.0 or p_rain == 0.0 or p_overcast == 0.0) and (p_overcast == 1.0 or p_rain == 1.0 or p_sunny == 1.0):
        return 0
    elif (p_sunny == 0.0 and p_overcast != 0.0 and p_rain != 0.0):
        return -1 * (p_rain * math.log2(p_rain) + p_overcast * math.log2(p_overcast))
    elif (p_sunny != 0.0 and p_overcast == 0.0 and p_rain != 0.0):
        return -1 * (p_rain * math.log2(p_rain) + p_sunny * math.log2(p_sunny))
    elif (p_sunny != 0.0 and p_overcast != 0.0 and p_rain == 0.0):
        return -1 * (p_overcast * math.log2(p_overcast) + p_sunny * math.log2(p_sunny))
    else:
        return -1 * (p_rain * math.log2(p_rain) + p_overcast * math.log2(p_overcast) + p_sunny * math.log2(p_sunny))

def info_gain(examples, attr):
    uniq = np.unique(examples[attr])
    gain = entropy(examples)
    for u in uniq:
        subdata = examples[examples[attr] == u]
        sub_e = entropy(subdata)
        gain -= (float(len(subdata)) / float(len(examples))) * sub_e
    return gain

def ID3(examples, attrs):
    root = Node()
    max_gain = 0.0
    max_feat = ""
    for feature in attrs:
        gain = info_gain(examples, feature)
        if gain > max_gain:
            max_gain = gain
            max_feat = feature
    root.value = max_feat
    uniq = np.unique(examples[max_feat])
    for u in uniq:
        #print(u)
        subdata = examples[examples[max_feat] == u]
        if entropy(subdata) == 0.0:
            newNode = Node()
            newNode.isLeaf = True
            newNode.value = u
            newNode.pred = np.unique(subdata["weather"])
            root.children.append(newNode)
        else:
            dummyNode = Node()
            dummyNode.value = u
            new_attrs = attrs.copy()
            new_attrs.remove(max_feat)
            child = ID3(subdata, new_attrs)
            dummyNode.children.append(child)
            root.children.append(dummyNode)

    return root


def classify(Root: Node, New):
    for child in Root.children:
        if child.value == New[Root.value]:
            if child.isLeaf:
                print("Predicted Label for new example", New, " is:", child.pred)
                exit()
            else:
                classify(child.children[0], New)

def printTree(root: Node, depth=0):
    for i in range(depth):
        print("\t", end="")
    print(root.value, end="")
    if root.isLeaf:
        print(" -> ", root.pred)
    print()
    for child in root.children:
        printTree(child, depth + 1)

root = ID3(dataset, features)
print("Temp: ")
temp = input()
print("Humidity: ")
humidity = input()
print("Wind: ")
wind = input()
new = {"temp": temp, "humidity": humidity, "wind": wind}
classify(root, new)