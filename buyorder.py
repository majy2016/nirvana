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
import requests, json, ssl
from bs4 import BeautifulSoup

ssl._create_default_https_context = ssl._create_unverified_context


def getGoodsPrice(id):
    url = "https://buff.163.com/api/market/goods/buy_order?game=pubg&goods_id=" + id + "&page_num=1"
    r = requests.get(url)
    if (r.status_code != 200):
        print("buy status_code", r.status_code)
        return False
    # print(r.text)
    buy = buyprice(r.text)
    url_sell = "https://buff.163.com/api/market/goods/sell_order?game=pubg&goods_id=" + id + "&page_num=1&sort_by=price&mode=&allow_tradable_cooldown=1"
    r_sell = requests.get(url_sell)
    if (r_sell.status_code != 200):
        print("sell status_code", r_sell.status_code)
        return False
    sell = sellprice(r_sell.text)
    result = {}
    result["id"] = id
    result["buy"] = buy
    result["sell"] = sell
    return result


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


# print(getGoodsPrice("756022"))

# 查询余额账户
def balanceChenck():
    url = "https://buff.163.com/api/asset/balance_check/?amount=0.01"
    headers = {
        "Cookie": "_ntes_nnid=40da4c75ce28ee3fd276a23789989ebb,1521015755470; _ntes_nuid=40da4c75ce28ee3fd276a23789989ebb; Province=0571; City=0571; __gads=ID=007456be95b9b848:T=1522813945:S=ALNI_MZrL3JIF0TJANFO5gRTe31usiVOgw; UM_distinctid=1628ec8d0ac70a-04b7f0def9e281-6a11157a-1fa400-1628ec8d0ad7f6; vjuids=d95d59992.1628ec8d662.0.540aa0c179edd; vinfo_n_f_l_n3=db93eb31cf6ddd34.1.1.1522813949576.1522813980223.1523340533497; vjlast=1522813950.1523589129.11; game=pubg; NTES_YD_SESS=js.DZrgDjBdaT_UZA98sx_z30NTUu1Gi0zvL43Ir12Z9rOhUrIJ5Lfh3CBYRfO.xGwjIgkwlKFxXuJ2ZOMkLi9HuFf7VIunsv5GYv04.v6wLsGR8RZb8wleEw.lOpMFMlUX0tVl51pV3DYPAyVKy8cfQrWu0RiYUYktIjmj_YdtXOoL4riCZXD69qxi4xT.MllMbkwncwbeVGf5Wyvcbs1hAXIewlfpjl8oC4PrkJJDAQ; S_INFO=1523843557|0|3&80##|15158009950; P_INFO=15158009950|1523843557|1|netease_buff|00&99|null&null&null#zhj&330100#10#0|&0||15158009950; _ga=GA1.2.72461816.1520413701; _gid=GA1.2.1866669209.1523842226; locale=zh; session=1-8fGn0QiF088A8uymAJ7FtmFy3n55uIQj4iAyb1w2oVx02045356209; csrf_token=dc90c423792d0d509f63f5227f8578bf7283f5c3"
    }
    x = requests.session()
    # requests.utils.add_dict_to_cookiejar(x.cookies, mycookie)
    r = x.get(url=url, headers=headers)
    print(r.status_code)
    print(r.text)


# balanceChenck()


