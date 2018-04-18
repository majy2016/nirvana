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
    sql = "select * from goods_sell_buy WHERE status = 1"
    x = until.sqlite_select(sql)
    for i in x:
        #预处理
        make(i)
        price = getGoodsPrice(i[0])
        # buy_order 为空才求购
        if price["sell_price"] >= i[5] and i[2] is None:
            #求购
            goods_id = i[0]
            price = price["buy_price"]
            num = 1
            pay_method = "3"
            r = createBuyOrder(goods_id, price, num, pay_method)
            print(type)
            print(r)
            if r["code"] =="OK":
                s = r["data"]["id"]+"|"+str(price)
                sql = "update goods_sell_buy set buy_order = %s WHERE goods_id = %d"%(s,goods_id)
                until.sqlite_update(sql)
                until.make_log("发布goods_id：%s 求购成功，price :%f" %(goods_id,price))
    # 上架
    sell()
    #出售调价
    sell_change()
    #求购调整
    buy_change()

def sell_change():
    sellDict = getSellList()
    for i in sellDict:
        r = getGoodsPrice(i)
        if (float(sellDict[i][1])-r["sell_price"])>=0.1:
            # 改价
            changePrice(i,sellDict[i][0],r["sell_price"])


def changePrice(goods_id, sell_order_id, price):
    url = "https://buff.163.com/api/market/sell_order/change"

    headers = {
        'Content-Type': 'application/json',
        "Referer": "https://buff.163.com/market/sell_order/on_sale?game=pubg",
        "X-CSRFToken": "ImRjOTBjNDIzNzkyZDBkNTA5ZjYzZjUyMjdmODU3OGJmNzI4M2Y1YzMi.DbWb7Q.DX1hDwcW0RGjKN5-d5VJyzlR5IE"
    }

    data = {
        "game": "pubg",
        "sell_orders": [{"sell_order_id": sell_order_id, "price": price, "goods_id": goods_id}]
    }

    r = until.make_request(url,"POST",data,headers)
    if r["code"] =="OK":
        until.make_log("goods_id :%s 改价  ，price ：%f" % (goods_id,price))



def buy_change():
    sql = "select * from goods_sell_buy WHERE buy_order is not NULL"
    r = until.sqlite_select(sql)
    buylist = getBuyList()
    for i in r :
        goods_id = i[0]
        buy_order = i[2].split("|")[0]
        now_buy_price = float(i[2].split("|")[1])
        sell_price = i[5]
        if buy_order not in buylist:
            sql = "update goods_sell_buy set buy_order = NULL WHERE  goods_id = %s"%goods_id
            until.sqlite_update(sql)
            continue
        x = getGoodsPrice(goods_id)
        if x and (x["sell_price"]-x["buy_price"]) <sell_price:
            #取消求购
            cancelBuyOrder(buy_order)
            continue
        if (x["buy_price"] - now_buy_price) >0.1 :
            cancelBuyOrder(buy_order)




def cancelBuyOrder(order_id):
    url = "https://buff.163.com/api/market/buy_order/cancel"
    data = {
        "game": "pubg",
        "buy_orders": [order_id]
    }
    headers = {
        'Content-Type': 'application/json',
        "Referer": "https://buff.163.com/market/buy_order/wait_supply?game=pubg",
        "X-CSRFToken": "ImRjOTBjNDIzNzkyZDBkNTA5ZjYzZjUyMjdmODU3OGJmNzI4M2Y1YzMi.DbWb7Q.DX1hDwcW0RGjKN5-d5VJyzlR5IE"
    }
    r = until.make_request(url,"POST",data,headers)
    if r is None:
        return False
    if r["code"] =="OK":
        sql = "update goods_sell_buy set buy_order = NULL WHERE  buy_order = %s"%order_id
        until.sqlite_update(sql)
        until.make_log("取消求购 buy_order ： %s"%order_id)


# 查询求购信息
def getBuyList():
    url = "https://buff.163.com/market/buy_order/wait_supply?game=pubg"
    headers = {
        "Referer": "https://buff.163.com/market/buy_order/wait_supply?game=pubg",
        "X-CSRFToken": "ImRjOTBjNDIzNzkyZDBkNTA5ZjYzZjUyMjdmODU3OGJmNzI4M2Y1YzMi.DbWb7Q.DX1hDwcW0RGjKN5-d5VJyzlR5IE"
    }
    r = until.make_request(url,"GET" ,None,headers)
    if r is  None:
        return []
    bs = BeautifulSoup(r, "lxml")
    list = bs.findAll("a", {"class": "i_Btn cancel-buy-order i_Btn_hollow"})
    return list

