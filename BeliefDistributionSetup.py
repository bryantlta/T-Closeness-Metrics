import numpy as np
import math
import pandas as pd
import matplotlib.pyplot as plt 

class Setup:
    def __init__(self, data_table_name, quasi_identifier, sensitive_column):
        self.data = pd.read_csv(data_table_name)
        self.data.head()
        
        self.p, self.eq_class = self.constructP(self.data, quasi_identifier, sensitive_column)
        self.sensitives = self.computeSensitiveAttrs(self.data, quasi_identifier, sensitive_column)
        self.qList = self.constructAllQs(self.data, quasi_identifier, sensitive_column, self.sensitives, self.eq_class, self.p)
    
    def normalize(self, d, target=1.0):
        """ Normalizes a distribution. """

        raw = sum(d.values())
        factor = target/raw
        return {key:value*factor for key,value in d.items()}

    def computeSensitiveAttrs(self, data_table, quasi_identifier, sensitive_column):
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

    def constructP(self, data_table, quasi_identifier, sensitive_column):
        """ Constructs the P distribution. """

        eq_class, freq = np.unique(data_table[quasi_identifier + sensitive_column], return_counts=True,  axis=0)
        eq_class = np.append(eq_class, [[f] for f in freq], axis=1)
        prior = {}
        for i in eq_class:
            if i[-2] in prior:
                prior[i[-2]] += i[-1]
            else:
                prior[i[-2]] = i[-1]

        prior = self.normalize(prior)
        return prior, eq_class

    def constructAllQs(self, data_table, quasi_identifier, sensitive_column, sensitives, eq_class, prior):
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

            post = self.normalize(post)
            postList.append(post)
        return postList