# 创建求购订单
# pay_method 支付宝余额 3
# {\n  "code": "BuyOrder Create Cooling Down", \n  "error": "同一饰品15分钟内只能发起求购一次，请稍后再试"\n}
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
        "Host": "buff.163.com",
        "Referer": "https://buff.163.com/market/goods?goods_id=756022",
        "Origin": "https://buff.163.com",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
        "Cookie": "_ntes_nnid=40da4c75ce28ee3fd276a23789989ebb,1521015755470; _ntes_nuid=40da4c75ce28ee3fd276a23789989ebb; Province=0571; City=0571; __gads=ID=007456be95b9b848:T=1522813945:S=ALNI_MZrL3JIF0TJANFO5gRTe31usiVOgw; UM_distinctid=1628ec8d0ac70a-04b7f0def9e281-6a11157a-1fa400-1628ec8d0ad7f6; vjuids=d95d59992.1628ec8d662.0.540aa0c179edd; vinfo_n_f_l_n3=db93eb31cf6ddd34.1.1.1522813949576.1522813980223.1523340533497; vjlast=1522813950.1523589129.11; game=pubg; NTES_YD_SESS=js.DZrgDjBdaT_UZA98sx_z30NTUu1Gi0zvL43Ir12Z9rOhUrIJ5Lfh3CBYRfO.xGwjIgkwlKFxXuJ2ZOMkLi9HuFf7VIunsv5GYv04.v6wLsGR8RZb8wleEw.lOpMFMlUX0tVl51pV3DYPAyVKy8cfQrWu0RiYUYktIjmj_YdtXOoL4riCZXD69qxi4xT.MllMbkwncwbeVGf5Wyvcbs1hAXIewlfpjl8oC4PrkJJDAQ; S_INFO=1523843557|0|3&80##|15158009950; P_INFO=15158009950|1523843557|1|netease_buff|00&99|null&null&null#zhj&330100#10#0|&0||15158009950; _ga=GA1.2.72461816.1520413701; _gid=GA1.2.1866669209.1523842226; locale=zh; session=1-8fGn0QiF088A8uymAJ7FtmFy3n55uIQj4iAyb1w2oVx02045356209; csrf_token=dc90c423792d0d509f63f5227f8578bf7283f5c3",
        "X-CSRFToken": "ImRjOTBjNDIzNzkyZDBkNTA5ZjYzZjUyMjdmODU3OGJmNzI4M2Y1YzMi.DbWb7Q.DX1hDwcW0RGjKN5-d5VJyzlR5IE"
    }
    x = requests.session()
    r = x.post(url=url, data=data, headers=headers)
    print(r.status_code)
    print(r.text)


# createBuyOrder(756022,1,1,"3")


# 查询求购信息
# https://buff.163.com/market/buy_order/wait_supply?game=pubg
def getBuyList():
    url = "https://buff.163.com/market/buy_order/wait_supply?game=pubg"
    headers = {
        "Host": "buff.163.com",
        "Origin": "https://buff.163.com",
        "Referer": "https://buff.163.com/market/buy_order/wait_supply?game=pubg",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
        "Cookie": "_ntes_nnid=40da4c75ce28ee3fd276a23789989ebb,1521015755470; _ntes_nuid=40da4c75ce28ee3fd276a23789989ebb; Province=0571; City=0571; __gads=ID=007456be95b9b848:T=1522813945:S=ALNI_MZrL3JIF0TJANFO5gRTe31usiVOgw; UM_distinctid=1628ec8d0ac70a-04b7f0def9e281-6a11157a-1fa400-1628ec8d0ad7f6; vjuids=d95d59992.1628ec8d662.0.540aa0c179edd; vinfo_n_f_l_n3=db93eb31cf6ddd34.1.1.1522813949576.1522813980223.1523340533497; vjlast=1522813950.1523589129.11; game=pubg; NTES_YD_SESS=js.DZrgDjBdaT_UZA98sx_z30NTUu1Gi0zvL43Ir12Z9rOhUrIJ5Lfh3CBYRfO.xGwjIgkwlKFxXuJ2ZOMkLi9HuFf7VIunsv5GYv04.v6wLsGR8RZb8wleEw.lOpMFMlUX0tVl51pV3DYPAyVKy8cfQrWu0RiYUYktIjmj_YdtXOoL4riCZXD69qxi4xT.MllMbkwncwbeVGf5Wyvcbs1hAXIewlfpjl8oC4PrkJJDAQ; S_INFO=1523843557|0|3&80##|15158009950; P_INFO=15158009950|1523843557|1|netease_buff|00&99|null&null&null#zhj&330100#10#0|&0||15158009950; _ga=GA1.2.72461816.1520413701; _gid=GA1.2.1866669209.1523842226; locale=zh; session=1-8fGn0QiF088A8uymAJ7FtmFy3n55uIQj4iAyb1w2oVx02045356209; csrf_token=dc90c423792d0d509f63f5227f8578bf7283f5c3",
        "X-CSRFToken": "ImRjOTBjNDIzNzkyZDBkNTA5ZjYzZjUyMjdmODU3OGJmNzI4M2Y1YzMi.DbWb7Q.DX1hDwcW0RGjKN5-d5VJyzlR5IE"
    }
    x = requests.session()
    r = x.get(url=url, headers=headers)
    print(r.status_code)
    # print(r.text)
    bs = BeautifulSoup(r.text, "lxml")
    # print(bs)
    list = bs.findAll("a", {"class": "i_Btn cancel-buy-order i_Btn_hollow"})
    for i in list:
        print(i)
        print(i["data-orderid"])


