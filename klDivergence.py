import BeliefDistributionSetup as bds

def klDivergence(data_table, quasi_identifier, sensitive_column):
    setup = bds.Setup(data_table_name, quasi_identifier, sensitive_column)
    p = setup.p

    t_values = []
    maxT = 0

    for q in qList:
        t_value = 0

        for s in setup.sensitives:
            if q[s] > 0:
                t_value = p[s] * math.log(p[s] / q[s])

        t_values.append(t_value)

        maxT = max(t_value, maxT)

    return maxT