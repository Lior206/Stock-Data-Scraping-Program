import datetime as dt
import csv
import os
import requests
import json
from dataParser import Surgent


# Function to update request status
def updateCode(code, index, stockKey):
    if code != 200:
        with open(f"logging/Requests Codes.txt", 'a') as f:
            with open("jsons/Errors.json", 'r') as j:
                data = json.loads(j.read())
                massage = f'\n{code} , {index} , {stockKey}, ' + data[f'{code}']
                f.write(massage)


# Function to get urls
def urls(stockKey):
    return f"https://finance.yahoo.com/quote/{stockKey}?p={stockKey}"


# Function to check csv file exist
def checkExistCsvFile(stockKey):
    if not os.path.exists(f'StockCsv/{stockKey}.csv'):
        with open(f'StockCsv/{stockKey}.csv', 'w') as f:
            writer = csv.writer(f, delimiter=',', lineterminator='\n')
            writer.writerow(['Date', 'Price', 'Change', 'P_Change', 'Open', 'Volume',
                            'Avg_Volume', 'Market_Cap', 'Beta', 'PE_Ratio', 'EPS'])


# Algorithm to send the http requests
def worker(stockKey, year, month, day, hour, minute):
    try:
        t = dt.time(hour, minute)
        d = dt.date(year, month, day)
        index = dt.datetime.combine(d, t)
        checkExistCsvFile(stockKey)
        html_val = getHtmlStr(urls(stockKey), index, stockKey)
        finder = Surgent(index)
        finder.feed(html_val)
        data = finder.getData(index)
        putDataInCsvFile(stockKey, data, index)
    except Exception as inst:
        with open(f"logging/ErrorsSummary.txt", 'a') as f:
            f.write(f'\nError: at worker {index}, with {stockKey} :' + inst.__str__())
        print("Error: can't crawl page")


# Function to put data in tmp csv files
def putDataInCsvFile(stockKey, data, index):
    try:
        with open(f"StockCsv/{stockKey}.csv", 'a') as f:
            writer = csv.writer(f, delimiter=',', lineterminator='\n')
            writer.writerow(data)
    except Exception as inst:
        with open(f"logging/ErrorsSummary.txt", 'a') as f:
            f.write(f'\nError: at putDataInCsvFile in {index}, with {stockKey} :' + inst.__str__())
        print("Error: can't crawl page")


# Function to get http request
def reqFunction(url, index, stockKey):
    try:
        response = requests.get(url)
        updateCode(response.status_code, index, stockKey)
        return response.content.decode('utf-8')
    except Exception as inst:
        with open(f"logging/ErrorsSummary.txt", 'a') as f:
            f.write(f'\nError: at reqFunction in {index}, with {stockKey} : ' + inst.__str__())
        print("Error: can't crawl page")


# Function to check and return the html code
def getHtmlStr(url, index, stockKey):
    try:
        html_val = reqFunction(url, index, stockKey)
        if html_val == "":
            raise ValueError
        return html_val
    except ValueError:
        with open(f"logging/ErrorsSummary.txt", 'a') as f:
            f.write(f'\nError: at getHtmlStr in {index}, with {stockKey}')
        print("Error: can't crawl page after running 4 functions")