# getBuyList()

# 求购取消
# https://buff.163.com/api/market/buy_order/cancel
# {"game":"pubg","buy_orders":["180416T1094484427"]}
def cancelBuyOrder(order_id):
    url = "https://buff.163.com/api/market/buy_order/cancel"
    data = {
        "game": "pubg",
        "buy_orders": [order_id]
    }
    print(data)
    headers = {
        "Host": "buff.163.com",
        'Content-Type': 'application/json',
        "Origin": "https://buff.163.com",
        "Referer": "https://buff.163.com/market/buy_order/wait_supply?game=pubg",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
        "Cookie": "_ntes_nnid=40da4c75ce28ee3fd276a23789989ebb,1521015755470; _ntes_nuid=40da4c75ce28ee3fd276a23789989ebb; Province=0571; City=0571; __gads=ID=007456be95b9b848:T=1522813945:S=ALNI_MZrL3JIF0TJANFO5gRTe31usiVOgw; UM_distinctid=1628ec8d0ac70a-04b7f0def9e281-6a11157a-1fa400-1628ec8d0ad7f6; vjuids=d95d59992.1628ec8d662.0.540aa0c179edd; vinfo_n_f_l_n3=db93eb31cf6ddd34.1.1.1522813949576.1522813980223.1523340533497; vjlast=1522813950.1523589129.11; game=pubg; NTES_YD_SESS=js.DZrgDjBdaT_UZA98sx_z30NTUu1Gi0zvL43Ir12Z9rOhUrIJ5Lfh3CBYRfO.xGwjIgkwlKFxXuJ2ZOMkLi9HuFf7VIunsv5GYv04.v6wLsGR8RZb8wleEw.lOpMFMlUX0tVl51pV3DYPAyVKy8cfQrWu0RiYUYktIjmj_YdtXOoL4riCZXD69qxi4xT.MllMbkwncwbeVGf5Wyvcbs1hAXIewlfpjl8oC4PrkJJDAQ; S_INFO=1523843557|0|3&80##|15158009950; P_INFO=15158009950|1523843557|1|netease_buff|00&99|null&null&null#zhj&330100#10#0|&0||15158009950; _ga=GA1.2.72461816.1520413701; _gid=GA1.2.1866669209.1523842226; locale=zh; session=1-8fGn0QiF088A8uymAJ7FtmFy3n55uIQj4iAyb1w2oVx02045356209; csrf_token=dc90c423792d0d509f63f5227f8578bf7283f5c3",
        "X-CSRFToken": "ImRjOTBjNDIzNzkyZDBkNTA5ZjYzZjUyMjdmODU3OGJmNzI4M2Y1YzMi.DbWb7Q.DX1hDwcW0RGjKN5-d5VJyzlR5IE"
    }
    x = requests.session()
    r = x.post(url=url, data=json.dumps(data), headers=headers)
    print(r.status_code)
    print(r.text)


