import time,datetime
from makeOrder import sysnc,start_service

while True:
    print("start ====================>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>",datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    try:
        sysnc()
        start_service()
    except Exception as e :
        print(e)
    time.sleep(120)
