import BeliefDistributionSetup as bds

def divergence(data_table, quasi_identifier, sensitive_column):
    setup = bds.Setup(data_table_name, quasi_identifier, sensitive_column)
  
    t_values = []
    maxT = 0

    for q in setup.qList:
        t_value = 0

        for s in sensitives:
            if q[s] > 0 and setup.p[s] > 0 and q[s] < 1 and setup.p[s] < 1: 
                val = ((setup.p[s] - q[s])**2) / ((setup.p[s] + q[s])**2)
                t_value += val

        t_values.append(t_value)

        maxT = max(t_value, maxT)

    return maxT