# cancelBuyOrder("180417T1094492255")


# 查询售卖列表
# https://buff.163.com/market/sell_order/on_sale?game=pubg
def getSellList():
    url = "https://buff.163.com/market/sell_order/on_sale?game=pubg"
    headers = {
        "Host": "buff.163.com",
        "Origin": "https://buff.163.com",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
        "Cookie": "_ntes_nnid=40da4c75ce28ee3fd276a23789989ebb,1521015755470; _ntes_nuid=40da4c75ce28ee3fd276a23789989ebb; Province=0571; City=0571; __gads=ID=007456be95b9b848:T=1522813945:S=ALNI_MZrL3JIF0TJANFO5gRTe31usiVOgw; UM_distinctid=1628ec8d0ac70a-04b7f0def9e281-6a11157a-1fa400-1628ec8d0ad7f6; vjuids=d95d59992.1628ec8d662.0.540aa0c179edd; vinfo_n_f_l_n3=db93eb31cf6ddd34.1.1.1522813949576.1522813980223.1523340533497; vjlast=1522813950.1523589129.11; game=pubg; NTES_YD_SESS=js.DZrgDjBdaT_UZA98sx_z30NTUu1Gi0zvL43Ir12Z9rOhUrIJ5Lfh3CBYRfO.xGwjIgkwlKFxXuJ2ZOMkLi9HuFf7VIunsv5GYv04.v6wLsGR8RZb8wleEw.lOpMFMlUX0tVl51pV3DYPAyVKy8cfQrWu0RiYUYktIjmj_YdtXOoL4riCZXD69qxi4xT.MllMbkwncwbeVGf5Wyvcbs1hAXIewlfpjl8oC4PrkJJDAQ; S_INFO=1523843557|0|3&80##|15158009950; P_INFO=15158009950|1523843557|1|netease_buff|00&99|null&null&null#zhj&330100#10#0|&0||15158009950; _ga=GA1.2.72461816.1520413701; _gid=GA1.2.1866669209.1523842226; locale=zh; session=1-8fGn0QiF088A8uymAJ7FtmFy3n55uIQj4iAyb1w2oVx02045356209; csrf_token=dc90c423792d0d509f63f5227f8578bf7283f5c3",
        "X-CSRFToken": "ImRjOTBjNDIzNzkyZDBkNTA5ZjYzZjUyMjdmODU3OGJmNzI4M2Y1YzMi.DbWb7Q.DX1hDwcW0RGjKN5-d5VJyzlR5IE"
    }
    x = requests.session()
    r = x.get(url=url, headers=headers)
    print(r.status_code)
    # print(r.text)
    bs = BeautifulSoup(r.text, "lxml")
    # print(bs)
    list = bs.findAll("li", {"class": "salable"})
    result = {}
    for i in list:
        result[i["data-goodsid"]] = [i["data-orderid"],i["data-price"]]
    print(result)



getSellList()

