import requests,json,ssl,sqlite3

ssl._create_default_https_context = ssl._create_unverified_context

#构建请求
def make_request(url,method,data,h):
    x = requests.session()
    headers = make_headers(h)
    if(method == "GET"):
        r = x.get(url=url,headers=headers)
    else:
        if("Content-Type" in headers):
            data=json.dumps(data)
        r = x.post(url=url,headers=headers,data=data)
    if(r.status_code!=200):
        return None
    return r.text

#补全headers
def make_headers(h):
    #todo
    headers = {
        "Host": "buff.163.com",
        "Origin": "https://buff.163.com",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
        "Cookie": "_ntes_nnid=40da4c75ce28ee3fd276a23789989ebb,1521015755470; _ntes_nuid=40da4c75ce28ee3fd276a23789989ebb; Province=0571; City=0571; __gads=ID=007456be95b9b848:T=1522813945:S=ALNI_MZrL3JIF0TJANFO5gRTe31usiVOgw; UM_distinctid=1628ec8d0ac70a-04b7f0def9e281-6a11157a-1fa400-1628ec8d0ad7f6; vjuids=d95d59992.1628ec8d662.0.540aa0c179edd; vinfo_n_f_l_n3=db93eb31cf6ddd34.1.1.1522813949576.1522813980223.1523340533497; vjlast=1522813950.1523589129.11; game=pubg; NTES_YD_SESS=js.DZrgDjBdaT_UZA98sx_z30NTUu1Gi0zvL43Ir12Z9rOhUrIJ5Lfh3CBYRfO.xGwjIgkwlKFxXuJ2ZOMkLi9HuFf7VIunsv5GYv04.v6wLsGR8RZb8wleEw.lOpMFMlUX0tVl51pV3DYPAyVKy8cfQrWu0RiYUYktIjmj_YdtXOoL4riCZXD69qxi4xT.MllMbkwncwbeVGf5Wyvcbs1hAXIewlfpjl8oC4PrkJJDAQ; S_INFO=1523843557|0|3&80##|15158009950; P_INFO=15158009950|1523843557|1|netease_buff|00&99|null&null&null#zhj&330100#10#0|&0||15158009950; _ga=GA1.2.72461816.1520413701; _gid=GA1.2.1866669209.1523842226; locale=zh; session=1-8fGn0QiF088A8uymAJ7FtmFy3n55uIQj4iAyb1w2oVx02045356209; csrf_token=dc90c423792d0d509f63f5227f8578bf7283f5c3",
    }
    if h is not None:
        for (k,v) in h.items():
            headers[k] = v
    return headers

#sqlite
def sqlite_select(sql):
    r = []
    conn = sqlite3.connect("data.db")
    c = conn.cursor()
    cur = c.execute(sql)
    for i in cur:
        r.append(i)
    conn.close()
    return r

def sqlite_update(sql):
    conn = sqlite3.connect("data.db")
    c = conn.cursor()
    cur = c.execute(sql)
    conn.commit()
    conn.close()

