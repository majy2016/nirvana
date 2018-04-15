"""
获取求购订单的请口，暂时硬编码pubg
https://buff.163.com/api/market/goods/buy_order?game=pubg&goods_id=
756022
&page_num=1
&_=1523639198390

"""
import requests,json


def getGoodsPrice(id):
    url = "https://buff.163.com/api/market/goods/buy_order?game=pubg&goods_id="+id+"&page_num=1"
    r = requests.get(url)
    if(r.status_code != 200):
        print("status_code",r.status_code)
        return False
    print(r.text)


def buyprice(str):
    j = json.loads(str)
    a = j["data"]["items"][0]
    price = a["price"]
    num = a["num"]
    real_num = ["real_num"]
    if (real_num - num) > 3:
        return  price


getGoodsPrice("756022")