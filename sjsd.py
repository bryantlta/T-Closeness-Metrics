import BeliefDistributionSetup as bds

def sjsd(data_table, quasi_identifier, sensitive_column):
    setup = bds.Setup(data_table_name, quasi_identifier, sensitive_column)
    p = setup.p

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