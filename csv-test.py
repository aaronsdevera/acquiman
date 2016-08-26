def getCol(col_name):
    import csv
    tmp = []
    with open('acquire-list.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            tmp.append(row[col_name])
    return tmp

