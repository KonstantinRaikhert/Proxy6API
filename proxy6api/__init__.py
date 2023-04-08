"""
Proxy6.net API Library
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
   {'status': 'yes',
    'user_id': '495666',
    'balance': '21.68',
    'currency': 'RUB',
    'date_mod': '2023-04-08 20:05:26',
    'list_count': 2,
    'list': {
        '21358215':
            {'id': '21358215',
            'version': '6',
            'ip': '2a06:c006:ab5f:3293:7acf:07af:2c9a:1952',
            'host': '217.29.63.40',
            'port': '10212',
            'user': 'BWqqWK',
            'pass': 'VErw3n',
            'type': 'http',
            'country': 'ru',
            'date': '2023-04-08 20:05:26',
            'date_end': '2023-04-09 20:05:26',
            'unixtime': 1680973526,
            'unixtime_end': 1681059926,
            'descr': '',
            'active': '1'
            },
        '21358216':
            {'id': '21358216',
            'version': '6',
            'ip': '2a06:c006:510f:be73:2468:82a3:4a4a:d27d',
            'host': '217.29.63.40',
            'port': '10213',
            'user': 'BWqqWK',
            'pass': 'VErw3n',
            'type': 'http',
            'country': 'ru',
            'date': '2023-04-08 20:05:26',
            'date_end': '2023-04-09 20:05:26',
            'unixtime': 1680973526,
            'unixtime_end': 1681059926,
            'descr': '',
            'active': '1'
            }
        },
    'page': 1
    }

    or if error (example):

    >>> client.get_proxy()
    {'status': 'no',
    'error_id': 100,
    'error': 'Error key - Ошибка авторизации, неверный ключ '
    }

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
