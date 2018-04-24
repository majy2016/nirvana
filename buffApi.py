"""
封装调用网易BUFF行为接口请求

"""
import json
from bs4 import BeautifulSoup
from until import make_request,sqlite_update

#上架
def sell(on_sell_dict):
    url = "https://buff.163.com/api/market/sell_order/create/auto"
    for (k,v) in on_sell_dict.items():
        game = v
        headers = {
            "Referer": "https://buff.163.com/market/backpack?game="+game,
            'Content-Type': 'application/json',
            "X-CSRFToken": "ImRjOTBjNDIzNzkyZDBkNTA5ZjYzZjUyMjdmODU3OGJmNzI4M2Y1YzMi.Dbb2kQ.udSbhbI-yDNuF7OhndaiNMnkTkU"
        }
        try:
            k = k.replace("null", "1111")
            back_object = eval(k)
            price = getGoodsPrice(str(back_object["asset_info"]["goods_id"]))
            data = {
                "game": game,
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
            r = make_request(url, "POST", data, headers)
            r = r.replace("null", "1111")
            r = eval(r)
            if r["code"] == "OK":
                sell_order = None
                for i in r.keys():
                    sell_order = i
                sql = "update goods_sell_buy set back_object = NULL,sell_order = %s WHERE goods_id = %d" % (
                sell_order, back_object["asset_info"]["goods_id"])
                sqlite_update(sql)
                print("上架goods_id ：%s,价格：%f =======================>>>>>>>>>>>>>>>>>>" % (
                str(back_object["asset_info"]["goods_id"]), price["sell_price"]))
        except Exception as e:
            print("上架异常 ===============>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>",e)

#求购
def createBuyOrder(on_buy_dict):
    url = "https://buff.163.com/api/market/buy_order/create"

    headers = {
        "Referer": "https://buff.163.com/market/goods?goods_id=756022",
        "X-CSRFToken": "ImRjOTBjNDIzNzkyZDBkNTA5ZjYzZjUyMjdmODU3OGJmNzI4M2Y1YzMi.DbWb7Q.DX1hDwcW0RGjKN5-d5VJyzlR5IE"
    }
    print(on_buy_dict)
    for (k,v) in on_buy_dict.items():
        goods_id = k
        price = v[0]
        num = v[1]
        pay_method = v[2]
        game = v[3]
        data = {
            "game": game,
            "goods_id": goods_id,
            "price": price,
            "num": num,
            "pay_method": pay_method,
            "allow_tradable_cooldown": 0
        }
        try:
            r = make_request(url,"POST",data,headers)
            print("求购结果 =========================================>>>>>>>>", r)
            r = r.replace("null", "1111")
            r = eval(r)
            if r["code"] == "OK":
                s = r["data"]["id"]+"|"+str(price)
                sql = "update goods_sell_buy set buy_order = %s WHERE goods_id = %s" % (s,goods_id)
                print(sql)
                sqlite_update(sql)
        except Exception as e:
            print("=================>>>>>>>>>>>>>>>>>> 求购报错",e)


#改价
def sell_change(on_change_dict,game):
    url = "https://buff.163.com/api/market/sell_order/change"

    headers = {
        'Content-Type': 'application/json',
        "Referer": "https://buff.163.com/market/sell_order/on_sale?game="+game,
        "X-CSRFToken": "ImRjOTBjNDIzNzkyZDBkNTA5ZjYzZjUyMjdmODU3OGJmNzI4M2Y1YzMi.DbWb7Q.DX1hDwcW0RGjKN5-d5VJyzlR5IE"
    }
    for(k,v) in on_change_dict.items():
        try:
            goods_id = k
            sell_order_id = v.split("|")[0]
            price = v.split("|")[1]
            data = {
                "game": game,
                "sell_orders": [{"sell_order_id": sell_order_id, "price": price, "goods_id": goods_id}]
            }
            r = make_request(url,"POST",data,headers)
            print("改价结果 =====================>>>>>>>>>>>>>>>",r)
        except Exception as e:
            print("改价=============>>>>>>>>>",e)


# 查询售卖列表
def getSellList(game):
    result = {}
    url = "https://buff.163.com/market/sell_order/on_sale?game="+game
    headers = {
        "X-CSRFToken": "ImRjOTBjNDIzNzkyZDBkNTA5ZjYzZjUyMjdmODU3OGJmNzI4M2Y1YzMi.DbWb7Q.DX1hDwcW0RGjKN5-d5VJyzlR5IE"
    }
    r = make_request(url,"GET",None,headers)
    if r is None:
        print("获取求购列表失败====================>>>>>>>>>>>>>>>>>>>>")
        return False
    bs = BeautifulSoup(r, "lxml")
    list = bs.findAll("li", {"class": "salable"})
    for i in list:
        result[i["data-goodsid"]] = [i["data-orderid"],i["data-price"]]
    return result

# 查询求购信息
def getBuyList(game):
    url = "https://buff.163.com/market/buy_order/wait_supply?game="+game
    headers = {
        "Referer": "https://buff.163.com/market/buy_order/wait_supply?game="+game,
        "X-CSRFToken": "ImRjOTBjNDIzNzkyZDBkNTA5ZjYzZjUyMjdmODU3OGJmNzI4M2Y1YzMi.DbWb7Q.DX1hDwcW0RGjKN5-d5VJyzlR5IE"
    }
    r = make_request(url,"GET" ,None,headers)
    if r is  None:
        return []
    bs = BeautifulSoup(r, "lxml")
    list = bs.findAll("a", {"class": "i_Btn cancel-buy-order i_Btn_hollow"})
    return list


# 查询背包列表
def getBackpack(game):
    url = "https://buff.163.com/api/market/backpack?game="+game+"&page_num=1"
    headers = {
        "Referer":"https://buff.163.com/market/buy_order/wait_supply?game="+game
       }
    r = make_request(url,"GET",None,headers)
    if r is None:
        print("=================>>>>>>>>>>>>>>>>>>>>> 获取背包列表失败 !!!")
        return False
    j = json.loads(r)
    if j["code"] != "OK":
        print("=================>>>>>>>>>>>>>>>>>>>>> 获取背包列表失败 2 !!!",r)
        return False
    return j["data"]["items"]

#取消求购
def cancelBuyOrder(on_cancel_dict):
    for (order_id,game) in on_cancel_dict.items():
        url = "https://buff.163.com/api/market/buy_order/cancel"
        data = {
            "game": game,
            "buy_orders": [order_id]
        }
        headers = {
            'Content-Type': 'application/json',
            "Referer": "https://buff.163.com/market/buy_order/wait_supply?game="+game,
            "X-CSRFToken": "ImRjOTBjNDIzNzkyZDBkNTA5ZjYzZjUyMjdmODU3OGJmNzI4M2Y1YzMi.DbWb7Q.DX1hDwcW0RGjKN5-d5VJyzlR5IE"
        }
        try:
            r = make_request(url,"POST",data,headers)
            if r["code"] =="OK":
                sql = "update goods_sell_buy set buy_order = NULL WHERE  buy_order = %s"%order_id
                sqlite_update(sql)
                print("取消求购 buy_order ： %s ====================================>>>>>>>>>>>>>>>>>"%order_id)
        except Exception as e:
            print(" =====================>>>>>>>>>>>>>>>>>>>>>>>取消求购出错",order_id,e)


#获取价格
def getGoodsPrice(goods_id,game,low_price,fee_p,win_price):
    try:
        url_buy = "https://buff.163.com/api/market/goods/buy_order?game="+game+"&goods_id=" + goods_id + "&page_num=1"
        r_buy = make_request(url_buy,"GET",None,None)
        if r_buy is None:
            print("获取goods_id : %s 求购价格失败 ."%goods_id)
            return False
        url_sell = "https://buff.163.com/api/market/goods/sell_order?game="+game+"&goods_id=" + goods_id + "&page_num=1&sort_by=price&mode=&allow_tradable_cooldown=1"
        r_sell = make_request(url_sell, "GET",None,None)
        if r_sell is None:
            print("获取goods_id : %s 出售价格失败 ."%goods_id)
            return False
        buy_price = buyprice(r_buy)
        sell_price = sellprice(r_sell)
        print("goods_id: %s ,求购价格：%s ,出售价格: %s" % (goods_id,buy_price,sell_price))
        if sell_price < low_price:
            x = sell_price - buy_price - 0.1
        else:
            x = (sell_price*fee_p) - buy_price
        result = {}
        if x < win_price:
            print("===================>>>>>>>>>>>. 利润过小",goods_id)
            result["buy"] = False
        else:
            result["buy"] = True
        result["buy_price"] = buy_price
        result["sell_price"] = sell_price
        return result
    except Exception as e:
        print("===========================>>>>>>>>>>>>>>>> 获取价格出错",e)
        return False

def buyprice(str):
    j = json.loads(str)
    a = j["data"]["items"][0]
    price = a["price"]
    num = a["num"]
    real_num = a["real_num"]
    if (num - real_num) >= 2:
        return float(price)
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