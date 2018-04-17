import requests,json,ssl

ssl._create_default_https_context = ssl._create_unverified_context

#构建请求
def make_request(url,method,data,h):
    x = requests.session()
    headers = make_headers(h)
    if(method == "GET"):
        r = x.get(url=url,headers=headers)
    else:
        if(headers["Content-Type"]=="application/json"):
            data=json.dumps(data)
        r = x.post(url=url,headers=headers,data=data)
    if(r.status_code!=200):
        return None
    return r.text

#补全headers
def make_headers(h):
    headers = {
        "Host": "buff.163.com",
        "Origin": "https://buff.163.com",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"
    }
    for (k,v) in h.items():
        headers[k] = headers[v]

#记录信息
def make_log(msg):
    #todo
    pass