# 改价
# https://buff.163.com/api/market/sell_order/change
def changePrice(goods_id, sell_order_id, price):
    url = "https://buff.163.com/api/market/sell_order/change"

    headers = {
        "Host": "buff.163.com",
        "Origin": "https://buff.163.com",
        'Content-Type': 'application/json',
        "Referer": "https://buff.163.com/market/sell_order/on_sale?game=pubg",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
        "Cookie": "_ntes_nnid=40da4c75ce28ee3fd276a23789989ebb,1521015755470; _ntes_nuid=40da4c75ce28ee3fd276a23789989ebb; Province=0571; City=0571; __gads=ID=007456be95b9b848:T=1522813945:S=ALNI_MZrL3JIF0TJANFO5gRTe31usiVOgw; UM_distinctid=1628ec8d0ac70a-04b7f0def9e281-6a11157a-1fa400-1628ec8d0ad7f6; vjuids=d95d59992.1628ec8d662.0.540aa0c179edd; vinfo_n_f_l_n3=db93eb31cf6ddd34.1.1.1522813949576.1522813980223.1523340533497; vjlast=1522813950.1523589129.11; game=pubg; NTES_YD_SESS=js.DZrgDjBdaT_UZA98sx_z30NTUu1Gi0zvL43Ir12Z9rOhUrIJ5Lfh3CBYRfO.xGwjIgkwlKFxXuJ2ZOMkLi9HuFf7VIunsv5GYv04.v6wLsGR8RZb8wleEw.lOpMFMlUX0tVl51pV3DYPAyVKy8cfQrWu0RiYUYktIjmj_YdtXOoL4riCZXD69qxi4xT.MllMbkwncwbeVGf5Wyvcbs1hAXIewlfpjl8oC4PrkJJDAQ; S_INFO=1523843557|0|3&80##|15158009950; P_INFO=15158009950|1523843557|1|netease_buff|00&99|null&null&null#zhj&330100#10#0|&0||15158009950; _ga=GA1.2.72461816.1520413701; _gid=GA1.2.1866669209.1523842226; locale=zh; session=1-8fGn0QiF088A8uymAJ7FtmFy3n55uIQj4iAyb1w2oVx02045356209; csrf_token=dc90c423792d0d509f63f5227f8578bf7283f5c3",
        "X-CSRFToken": "ImRjOTBjNDIzNzkyZDBkNTA5ZjYzZjUyMjdmODU3OGJmNzI4M2Y1YzMi.DbWb7Q.DX1hDwcW0RGjKN5-d5VJyzlR5IE"
    }

    data = {
        "game": "pubg",
        "sell_orders": [{"sell_order_id": sell_order_id, "price": price, "goods_id": goods_id}]
    }
    print(data)
    x = requests.session()
    r = x.post(url=url, data=json.dumps(data), headers=headers)
    print(r.status_code)
    print(r.text)


changePrice(33232,"180417T1095187850",0.7)

# 查询背包列表
def getBackpack():
    url = "https://buff.163.com/api/market/backpack?game=pubg&page_num=1"
    headers = {
        "Host": "buff.163.com",
        "Origin": "https://buff.163.com",
        "Referer": "https://buff.163.com/market/buy_order/wait_supply?game=pubg",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
        "Cookie": "_ntes_nnid=40da4c75ce28ee3fd276a23789989ebb,1521015755470; _ntes_nuid=40da4c75ce28ee3fd276a23789989ebb; Province=0571; City=0571; __gads=ID=007456be95b9b848:T=1522813945:S=ALNI_MZrL3JIF0TJANFO5gRTe31usiVOgw; UM_distinctid=1628ec8d0ac70a-04b7f0def9e281-6a11157a-1fa400-1628ec8d0ad7f6; vjuids=d95d59992.1628ec8d662.0.540aa0c179edd; vinfo_n_f_l_n3=db93eb31cf6ddd34.1.1.1522813949576.1522813980223.1523340533497; vjlast=1522813950.1523589129.11; game=pubg; NTES_YD_SESS=js.DZrgDjBdaT_UZA98sx_z30NTUu1Gi0zvL43Ir12Z9rOhUrIJ5Lfh3CBYRfO.xGwjIgkwlKFxXuJ2ZOMkLi9HuFf7VIunsv5GYv04.v6wLsGR8RZb8wleEw.lOpMFMlUX0tVl51pV3DYPAyVKy8cfQrWu0RiYUYktIjmj_YdtXOoL4riCZXD69qxi4xT.MllMbkwncwbeVGf5Wyvcbs1hAXIewlfpjl8oC4PrkJJDAQ; S_INFO=1523843557|0|3&80##|15158009950; P_INFO=15158009950|1523843557|1|netease_buff|00&99|null&null&null#zhj&330100#10#0|&0||15158009950; _ga=GA1.2.72461816.1520413701; _gid=GA1.2.1866669209.1523842226; locale=zh; session=1-8fGn0QiF088A8uymAJ7FtmFy3n55uIQj4iAyb1w2oVx02045356209; csrf_token=dc90c423792d0d509f63f5227f8578bf7283f5c3",
    }
    print(headers)
    x = requests.session()
    r = x.get(url=url, headers=headers)
    print(r.status_code)
    # print(r.text)
    # print(type(r.text))
    j = json.loads(r.text)
    print(j["data"]["items"])


