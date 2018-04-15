"""
获取求购订单的请口，暂时硬编码pubg
https://buff.163.com/api/market/goods/buy_order?game=pubg&goods_id=
756022
&page_num=1
&_=1523639198390


https://buff.163.com/api/market/goods/sell_order?game=pubg&goods_id=
756022
&page_num=1&sort_by=price&mode=&allow_tradable_cooldown=1

"""
import requests,json


def getGoodsPrice(id):
    url = "https://buff.163.com/api/market/goods/buy_order?game=pubg&goods_id="+id+"&page_num=1"
    r = requests.get(url)
    if(r.status_code != 200):
        print("buy status_code",r.status_code)
        return False
    # print(r.text)
    buy = buyprice(r.text)
    url_sell = "https://buff.163.com/api/market/goods/sell_order?game=pubg&goods_id="+id+"&page_num=1&sort_by=price&mode=&allow_tradable_cooldown=1"
    r_sell = requests.get(url_sell)
    if(r_sell.status_code!=200):
        print("sell status_code",r_sell.status_code)
        return False
    sell = sellprice(r_sell.text)
    result = {}
    result["id"] = id
    result["buy"] = buy
    result["sell"] = sell
    return  result


def buyprice(str):
    j = json.loads(str)
    a = j["data"]["items"][0]
    price = a["price"]
    num = a["num"]
    real_num = a["real_num"]
    if (num - real_num) >= 2:
        return  price
    else:
        b = j["data"]["items"][1]
        price_b = b["price"]
        return price_b

def sellprice(str):
    j = json.loads(str)
    a = j["data"]["items"][0]["price"]
    b = j["data"]["items"][1]["price"]
    if(float(a)-float(b))>0.1:
        return b
    else:
        return a

print(getGoodsPrice("756022"))