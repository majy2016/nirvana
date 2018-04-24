import time,datetime
from makeOrder import start

while True:
    print("start ====================>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>",datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    try:
        start()
    except Exception as e:
        print("运行异常 ！",e)
    time.sleep(210)
