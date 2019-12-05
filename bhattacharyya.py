import BeliefDistributionSetup as bds

def bhattacharyya(data_table, quasi_identifier, sensitive_column):
    setup = bds.Setup(data_table_name, quasi_identifier, sensitive_column)
    p = setup.p

    t_values = []
    maxT = 0

    for q in qList:
        t_value = 0

        for s in setup.sensitives:
            t_value += math.sqrt(p[s] * q[s])

        t_value = math.log(t_value) * -1
    
        t_values.append(t_value)

        maxT = max(t_value, maxT)

    return maxT