import csv


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


# function to clean csv files
def cleanCsvFile(stock_str):
    with open(f'StockCsv/{stock_str}.csv', 'w') as f:
        writer = csv.writer(f, delimiter=',', lineterminator='\n')
        writer.writerow(
            ['Date', 'Price', 'Change', 'P_Change', 'Open', 'Volume', 'Avg_Volume', 'Market_Cap', 'Beta', 'PE_Ratio',
             'EPS'])


# call cleaning func to each stock key
def cleanFiles(stockKeys):
    for stockKey in stockKeys:
        cleanCsvFile(stockKey)
    with open(f'logging/ErrorsSummary.txt', 'w') as f:
        pass
    with open(f'logging/Failed Processes.txt', 'w') as f:
        pass
    with open(f'logging/Requests Codes.txt', 'w') as f:
        pass
    with open(f'logging/Fixes Amount.txt', 'w') as f:
        pass


# extract hour from row list
def convertHour(row):
    return int(row[0][11:13])


# extract minute from row list
def convertMinute(row):
    return int(row[0][14:16])


# function to replace hour and minute in row list
def replaceHourMinuteInRow(row, hour, minute):
    newDate = row[0]
    if hour > 9:
        newHour = str(hour)
    else:
        newHour = '0' + str(hour)
    if minute > 9:
        newMinute = str(minute)
    else:
        newMinute = '0' + str(minute)
    newDate = newDate[0:11] + newHour + ':' + newMinute + newDate[16:]
    row[0] = newDate
    return row


# function to update all failed processes in main 1
def updateFailedProcess(hour, minute):
    with open('logging/Failed Processes.txt', 'a') as f:
        f.write(f"\n{hour}:{minute} Faild")

#cleanFiles(stockKeys)