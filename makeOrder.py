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

def start(goods_id):

    goods_price = getGoodsPrice(goods_id)



#获取价格
def getGoodsPrice(goods_id):

    url_buy = "https://buff.163.com/api/market/goods/buy_order?game=pubg&goods_id=" + goods_id + "&page_num=1"
    r_buy = until.make_request(url_buy,"GET")
    if r_buy is None:
        until.make_log("获取goods_id : %s 求购价格失败 ."%goods_id)
        return False
    url_sell = "https://buff.163.com/api/market/goods/sell_order?game=pubg&goods_id=" + id + "&page_num=1&sort_by=price&mode=&allow_tradable_cooldown=1"
    r_sell = until.make_request(url_sell, "GET")
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