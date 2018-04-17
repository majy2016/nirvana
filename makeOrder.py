"""
0. 获取goods_id 最合适的 （出售价格 - 求购价格 = 利润）
1. 获取登录session
2. 获取我的背包列表
3. 获取我的出售列表
4. 获取我的求购列表
5. goods_id 是否在求购列表 => 求购
6. goods_id 是否在出售列表 => 出售
"""

import until,json
from bs4 import BeautifulSoup

def start():
    sql = "select * from goods_sell_buy"
    x = until.sqlite_select(sql)
    for i in x:
        start(i)


def make(rows):

    goods_id = rows[0]

    goods_price = getGoodsPrice(goods_id)
    if goods_price is False:
        return "1"
    list_back_goods = getBackpack()
    if list_back_goods is False:
        return "2"

    #判断背包里有没有
    for i in list_back_goods:
        if(i["goods_id"] == goods_id):
            #todo
            break

    list_sell_goods = getSellList()
    if list_sell_goods is False:
        return "3"

    for (k,v) in list_sell_goods:
        if (k == goods_id):
            #todo
            break
    list_buy_goods = 0




# 查询售卖列表
def getSellList():
    result = {}
    url = "https://buff.163.com/market/sell_order/on_sale?game=pubg"
    headers = {
        "X-CSRFToken": "ImRjOTBjNDIzNzkyZDBkNTA5ZjYzZjUyMjdmODU3OGJmNzI4M2Y1YzMi.DbWb7Q.DX1hDwcW0RGjKN5-d5VJyzlR5IE"
    }
    r = until.make_request(url,"GET",None,headers)
    if r is None:
        until.make_log("获取求购列表失败")
        return False
    bs = BeautifulSoup(r, "lxml")
    list = bs.findAll("li", {"class": "salable"})
    for i in list:
        result[i["data-goodsid"]] = [i["data-orderid"],i["data-price"]]
    return result


# 查询背包列表
def getBackpack():
    url = "https://buff.163.com/api/market/backpack?game=pubg&page_num=1&_=1523930800587"
    headers = {
        "Referer": "https://buff.163.com/market/buy_order/wait_supply?game=pubg"
       }
    r = until.make_request(url,"GET",None,headers)
    if r is None:
        until.make_log("获取背包列表失败")
        return False
    j = json.loads(r)
    return j["data"]["items"]

#获取价格
def getGoodsPrice(goods_id):

    url_buy = "https://buff.163.com/api/market/goods/buy_order?game=pubg&goods_id=" + goods_id + "&page_num=1"
    r_buy = until.make_request(url_buy,"GET",None,None)
    if r_buy is None:
        until.make_log("获取goods_id : %s 求购价格失败 ."%goods_id)
        return False
    url_sell = "https://buff.163.com/api/market/goods/sell_order?game=pubg&goods_id=" + id + "&page_num=1&sort_by=price&mode=&allow_tradable_cooldown=1"
    r_sell = until.make_request(url_sell, "GET",None,None)
    if r_sell is None:
        until.make_log("获取goods_id : %s 出售价格失败 ."%goods_id)
        return False
    buy_price = buyprice(r_buy)
    sell_price = sellprice(r_sell)
    until.make_log("goods_id: %s ,求购价格：%s ,出售价格: %s" % (goods_id,buy_price,sell_price))
    return {"goods_id":goods_id,"buy_price":buy_price,"sell_price":sell_price}

def buyprice(str):
    j = json.loads(str)
    a = j["data"]["items"][0]
    price = a["price"]
    num = a["num"]
    real_num = a["real_num"]
    if (num - real_num) >= 2:
        return price
    else:
        b = j["data"]["items"][1]
        price_b = b["price"]
        return price_b

def sellprice(str):
    j = json.loads(str)
    a = j["data"]["items"][0]["price"]
    b = j["data"]["items"][1]["price"]
    if (float(a) - float(b)) > 0.1:
        return b
    else:
        return a