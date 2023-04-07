from dataclasses import dataclass
from typing import Dict, Union

import requests
from requests.exceptions import ConnectTimeout

from proxy6api.settings.bases import COUNTRIES_HUMAN_NAME_KEYS, COUNTRIES_ISO2_KEYS
from proxy6api.settings.errors import CODES_OF_ERRORS


@dataclass
class Proxy_6_API_URL:
    """
    The API is accessed at:
    https://proxy6.net/api/{api_key}/{method}/?{params}

    url: https://proxy6.net/api/
    api_key: api_key
    """

    url: str = "https://proxy6.net/api"
    api_key: str = None


class Proxy_6_Client:
    def __init__(self, api_url: Proxy_6_API_URL) -> None:
        self.url = api_url.url
        self.api_key = api_url.api_key

    @staticmethod
    def _query_params_of_method(**query_params) -> str:
        """Converts the request parameters to a string"""
        query_params_string: str = "?"
        for key, value in query_params.items():
            if value is None or value is False:
                continue
            if isinstance(value, list):
                value = ",".join(map(str, value))
            query_params_string += f"{key}={value}&"
        return query_params_string

    def request(self, method: str, **query_params) -> Union[Dict, str]:
        try:
            url = f"{self.url}/{self.api_key}/{method}"
            if query_params:
                params_of_method = Proxy_6_Client._query_params_of_method(**query_params)
                url += params_of_method
            response_json = requests.get(url=url).json()
            if response_json.get("error"):
                return CODES_OF_ERRORS.get(response_json["error_id"])
            return response_json
        except ConnectTimeout as er:
            return er

    def get_price(self, count: int, period: int, version: int = None) -> Dict:
        """
        Used to get information about the cost of the order, depending on
        the version, period and number of proxy.

        Method paremeters:
            count - (Required) - Number of proxies;
            period - (Required) - Period – number of days;
            version - Proxies version: 4 - IPv4, 3 - IPv4 Shared,
            6 - IPv6 (default).
        """
        return self.request(method="getprice", count=count, period=period, version=version)

    def get_count_in_country(self, country: str, version: int = None) -> Dict:
        """
        Displays the information on amount of proxies available to purchase for a selected country.

        Method parameters:
            country - (Required) - Country code in iso2 format
            version - Proxies version: 4 - IPv4, 3 - IPv4 Shared, 6 - IPv6 (default)
        """
        country = COUNTRIES_HUMAN_NAME_KEYS.get(country)
        return self.request(method="getcount", country=country, version=version)

    def get_countries(self, version: int = None) -> Union[list, str]:
        """
        Displays information on available for proxies purchase countries.

        Method paremeters:
            version - Proxies version: 4 - IPv4, 3 - IPv4 Shared, 6 - IPv6 (default).
        """
        response = self.request(method="getcountry", version=version)
        list_of_countries = response.get("list")
        if list_of_countries:
            human_readable_list = []
            for item in list_of_countries:
                human_readable_list.append(COUNTRIES_ISO2_KEYS.get(item))
            return human_readable_list
        return "Not available for proxies purchase countries"

    def get_proxy(
        self, state: str = None, descr: str = None, nokey: bool = False, page: int = None, limit: int = None
    ) -> Dict:
        """Method 'getproxy'. Displays the list of your proxies.

        Method parameters:

        state - State returned proxies. Available values:
            active - Active, expired - Not active, expiring - Expiring, all - All (default);
        descr - Technical comment you have entered when purchasing proxy. If you filled in this parameter,
            then the reply would display only those proxies with given parameter. If the parameter was not filled in,
            the reply would display all your proxies;
        nokey - By adding this parameter (the value is not needed), the list will be returned without keys;
        page - The page number to output. 1 - by default;
        limit - The number of proxies to output in the list. 1000 - by default (maximum value).
        """
        return self.request(method="getproxy", state=state, descr=descr, nokey=nokey, page=page, limit=limit)

    def set_type(self, ids: list[int], type: str) -> Dict:
        """
        Changes the type (protocol) in the proxy list.

        Method parameters:
            ids - (Required) - List of internal proxies numbers in our system, divided by comas;
            type - (Required) - Sets the type (protocol): http - HTTPS or socks - SOCKS5.
        """
        return self.request(method="settype", ids=ids, type=type)

    def set_descr(self, new: str, old: str = None, ids: list[int] = None) -> Dict:
        """
        Update technical comments in the proxy list that was added when buying (method buy).

        Method parameters:
            new - (Required) - Technical comment to which you want to change. The maximum length of 50 characters;
            old - Technical comment to be changed. The maximum length of 50 characters;
            ids - List of internal proxies numbers in our system, divided by comas.
            One of the parameters must be present - ids or descr.
        """
        return self.request(method="setdescr", new=new, old=old, ids=ids)

    def buy(
        self,
        count: int,
        period: int,
        country: str,
        version: int = None,
        type: str = None,
        descr: str = None,
        auto_prolong: bool = False,
        nokey: bool = False,
    ) -> Dict:
        """
        Used for proxy purchase.

        Method parameters:
            count - (Required) - Amount of proxies for purchase;
            period - (Required) - Period for which proxies are purchased in days;
            country - (Required) - Country in iso2 format;
            version - Proxies version: 4 - IPv4, 3 - IPv4 Shared, 6 - IPv6 (default);
            type - Proxies type (protocol): socks or http (default);
            descr - Technical comment for proxies list, max value 50 characters.
                Entering this parameter will help you to select certain proxies through getproxy method;
            auto_prolong - By adding this parameter (the value is not needed), enables the purchased proxy auto-renewal;
            nokey - By adding this parameter (the value is not needed), the list will be returned without keys.
        """
        return self.request(
            method="buy",
            count=count,
            period=period,
            country=country,
            version=version,
            type=type,
            descr=descr,
            auto_prolong=auto_prolong,
            nokey=nokey,
        )

    def prolong(self, period: int, ids: list[int], nokey: bool = False) -> Dict:
        """
        Used to extend existing proxies.

        Method parametres:
            period - (Required) - Extension period in days;
            ids - (Required) - List of internal proxies’ numbers in our system, divided by comas;
            nokey - By adding this parameter (the value is not needed), the list will be returned without keys.
        """
        return self.request(method="prolong", period=period, ids=ids, nokey=nokey)

    def delete(self, ids: list[int], descr: str = None) -> Dict:
        """
        Used to delete proxies.

        Method parametres:
            ids - (Required) - List of internal proxies’ numbers in our system, divided by comas;
            descr - (Required) - Technical comment you have entered when purchasing proxy or by method setdescr.
            One of the parameters must be present - ids or descr.
        """
        return self.request(method="delete", ids=ids, descr=descr)

    def check(self, ids: int) -> Dict:
        """
        Used to check the validity of the proxy.

        Method parametres:
            ids - (Required) - Internal proxy number in our system.
        """
        return self.request(method="check", ids=ids)

    @property
    def balance(self) -> str:
        response = self.request(method="")
        if not isinstance(response, dict):
            return response
        return f"{response['balance']} {response['currency']}"
