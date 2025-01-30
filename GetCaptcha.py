import requests
from util import RunJSFile
from log import logger as log
from detectimg import model,solve
def DownloadCaptcha():
    headers = {
        'accept': '*/*',
        'accept-language': 'vi-VN,vi;q=0.9,en-US;q=0.8,en;q=0.7,ja;q=0.6',
        'cache-control': 'no-cache',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'origin': 'https://cloud.vmoscloud.com',
        'pragma': 'no-cache',
        'priority': 'u=1, i',
        'referer': 'https://cloud.vmoscloud.com/',
        'sec-ch-ua': '"Not A(Brand";v="8", "Chromium";v="132", "Google Chrome";v="132"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'cross-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36',
    }
    timestamp,nonce,sign = RunJSFile('test.js').split(',')
    data = {
        'AccessKeyId': 'LTAI5tSEBwYMwVKAQGpxmvTd',
        'SignatureMethod': 'HMAC-SHA1',
        'SignatureVersion': '1.0',
        'Format': 'JSON',
        'Timestamp': timestamp,
        'Version': '2023-03-05',
        'Action': 'InitCaptcha',
        'SceneId': '5jvar3wp',
        'Language': 'en',
        'Mode': 'popup',
        'DeviceData': 'TEQYvgJq1LrMqFaBybfIzPxz2ygFyAct7X/w+LacfXWd9rGSwE/x6ZCONucD1fehpGN+YnQ2440yHZY/zw6Giy4lg7O0ZMt3EjbNsWpCj58sAYQXCebs5Tj8FX7wir6HvRdG6AXmzjWm+EbkjEm6/A==',
        'SignatureNonce': nonce,
        'Signature': sign,
    }

    response = requests.post('https://69r0rc.captcha-open-southeast.aliyuncs.com/', headers=headers, data=data).json()
    return response


while True:
    res =  DownloadCaptcha()
    if res['Success']:
        namefile = res['Image'].split('/')[-1]
        with open('.\\img\\'+"".join(res["Question"].split())+"_"+namefile,'wb+') as f:
            f.write(requests.get('https://static-captcha-sgp.aliyuncs.com/'+res['Image']).content)
        log.debug(f'Save image success name:{namefile}')
        log.debug(f'Question:{res["Question"]}')
        result = solve('.\\img\\'+"".join(res["Question"].split())+"_"+namefile,model,res["Question"])
        log.debug(f'Result:{result}')
    else:
        log.error(f'Cannot get captcha!')