def createBuyOrder(goods_id, price, num, pay_method):
    url = "https://buff.163.com/api/market/buy_order/create"

    data = {
        "game": "pubg",
        "goods_id": goods_id,
        "price": price,
        "num": num,
        "pay_method": pay_method,
        "allow_tradable_cooldown": 0
    }

    headers = {
        "Referer": "https://buff.163.com/market/goods?goods_id=756022",
        "X-CSRFToken": "ImRjOTBjNDIzNzkyZDBkNTA5ZjYzZjUyMjdmODU3OGJmNzI4M2Y1YzMi.DbWb7Q.DX1hDwcW0RGjKN5-d5VJyzlR5IE"
    }
    r = until.make_request(url,"POST",data,headers)
    return r


def make(rows):

    goods_id = rows[0]
    goods_price = getGoodsPrice(goods_id)
    if goods_price is False:
        return "1"
    list_back_goods = getBackpack()
    if list_back_goods is False:
        return "2"

    # 判断背包里有没有
    for i in list_back_goods:
        if (str(i["goods_id"]) == goods_id and rows[3] is  None ):
            sql = "update goods_sell_buy set back_object = \"%s\" WHERE goods_id = %s"%(i,goods_id)
            until.sqlite_update(sql)
            break

def sell():
    url = "https://buff.163.com/api/market/sell_order/create/auto"
    headers = {
        "Referer": "https://buff.163.com/market/backpack?game=pubg",
        'Content-Type': 'application/json',
        "X-CSRFToken": "ImRjOTBjNDIzNzkyZDBkNTA5ZjYzZjUyMjdmODU3OGJmNzI4M2Y1YzMi.Dbb2kQ.udSbhbI-yDNuF7OhndaiNMnkTkU"
    }
    sql = "select back_object from goods_sell_buy WHERE status = 1 and back_object is NOT NULL"
    r = until.sqlite_select(sql)

    for i in r:
        back_object = eval(i[0])
        price = getGoodsPrice(str(back_object["asset_info"]["goods_id"]))
        data = {
            "game": "pubg",
            "assets": [{
                "game": back_object["game"],
                "market_hash_name": back_object["market_hash_name"],
                "contextid": back_object["asset_info"]["contextid"],
                "assetid": back_object["asset_info"]["assetid"],
                "classid": back_object["asset_info"]["classid"],
                "instanceid": back_object["asset_info"]["instanceid"],
                "goods_id": back_object["asset_info"]["goods_id"],
                "price": price["sell_price"]
            }]
        }
        r = until.make_request(url,"POST",data,headers)
        if r["code"] =="OK":
            sell_order = None
            for i in r.keys():
                sell_order = i
            sql = "update goods_sell_buy set back_object = NULL,set sell_order = %s WHERE goods_id = %d"% (sell_order,back_object["asset_info"]["goods_id"])
            until.sqlite_update(sql)
            until.make_log("上架goods_id ：%s,价格：%f" % (str(back_object["asset_info"]["goods_id"]),price["sell_price"]))


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
    url = "https://buff.163.com/api/market/backpack?game=pubg&page_num=1"
    headers = {
        "Referer": "https://buff.163.com/market/buy_order/wait_supply?game=pubg"
       }
    r = until.make_request(url,"GET",None,headers)
    if r is None:
        until.make_log("获取背包列表失败")
        return False
    j = json.loads(r)
    if j["code"] != "OK":
        return False
    return j["data"]["items"]

#获取价格
def getGoodsPrice(goods_id):

    url_buy = "https://buff.163.com/api/market/goods/buy_order?game=pubg&goods_id=" + goods_id + "&page_num=1"
    r_buy = until.make_request(url_buy,"GET",None,None)
    if r_buy is None:
        until.make_log("获取goods_id : %s 求购价格失败 ."%goods_id)
        return False
    url_sell = "https://buff.163.com/api/market/goods/sell_order?game=pubg&goods_id=" + goods_id + "&page_num=1&sort_by=price&mode=&allow_tradable_cooldown=1"
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
        return float(price_b)

def sellprice(str):
    j = json.loads(str)
    a = j["data"]["items"][0]["price"]
    b = j["data"]["items"][1]["price"]
    if (float(a) - float(b)) > 0.1:
        return float(a)
    else:
        return float(b)

start()