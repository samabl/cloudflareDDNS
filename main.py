import urllib3
import json


def askApi(accountInfo, dnsInfo):
    apiUrl = 'https://api.cloudflare.com/client/v4/zones/%s/dns_records/%s' % (
        accountInfo['zones'], dnsInfo['dns_records']
    )

    dnsInfo.pop('dns_records')
    body = json.dumps(dnsInfo)

    headers = {
        'user-agent': 'Mozilla/5.0',
        'X-Auth-Email': accountInfo['email'],
        'X-Auth-Key': accountInfo['api'],
        'Content-Type': 'application/json'
    }

    res = urllib3.PoolManager().request("PUT", apiUrl, body=body, headers=headers)

    if res.status == 200:
        return print(dnsInfo['name'] + ": Success!")
    else:
        return print(dnsInfo['name'] + ": Fail!")


if __name__ == '__main__':
    # 获取IP地址
    ipv4 = urllib3.PoolManager().request(method="GET", url="https://ipv4.icanhazip.com").data.decode().rstrip()
    ipv6 = urllib3.PoolManager().request(method='GET', url='http://ipv6.icanhazip.com').data.decode().rstrip()

    # 账户信息(固定)(全部填写)
    accountInfo = {
        'email': 'example@qq.com',
        'zones': 'example',
        'api': 'example'
    }

    # 请求api实现DDNS 域名解析信息(变化)(按需填写)
    askApi(accountInfo, dnsInfo={
        'dns_records': 'example',# DNS解析ID
        'type': 'A',# A 记录
        'name': 'example', #解析的域名
        'content': ipv4, #ipv4地址
        'ttl': 0,# TTL
        'proxied': True # 是否开启Cloudflare
    })
    askApi(accountInfo, dnsInfo={
        'dns_records': 'example',
        'type': 'AAAA',
        'name': 'example',
        'content': ipv6,
        'ttl': 120,
        'proxied': True
    })
