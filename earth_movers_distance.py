import BeliefDistributionSetup as bds

def EMD_ordered_distance(data_table_name, quasi_identifier, sensitive_column):
        setup = bds.Setup(data_table_name, quasi_identifier, sensitive_column)
        t_values = []
        maxT = 0

        for q in setup.qList:
            cumm = [0]

            for s in setup.sensitives:
                cumm.append(setup.p[s] - q[s] + cumm[-1])

            totalSum = 0
            for c in cumm:
                totalSum += abs(c)

            t = totalSum / (len(setup.sensitives) - 1)
            maxT = max(t, maxT)
            t_values.append(t)
        return maxT