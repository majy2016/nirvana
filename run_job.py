import time,datetime
from makeOrder import start

while True:
    print("start ====================>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>",datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    start()
    time.sleep(300)
