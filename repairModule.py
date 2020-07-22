import csv
import threading as th
from manageModule import convertHour, convertMinute, replaceHourMinuteInRow

# Stock keys
stockKeys = ['KO', 'T', 'PFE', 'GE', 'ABT',
               'VZ', 'SBUX', 'NKE', 'BAC', 'WFC',
               'CSCO', 'INTC', 'BMY', 'MRK', 'CELG', 'AMD',
               'MDCO', 'NIO', 'ACB', 'ZNGA', 'SCHW',
               'AMTD', 'TEVA', 'S', 'SNAP', 'F',
               'TIF', 'FCX', 'NOK', 'PDD', 'AAPL',
               'TSLA', 'MSFT', 'DIS', 'GOOG', 'C',
               'ADBE', 'MA', 'JNJ', 'CRM', 'UBER',
               'GS', 'BA', 'AVGO', 'COP', 'CAT',
               'QCOM', 'PYPL', 'LMT', 'IBM', 'MS',
             'PM', 'MMM', 'MCD', 'AIG', 'JPM']


# function to check each minute
def checkIfNeedToRepair(firstList, secondList):
    firstHour = convertHour(firstList)
    firstMinute = convertMinute(firstList)
    secondHour = convertHour(secondList)
    secondMinute = convertMinute(secondList)
    return subtractHours(firstHour, firstMinute, secondHour, secondMinute)


# function to add minute to the time value
def addOneMinute(hour, minute):
    m = minute + 1
    if m > 59:
        return hour + 1, 0
    else:
        return hour, m


# function to repair current gap in data set
def repairMatrixFunction(currentMatrix, index, sub, hour, minute):
    h, m = addOneMinute(hour, minute)
    newMatrix = currentMatrix[0:-index]
    while sub != 0:
        lst = currentMatrix[-index - 1].copy()
        newMatrix.append(replaceHourMinuteInRow(lst, h, m))
        sub -= 1
        h, m = addOneMinute(h, m)
    newMatrix += currentMatrix[-index:]
    return newMatrix


def subtractHours(firstHour, firstMinute, secondHour, secondMinute):
    return (firstHour - secondHour) * 60 + (firstMinute - secondMinute)


def updateFixesLogFile(stockKey, hour, minute):
    with open('logging/Fixes Amount.txt.txt', 'a') as f:
        f.write(f"\n{hour}:{minute} {stockKey} Fixed")


# repair last 10 minutes
def repairStockCsvFile(stockKey):
    global currentMatrix
    with open(f'StockCsv/{stockKey}.csv', 'r') as base_r:
        currMatrix = list(csv.reader(base_r))
        if len(currMatrix) > 10:
            for index in list(range(1, 11)):
                sub = checkIfNeedToRepair(currMatrix[-index], currMatrix[-index - 1])
                if sub != 1:
                    hour = convertHour(currMatrix[-index - 1])
                    minute = convertMinute(currMatrix[-index - 1])
                    updateFixesLogFile(stockKey, hour, minute)
                    currMatrix = repairMatrixFunction(currMatrix, index, sub - 1, hour, minute)
    with open(f'StockCsv/{stockKey}.csv', 'w', newline="") as base_r:
        wr = csv.writer(base_r)
        wr.writerows(currMatrix)


# function to execute threads to repair csv files
def repairStocksCsv(stockKeys):
    for stock_key in stockKeys:
        t1 = th.Thread(target=repairStockCsvFile, args=stock_key)
        t1.start()
    print("Finish Repairing Csv Files")


