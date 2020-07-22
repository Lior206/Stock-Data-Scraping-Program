import threading as th
from algoModule import worker


# Function to execute threads
def threadsFunction(stockKeys, year, month, day, hour, minute):
    for stockKey in stockKeys:
        try:
            thread = th.Thread(target=worker, args=(stockKey, year, month, day, hour, minute))
            thread.start()
            print(f"Task Executed: {th.current_thread()}")
        except Exception as inst:
            with open(f"logging/ErrorsSummary.txt", 'a') as f:
                f.write(f'\nError: ' + inst.__str__())
            print(f'\nError: Could not start new theard')
