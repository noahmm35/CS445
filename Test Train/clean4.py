import csv

# open file
with open('alcoholism_traintest.csv', 'r') as file:

    reader = csv.reader(file)

    # new list to hold clean data
    cleanData = []

    l=0

    # loop over every row
    for row in reader:

        #skip column titles
        if(l==0):
            l=1
            continue

        # do not include rows w/ missing values
        if not all(row):
            continue

        # remove all rows with -999 cuz boo
        if "-999" in row:
            del row
            continue
        
        # clean up the rows
        # anything that was not 1, 0, -1 was assigned a new value below
        cleanRow = []
        for val in row[1:]:
            val = int(val)
            if val==1 or val==-1 or val==0:
                cleanRow.append(val)
            elif val<3:
                cleanRow.append(0)
            else:
                cleanRow.append(1)

        # add row to list of 'clean rows'
        cleanData.append(cleanRow)

# copy clean data into new CSV
with open('cleanData.csv', 'w', newline='') as file:

    writer = csv.writer(file)
    for row in cleanData:
        writer.writerow(row)