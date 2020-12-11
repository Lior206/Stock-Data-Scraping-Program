import datetime as dt
import time
from multiprocessing import Process
from threadManage import threadsFunction
from repairModule import repairStocksCsv
from manageModule import updateFailedProcess

if __name__ == '__main__':
    # Bool function to determine trading time
    def IsTradingTime(rightNow):
        print(rightNow)
        return 17 <= rightNow.hour < 23 or (rightNow.hour == 16 and rightNow.minute >= 30)

    # Function to set sleeping mode (turn process to blocking)
    def waitToStart(hour, mint):
        if hour < 16:
            res = ((16 - hour)*60 + (29 - mint))*60
            print(f"Wait to trading time: {res} seconds")
            time.sleep(res)

    stockKeys = ['AAPL']
    # bool, time variables
    today = dt.datetime.today().strftime("%A")
    first = True
    running = True

    # Main Process, to execute task
    if today != "Sunday" and today != "Saturday":
        while running:
            now = dt.datetime.now()
            if now.second != 0:
                first = True
            waitToStart(now.hour, now.minute)
            if IsTradingTime(now):
                if now.second < 1 and first:
                    try:
                        p = Process(target=threadsFunction, args=(stockKeys, now.year, now.month, now.day, now.hour, now.minute))
                        p.start()
                        p.join()
                        print(f"Process Executed: " + p.name)
                        # Function to repair csv file
                        repairStocksCsv(stockKeys)
                        # time.sleep(35)
                        first = False
                    except Exception as inst:
                        updateFailedProcess(now.hour, now.minute)
                        with open("logging/ErrorsSummary.txt", 'a') as f:
                            f.write(f'\nError in Main Process: ' + inst.__str__())
                        print("Error: Could not start new process")
            else:
                print("Not in trading time")
            if now.hour == 23:
                time.sleep(3660)
    else:
        print("Not in trading day")
