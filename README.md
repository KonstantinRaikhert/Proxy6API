# Proxy6API

This is unofficial software for using API on [proxy 6.net](https://proxy6.net/)

## Installation:

`pip install proxy6api`

## Usage

After registration on [proxy 6.net](https://proxy6.net/) get API_KEY on [this page](https://proxy6.net/en/user/developers).

Import and usage methods:

```
import osfrom proxy6api import Proxy_6_Client
API_KEY = os.getenv("PROXY_6_API_KEY")
client = Proxy_6_Client(api_key=API_KEY)
client.get_proxy()
```

response:

```
ProxyInfo(status='yes', user_id=111, balance=16.88, currency='RUB', list_count=4, date_mod=datetime.datetime(2023, 4, 9, 19, 12, 20), proxies_list=[ProxyItemInfo(id=71087, ip='2a06:c006:e8e0:a6b4:9e4c:05d2:2fa1:afc5', host='11.229.63.40', port='10409', user='oz295', password='tjQpP6', proxy_type='http', country='ru', date=datetime.datetime(2023, 4, 9, 19, 10, 51), date_end=datetime.datetime(2023, 4, 10, 19, 10, 51), unixtime=1681056651, unixtime_end=1681143051, descr='', active=True), ProxyItemInfo(id=2182, ip='2a06:c006:2bd8:3f81:d1ce:7354:4442:98db', host='217.209.683.40', port='1035', user='tpeS', password='b2S0f', proxy_type='socks', country='ru', date=datetime.datetime(2023, 4, 9, 18, 25, 20), date_end=datetime.datetime(2023, 4, 10, 18, 25, 20), unixtime=1681053920, unixtime_end=1681140320, descr='test', active=True), ProxyItemInfo(id=2181, ip='2a06:c006:17df:0ee1:43a3:2679:b194:6ad5', host='2137.29.623.40', port='10498', user='PtsxYC', password='KCsduj', proxy_type='http', country='ru', date=datetime.datetime(2023, 4, 9, 19, 9, 6), date_end=datetime.datetime(2023, 4, 10, 19, 9, 6), unixtime=1681056546, unixtime_end=1681142946, descr='', active=True), ProxyItemInfo(id=2112091, ip='2a06:c006:524f:862d:b3bc:e923:e995:de4b', host='217.239.63.430', port='10400', user='TsdEV', password='kK325q', proxy_type='http', country='ru', date=datetime.datetime(2023, 4, 9, 19, 12, 20), date_end=datetime.datetime(2023, 4, 10, 19, 12, 20), unixtime=1681056740, unixtime_end=1681143140, descr='', active=True)], page=1)
```

error example:

```
ErrorInfo(error_id=100, error='Error key - Ошибка авторизации, неверный ключ ')
```
