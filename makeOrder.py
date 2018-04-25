"""
0. 获取goods_id 最合适的 （出售价格 - 求购价格 = 利润）
1. 获取登录session
2. 获取我的背包列表
3. 获取我的出售列表
4. 获取我的求购列表
5. goods_id 是否在求购列表 => 求购
6. goods_id 是否在出售列表 => 出售
"""

import until,buffApi

low_price = 5
fee_p = 0.018

# 进行记录同步
def sysnc():
    sql = "select * from goods_sell_buy"
    x = until.sqlite_select(sql)
    back_list = buffApi.getBackpack("pubg")
    sell_list = buffApi.getSellList("pubg")
    for i in x:
        goods_id = i[0]
        # 将背包里的东西更新入数据库，并且更新订单
        if back_list:
            for b in back_list:
                if (str(b["goods_id"]) == goods_id):
                    sql = "update goods_sell_buy set back_object = \"%s\",buy_order = null WHERE goods_id = %s" % (b, goods_id)
                    until.sqlite_update(sql)
                    break
        if sell_list:
            if goods_id not in sell_list and i[1] is not None:
                sql = "update goods_sell_buy set sell_order = null WHERE goods_id = %s" % goods_id
                until.sqlite_update(sql)
            if goods_id in sell_list:
                s = str(sell_list[goods_id][0])+"|"+str(sell_list[goods_id][1])
                sql = "update goods_sell_buy set sell_order = \"%s\" WHERE goods_id = %s" % (s,goods_id)
                until.sqlite_update(sql)



#处理数据
def start_service():

    #待上架
    on_sell_dict = {}
    #待取消求购
    on_cancel_dict = {}
    #待改价
    on_change_dict = {}
    #待求购
    on_buy_dict = {}

    sql = "select * from goods_sell_buy "
    x = until.sqlite_select(sql)

    for i in x :
        goods_id = i[0]

        # 对不买的产品的求购加入下架列表
        if i[4] == 0 and i[2] is not None:
            buy_order = i[2].split("|")[0]
            on_cancel_dict[buy_order] = "pubg"

        # 数据采集、价格分析
        goods_ana = False
        if i[1] is not None or i[4] ==1:
            goods_ana = buffApi.getGoodsPrice(goods_id,"pubg",low_price,fee_p,i[5])

        if goods_ana :
            #求购
            if goods_ana["buy"] and i[1] is None and i[2] is None and i[4] ==1:
                on_buy_dict[goods_id]= [goods_ana["buy_price"],1,"3","pubg"]
            #取消
            if not goods_ana["buy"] and i[2] is not None:
                on_cancel_dict[i[2]] = "pubg"
            #改价
            if i[1] is not None:
                now_sell_price = float(i[1].split("|")[1])
                new_sell_price = goods_ana["sell_price"]
                if (now_sell_price - new_sell_price)>=0.02:
                    on_change_dict[goods_id]=i[1].replace(str(now_sell_price),str(new_sell_price))

        #上架
        if i[3] is not None :
            on_sell_dict[i[3]]=["pubg",low_price,fee_p,i[5]]


    #处理结果
    # buffApi.cancelBuyOrder(on_cancel_dict)
    buffApi.sell_change(on_change_dict,"pubg")
    # buffApi.sell(on_sell_dict)
    # buffApi.createBuyOrder(on_buy_dict)