# getBackpack()


# 寄售上架
# https://buff.163.com/api/market/sell_order/create/auto
# {"game":"pubg","assets":[{"game":"pubg","market_hash_name":"Cargo Pants (Khaki)","contextid":2,"assetid":"2843336623646208779","classid":"2330967986","instanceid":"0","goods_id":28824,"price":0.5}]}
def sell(assetid,classid,contextid,instanceid,goods_id,price):
    url = "https://buff.163.com/api/market/sell_order/create/auto"
    headers = {
        "Host": "buff.163.com",
        "Origin": "https://buff.163.com",
        'Content-Type': 'application/json',
        "Referer": "https://buff.163.com/market/backpack?game=pubg",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
        "Cookie": "_ntes_nnid=40da4c75ce28ee3fd276a23789989ebb,1521015755470; _ntes_nuid=40da4c75ce28ee3fd276a23789989ebb; Province=0571; City=0571; __gads=ID=007456be95b9b848:T=1522813945:S=ALNI_MZrL3JIF0TJANFO5gRTe31usiVOgw; UM_distinctid=1628ec8d0ac70a-04b7f0def9e281-6a11157a-1fa400-1628ec8d0ad7f6; vjuids=d95d59992.1628ec8d662.0.540aa0c179edd; vinfo_n_f_l_n3=db93eb31cf6ddd34.1.1.1522813949576.1522813980223.1523340533497; vjlast=1522813950.1523589129.11; game=pubg; NTES_YD_SESS=js.DZrgDjBdaT_UZA98sx_z30NTUu1Gi0zvL43Ir12Z9rOhUrIJ5Lfh3CBYRfO.xGwjIgkwlKFxXuJ2ZOMkLi9HuFf7VIunsv5GYv04.v6wLsGR8RZb8wleEw.lOpMFMlUX0tVl51pV3DYPAyVKy8cfQrWu0RiYUYktIjmj_YdtXOoL4riCZXD69qxi4xT.MllMbkwncwbeVGf5Wyvcbs1hAXIewlfpjl8oC4PrkJJDAQ; S_INFO=1523843557|0|3&80##|15158009950; P_INFO=15158009950|1523843557|1|netease_buff|00&99|null&null&null#zhj&330100#10#0|&0||15158009950; _ga=GA1.2.72461816.1520413701; _gid=GA1.2.1866669209.1523842226; locale=zh; session=1-8fGn0QiF088A8uymAJ7FtmFy3n55uIQj4iAyb1w2oVx02045356209; csrf_token=dc90c423792d0d509f63f5227f8578bf7283f5c3",
        "X-CSRFToken":"ImRjOTBjNDIzNzkyZDBkNTA5ZjYzZjUyMjdmODU3OGJmNzI4M2Y1YzMi.Dbb2kQ.udSbhbI-yDNuF7OhndaiNMnkTkU"
    }
    data = {
        "game": "pubg",
        "assets": [{
            "game":"pubg",
            "market_hash_name":"Cargo Pants (Beige)",
            "contextid":contextid,
            "assetid":assetid,
            "classid":classid,
            "instanceid":instanceid,
            "goods_id":goods_id,
            "price":price
        }]
    }
    print(data)
    x = requests.session()
    r = x.post(url=url, data=json.dumps(data), headers=headers)
    print(r.status_code)
    print(r.text)

# sell("3007718010361719267", "2769169232", 2, "0", 756022, 2.87)