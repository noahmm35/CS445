import csv

# open file
with open('cleanData.csv', 'r') as file:
    reader = csv.reader(file)

    currRow = 0
    testRows = []
    trainRows = []

    # seperate data into 80/20 test train split
    for row in reader:
    
        # 20% into test
        if currRow % 5 == 0:
            testRows.append(row)
        # 80% into train
        else:
            trainRows.append(row)
        
        currRow += 1

threshold = 4.5
initWeight = 0.5
step = 0.1
rounds = 5

#find location of answer within a given row
answer = len(trainRows[1])-1

perceptrons = []

#let the training commence!
for i in range(rounds):
    if i==0:
        for j in range(len(trainRows[1])-1):
            perceptrons.append(initWeight)

    newPerceptrons = perceptrons.copy()

    for row in trainRows:
        output = 0
        ans = int(row[answer])

        for i in range(len(row)-1):
            output = output + (int(row[i]) * newPerceptrons[i])

        if output > threshold:
            predict = 1
        else:
            predict = 0

        if predict == ans:
            continue

        #prediction was wrong
        elif predict < ans: # understimate
            for j in range(len(row)-1):
                if int(row[j]) == 1:
                    newVal = newPerceptrons[j] + step
                    newPerceptrons[j] = round(newVal,2)
        else: # overestimate
            for j in range(len(row)-1):
                if int(row[j]) == 1:
                    newVal = newPerceptrons[j] - step
                    newPerceptrons[j] = round(newVal,2)
            
    #check for convergence
    if(newPerceptrons == perceptrons):
        break
    else:
        perceptrons = newPerceptrons.copy()
#print(perceptrons)


#time to test
predPos = 0

for test in testRows:
    testOutput = 0
    testAns = int(test[answer])

    for n in range(len(test)-1):
        testOutput = testOutput + (int(test[n]) * perceptrons[n])

    if testOutput > threshold:
        predict = 1
    else:
        predict = 0

    if predict == testAns:
        predPos += 1
    else:
        continue

# print(len(testRows))
# print(predPos)

with open('weights.txt', 'w') as file:
    file.write(str(threshold))
    file.write('\n')

    for p in perceptrons:
        file.write(str(p))
        file.write('\n')