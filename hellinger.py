import BeliefDistributionSetup as bds

def hellinger(data_table, quasi_identifier, sensitive_column):
    setup = bds.Setup(data_table_name, quasi_identifier, sensitive_column)
    p = setup.p

    t_values = []
    maxT = 0

    for q in qList:
        t_value = 0

        for s in setup.sensitives:
            t_value = (math.sqrt(p[s]) - math.sqrt(q[s])) ** 2
            
            t_value = math.sqrt(t_value) * 1 / math.sqrt(2)

            t_values.append(t_value)

            maxT = max(t_value, maxT)

        return maxT