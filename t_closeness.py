import numpy as np
import math
import pandas as pd

def main():
    data = pd.read_csv("Lab2.csv")
    data.head()
    t = EMD_ordered_distance(data, ['Gender', 'Age', 'Marital_Status', 'Country_Birth', 'Race'], ['Household_Income'])
    print(t)
    t = divergence(data, ['Gender', 'Age', 'Marital_Status', 'Country_Birth', 'Race'], ['Household_Income'])
    print(t)
    t = pearson(data, ['Gender', 'Age', 'Marital_Status', 'Country_Birth', 'Race'], ['Household_Income'])
    print(t)
    t = sjsd(data, ['Gender', 'Age', 'Marital_Status', 'Country_Birth', 'Race'], ['Household_Income'])
    print(t)

def normalize(d, target=1.0):
    """ Normalizes a distribution. """

    raw = sum(d.values())
    factor = target/raw
    return {key:value*factor for key,value in d.items()}

def computeSensitiveAttrs(data_table, quasi_identifier, sensitive_column):
    """ List of sorted sensitive attributes."""

    eq_class, freq = np.unique(data_table[quasi_identifier + sensitive_column], return_counts=True,  axis=0)
    eq_class = np.append(eq_class, [[f] for f in freq], axis=1)
    sensitives = []
    for i in eq_class:
        if i[-2] in sensitives:
            pass
        else:
            sensitives.append(i[-2])
    sensitives.sort()
    return sensitives

def constructP(data_table, quasi_identifier, sensitive_column):
    """ Constructs the P distribution. """

    eq_class, freq = np.unique(data_table[quasi_identifier + sensitive_column], return_counts=True,  axis=0)
    eq_class = np.append(eq_class, [[f] for f in freq], axis=1)
    prior = {}
    for i in eq_class:
        if i[-2] in prior:
            prior[i[-2]] += i[-1]
        else:
            prior[i[-2]] = i[-1]

    prior = normalize(prior)
    return prior, eq_class

def constructAllQs(data_table, quasi_identifier, sensitive_column, sensitives, eq_class, prior):
    """ Constructs the Q distributions. """

    eq_class_2, freq = np.unique(data_table[quasi_identifier], return_counts=True, axis=0)
    eq_class_2 = np.append(eq_class_2, [[f] for f in freq], axis=1)
    maxT = 0

    postList = []

    for i in eq_class_2:
        post = {} # Q distribution.
        for s in sensitives:
            post[s] = 0

        for j in eq_class:
            match = True
            for k in range(len(quasi_identifier)):
                if i[k] != j[k]:
                    match = False
                    break
            if j[-2] in prior and match:
                post[j[-2]] += j[-1]

        post = normalize(post)
        postList.append(post)
    return postList

def EMD_ordered_distance(data_table, quasi_identifier, sensitive_column):
        p, eq_class = constructP(data_table, quasi_identifier, sensitive_column)
        sensitives = computeSensitiveAttrs(data_table, quasi_identifier, sensitive_column)
        qList = constructAllQs(data_table, quasi_identifier, sensitive_column, sensitives, eq_class, p)

        t_values = []
        maxT = 0

        for q in qList:
            cumm = [0]

            for s in sensitives:
                cumm.append(p[s] - q[s] + cumm[-1])

            totalSum = 0
            for c in cumm:
                totalSum += abs(c)

            t = totalSum / (len(sensitives) - 1)
            maxT = max(t, maxT)
            t_values.append(t)
        return maxT

def divergence(data_table, quasi_identifier, sensitive_column):
    p, eq_class = constructP(data_table, quasi_identifier, sensitive_column)
    sensitives = computeSensitiveAttrs(data_table, quasi_identifier, sensitive_column)
    qList = constructAllQs(data_table, quasi_identifier, sensitive_column, sensitives, eq_class, p)

    t_values = []
    maxT = 0

    for q in qList:
        t_value = 0

        for s in sensitives:
            if q[s] > 0 and p[s] > 0 and q[s] < 1 and p[s] < 1: 
                val = ((p[s] - q[s])**2) / ((p[s] + q[s])**2)
                t_value += val

        t_values.append(t_value)

        maxT = max(t_value, maxT)

    return maxT

def pearson(data_table, quasi_identifier, sensitive_column):
    p, eq_class = constructP(data_table, quasi_identifier, sensitive_column)
    sensitives = computeSensitiveAttrs(data_table, quasi_identifier, sensitive_column)
    qList = constructAllQs(data_table, quasi_identifier, sensitive_column, sensitives, eq_class, p)

    t_values = []
    maxT = 0

    for q in qList:
        t_value = 0

        for s in sensitives:
            if q[s] > 0 and p[s] > 0 and q[s] < 1 and p[s] < 1: 
                val = ((p[s] - q[s])**2) / q[s]
                t_value += val

        t_values.append(t_value)

        maxT = max(t_value, maxT)

    return maxT

def sjsd(data_table, quasi_identifier, sensitive_column):
    p, eq_class = constructP(data_table, quasi_identifier, sensitive_column)
    sensitives = computeSensitiveAttrs(data_table, quasi_identifier, sensitive_column)
    qList = constructAllQs(data_table, quasi_identifier, sensitive_column, sensitives, eq_class, p)

    t_values = []
    maxT = 0

    for q in qList:
        t_value = 0

        for s in sensitives:
            if q[s] > 0 and p[s] > 0 and q[s] < 1 and p[s] < 1: 
                t_value += p[s] * math.log(2, (2*p[s])/(p[s] + q[s]))
                t_value += q[s] * math.log(2, (2*q[s])/(p[s] + q[s]))
        t_value = t_value / 2
        t_value = math.sqrt(t_value)        

        t_values.append(t_value)

        maxT = max(t_value, maxT)

    return maxT

if __name__ == "__main__":
    main()