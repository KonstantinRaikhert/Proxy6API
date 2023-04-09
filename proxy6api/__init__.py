"""
Unofficial Proxy6.net API Library
~~~~~~~~~~~~~~~~~~~~~

Api allows you to integrate proxy purchase into your service or application.

Interaction of the partner with the system, as well as the interaction of the system with the partner,
is possible by GET-requests and JSON-responds. All communication uses UTF-8 coding.
The answer received in different coding will lead to operation errors.

   >>> import os
   >>> from proxy6api import Proxy_6_Client
   >>> API_KEY = os.getenv("PROXY_6_API_KEY")
   >>> client = Proxy_6_Client(api_key=API_KEY)
   >>> client.get_proxy()

   >>> ProxyInfo(status='yes', user_id=495666, balance=16.88, currency='RUB', list_count=4,
   date_mod=datetime.datetime(2023, 4, 9, 19, 12, 20), proxies_list=[ProxyItemInfo(id=21371087,
   ip='2a06:c006:e8e0:a6b4:9e4c:05d2:2fa1:afc5', host='217.29.63.40', port='10449', user='ozgK95',
   password='tjQpP6', proxy_type='http', country='ru', date=datetime.datetime(2023, 4, 9, 19, 10, 51),
   date_end=datetime.datetime(2023, 4, 10, 19, 10, 51), unixtime=1681056651, unixtime_end=1681143051,
   descr='', active=True), ProxyItemInfo(id=21370682, ip='2a06:c006:2bd8:3f81:d1ce:7354:4442:98db',
   host='217.29.63.40', port='10435', user='tpe85S', password='b29S0f', proxy_type='socks', country='ru',
   date=datetime.datetime(2023, 4, 9, 18, 25, 20), date_end=datetime.datetime(2023, 4, 10, 18, 25, 20),
   unixtime=1681053920, unixtime_end=1681140320, descr='test', active=True), ProxyItemInfo(id=21371081,
   ip='2a06:c006:17df:0ee1:43a3:2679:b194:6ad5', host='217.29.63.40', port='10448', user='PtSxYC', password='KC1uuj',
   proxy_type='http', country='ru', date=datetime.datetime(2023, 4, 9, 19, 9, 6),
   date_end=datetime.datetime(2023, 4, 10, 19, 9, 6), unixtime=1681056546, unixtime_end=1681142946,
   descr='', active=True), ProxyItemInfo(id=21371091, ip='2a06:c006:524f:862d:b3bc:e923:e995:de4b',
   host='217.29.63.40', port='10450', user='THvMEV', password='kK3y5q', proxy_type='http', country='ru',
   date=datetime.datetime(2023, 4, 9, 19, 12, 20), date_end=datetime.datetime(2023, 4, 10, 19, 12, 20),
   unixtime=1681056740, unixtime_end=1681143140, descr='', active=True)], page=1)

    or if error (example):

    >>> client.get_proxy()

    >>> ErrorInfo(error_id=100, error='Error key - Ошибка авторизации, неверный ключ ')

    Available methods:
        get_price - Getting information about the cost of the order;

        get_count_in_country - Getting information about the available number of proxies for a specific country;

        get_countries - Getting the list of available countries;

        get_proxy - Getting the list of your proxies;

        set_type - Changing the type (protocol) of the proxies;

        set_descr - Update technical comment;

        buy - Buy proxy;

        prolong - Proxy list extension;

        delete - Deleting a proxy;

        check - Proxy validity check.

"""


__all__ = ["Proxy_6_Client", "CODES_OF_ERRORS", "COUNTRIES_HUMAN_NAME_KEYS", "COUNTRIES_ISO2_KEYS", "typing_methods"]

from .client import Proxy_6_Client
from .settings import CODES_OF_ERRORS, COUNTRIES_HUMAN_NAME_KEYS, COUNTRIES_ISO2_KEYS, typing_methods

name = "Proxy6 API"
__author__ = "Konstantin Raikhert"
