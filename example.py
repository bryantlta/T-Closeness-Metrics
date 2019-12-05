import earth_movers_distance as emd

def main():
    t = emd.EMD_ordered_distance("Lab2.csv", ['Gender', 'Age', 'Marital_Status', 'Country_Birth', 'Race'], ['Household_Income'])
    print(t)


if __name__ == "__main__":
    main()