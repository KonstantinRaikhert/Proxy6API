from datetime import datetime
from typing import Dict, Union

import requests
from requests.exceptions import ConnectionError, ConnectTimeout, JSONDecodeError

from proxy6api.settings.bases import COUNTRIES_HUMAN_NAME_KEYS, COUNTRIES_ISO2_KEYS
from proxy6api.settings.errors import CODES_OF_ERRORS
from proxy6api.settings.typing_methods import (
    BalanceInfo,
    BuyInfo,
    CheckInfo,
    CountInfo,
    CountriesInfo,
    DeleteInfo,
    ErrorInfo,
    PriceInfo,
    ProlongInfo,
    ProlongItemInfo,
    ProxyInfo,
    ProxyItemInfo,
    SetDescrInfo,
    SetTypeInfo,
)


class Proxy_6_Client:
    """
    The API is accessed at:
    https://proxy6.net/api/{api_key}/{method}/?{params}

    url: https://proxy6.net/api/
    api_key: api_key
    """

    def __init__(self, api_key: str) -> None:
        self._url: str = "https://proxy6.net/api"
        self.__api_key = api_key

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

    @staticmethod
    def _convert_str_date_to_datetime_type(date: str) -> datetime:
        pattern = "%Y-%m-%d %H:%M:%S"
        return datetime.strptime(date, pattern)

    def _request(self, method: str, **query_params) -> Union[Dict, ErrorInfo]:
        try:
            url = f"{self._url}/{self.__api_key}/{method}"
            if query_params:
                params_of_method = Proxy_6_Client._query_params_of_method(**query_params)
                url += params_of_method
            response_json = requests.get(url=url).json()
            if response_json.get("error"):
                response_json["error"] = CODES_OF_ERRORS.get(response_json["error_id"])
                return ErrorInfo(error_id=int(response_json["error_id"]), error=response_json["error"])
            return response_json
        except JSONDecodeError:
            error_id = 10
            return ErrorInfo(error_id=error_id, error=CODES_OF_ERRORS[error_id])
        except ConnectionError:
            error_id = 20
            return ErrorInfo(error_id=error_id, error=CODES_OF_ERRORS[error_id])
        except ConnectTimeout:
            error_id = 25
            return ErrorInfo(error_id=error_id, error=CODES_OF_ERRORS[error_id])

    def get_price(self, count: int, period: int, version: int = None) -> Union[PriceInfo, ErrorInfo]:
        """
        Used to get information about the cost of the order, depending on
        the version, period and number of proxy.

        Method paremeters:

            count - (Required) - Number of proxies;
            period - (Required) - Period – number of days;
            version - Proxies version: 4 - IPv4, 3 - IPv4 Shared,
            6 - IPv6 (default).
        """
        response = self._request(method="getprice", count=count, period=period, version=version)
        if isinstance(response, ErrorInfo):
            return response
        return PriceInfo(
            status=response["status"],
            user_id=int(response["user_id"]),
            balance=float(response["balance"]),
            currency=response["currency"],
            price=float(response["price"]),
            price_single=float(response["price_single"]),
            period=int(response["period"]),
            count=int(response["count"]),
        )

    def get_count_in_country(self, country: str, version: int = None) -> Union[CountInfo, ErrorInfo]:
        """
        Displays the information on amount of proxies available to purchase for a selected country.

        Method parameters:
            country - (Required) - Country code in iso2 format or name of the country(russian language)
            version - Proxies version: 4 - IPv4, 3 - IPv4 Shared, 6 - IPv6 (default)
        """
        country = country if len(country) == 2 else COUNTRIES_HUMAN_NAME_KEYS.get(country)
        response = self._request(method="getcount", country=country, version=version)
        if isinstance(response, ErrorInfo):
            return response
        return CountInfo(
            status=response["status"],
            user_id=int(response["user_id"]),
            balance=float(response["balance"]),
            currency=response["currency"],
            count=int(response["count"]),
        )

    def get_countries(self, version: int = None, rus: bool = False) -> Union[CountriesInfo, ErrorInfo]:
        """
        Displays information on available for proxies purchase countries.

        Method paremeters:

            version - Proxies version: 4 - IPv4, 3 - IPv4 Shared, 6 - IPv6 (default).

            rus - Returns the names of countries in Russian.
        """
        response = self._request(method="getcountry", version=version)
        if isinstance(response, ErrorInfo):
            return response
        if rus:
            list_of_countries = response.get("list")
            if list_of_countries:
                human_readable_list = []
                for item in list_of_countries:
                    human_readable_list.append(COUNTRIES_ISO2_KEYS.get(item))
                response["list"] = human_readable_list
        return CountriesInfo(
            status=response["status"],
            user_id=int(response["user_id"]),
            balance=float(response["balance"]),
            currency=response["currency"],
            countries_list=response["list"],
        )

    def get_proxy(
        self, state: str = None, descr: str = None, page: int = None, limit: int = None
    ) -> Union[ProxyInfo, ErrorInfo]:
        """Method 'getproxy'. Displays the list of your proxies.

        Method parameters:

        state - State returned proxies. Available values:
            active - Active, expired - Not active, expiring - Expiring, all - All (default);
        descr - Technical comment you have entered when purchasing proxy. If you filled in this parameter,
            then the reply would display only those proxies with given parameter. If the parameter was not filled in,
            the reply would display all your proxies;
        page - The page number to output. 1 - by default;
        limit - The number of proxies to output in the list. 1000 - by default (maximum value).
        """
        response = self._request(method="getproxy", state=state, descr=descr, nokey=True, page=page, limit=limit)
        if isinstance(response, ErrorInfo):
            return response
        return ProxyInfo(
            status=response["status"],
            user_id=int(response["user_id"]),
            balance=float(response["balance"]),
            currency=response["currency"],
            list_count=int(response["list_count"]),
            date_mod=Proxy_6_Client._convert_str_date_to_datetime_type(response["date_mod"]),
            proxies_list=[
                ProxyItemInfo(
                    id=int(item["id"]),
                    ip=item["ip"],
                    host=item["host"],
                    port=item["port"],
                    user=item["user"],
                    password=item["pass"],
                    proxy_type=item["type"],
                    country=item["country"],
                    date=Proxy_6_Client._convert_str_date_to_datetime_type(item["date"]),
                    date_end=Proxy_6_Client._convert_str_date_to_datetime_type(item["date_end"]),
                    unixtime=int(item["unixtime"]),
                    unixtime_end=int(item["unixtime_end"]),
                    descr=item["descr"],
                    active=bool(item["active"]),
                )
                for item in response["list"]
            ],
            page=int(response["page"]),
        )

    def set_type(self, ids: list[int], type: str) -> Union[SetTypeInfo, ErrorInfo]:
        """
        Changes the type (protocol) in the proxy list.

        Method parameters:
            ids - (Required) - List of internal proxies numbers in our system, divided by comas;
            type - (Required) - Sets the type (protocol): http - HTTPS or socks - SOCKS5.
        """
        response = self._request(method="settype", ids=ids, type=type)
        if isinstance(response, ErrorInfo):
            return response
        return SetTypeInfo(
            status=response["status"],
            user_id=int(response["user_id"]),
            balance=float(response["balance"]),
            currency=response["currency"],
        )

    def set_descr(self, new: str, old: str = None, ids: list[int] = None) -> Union[SetDescrInfo, ErrorInfo]:
        """
        Update technical comments in the proxy list that was added when buying (method buy).

        Method parameters:
            new - (Required) - Technical comment to which you want to change. The maximum length of 50 characters;
            old - Technical comment to be changed. The maximum length of 50 characters;
            ids - List of internal proxies numbers in our system, divided by comas.
            One of the parameters must be present - ids or descr.
        """
        response = self._request(method="setdescr", new=new, old=old, ids=ids)
        if isinstance(response, ErrorInfo):
            return response
        return SetDescrInfo(
            status=response["status"],
            user_id=int(response["user_id"]),
            balance=float(response["balance"]),
            currency=response["currency"],
            count=response["count"],
        )

    def buy(
        self,
        count: int,
        period: int,
        country: str,
        version: int = None,
        type: str = None,
        descr: str = None,
        auto_prolong: bool = False,
    ) -> Union[BuyInfo, ErrorInfo]:
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
            auto_prolong - By adding this parameter (the value is not needed), enables the purchased proxy auto-renewal.
        """
        response = self._request(
            method="buy",
            count=count,
            period=period,
            country=country,
            version=version,
            type=type,
            descr=descr,
            auto_prolong=auto_prolong,
            nokey=True,
        )
        if isinstance(response, ErrorInfo):
            return response
        return BuyInfo(
            status=response["status"],
            user_id=int(response["user_id"]),
            balance=float(response["balance"]),
            currency=response["currency"],
            count=int(response["count"]),
            date_mod=Proxy_6_Client._convert_str_date_to_datetime_type(response["date_mod"]),
            price=float(response["price"]),
            period=int(response["period"]),
            country=response["country"],
            proxies_list=[
                ProxyItemInfo(
                    id=int(item["id"]),
                    ip=item["ip"],
                    host=item["host"],
                    port=item["port"],
                    user=item["user"],
                    password=item["pass"],
                    proxy_type=item["type"],
                    country=response["country"],
                    date=Proxy_6_Client._convert_str_date_to_datetime_type(item["date"]),
                    date_end=Proxy_6_Client._convert_str_date_to_datetime_type(item["date_end"]),
                    unixtime=int(item["unixtime"]),
                    unixtime_end=int(item["unixtime_end"]),
                    descr=descr,
                    active=bool(item["active"]),
                )
                for item in response["list"]
            ],
        )

    def prolong(self, period: int, ids: list[int]) -> Union[ProlongInfo, ErrorInfo]:
        """
        Used to extend existing proxies.

        Method parametres:
            period - (Required) - Extension period in days;
            ids - (Required) - List of internal proxies’ numbers in our system, divided by comas;
            nokey - By adding this parameter (the value is not needed), the list will be returned without keys.
        """
        response = self._request(method="prolong", period=period, ids=ids, nokey=True)
        if isinstance(response, ErrorInfo):
            return response
        return ProlongInfo(
            status=response["status"],
            user_id=int(response["user_id"]),
            balance=float(response["balance"]),
            currency=response["currency"],
            date_mod=Proxy_6_Client._convert_str_date_to_datetime_type(response["date_mod"]),
            price=float(response["price"]),
            period=int(response["period"]),
            count=int(response["count"]),
            proxies_list=[
                ProlongItemInfo(
                    id=int(item["id"]),
                    date_end=Proxy_6_Client._convert_str_date_to_datetime_type(item["date_end"]),
                    unixtime_end=int(item["unixtime_end"]),
                )
                for item in response["list"]
            ],
        )

    def delete(self, ids: list[int], descr: str = None) -> Union[DeleteInfo, ErrorInfo]:
        """
        Used to delete proxies.

        Method parametres:
            ids - (Required) - List of internal proxies’ numbers in our system, divided by comas;
            descr - (Required) - Technical comment you have entered when purchasing proxy or by method setdescr.
            One of the parameters must be present - ids or descr.
        """
        response = self._request(method="delete", ids=ids, descr=descr)
        if isinstance(response, ErrorInfo):
            return response
        return DeleteInfo(
            status=response["status"],
            user_id=int(response["user_id"]),
            balance=float(response["balance"]),
            currency=response["currency"],
            count=int(response["count"]),
        )

    def check(self, ids: list[int]) -> Union[CheckInfo, ErrorInfo]:
        """
        Used to check the validity of the proxy.

        Method parametres:
            ids - (Required) - Internal proxy number in our system.
        """
        response = self._request(method="check", ids=ids)
        if isinstance(response, ErrorInfo):
            return response
        return CheckInfo(
            status=response["status"],
            user_id=int(response["user_id"]),
            balance=float(response["balance"]),
            currency=response["currency"],
            date_mod=Proxy_6_Client._convert_str_date_to_datetime_type(response["date_mod"]),
            proxy_id=int(response["proxy_id"]),
            proxy_status=response["proxy_status"],
            proxy_time=float(response["proxy_time"]),
        )

    @property
    def balance(self) -> Union[BalanceInfo, ErrorInfo]:
        response = self._request(method="")
        if isinstance(response, ErrorInfo):
            return response
        return BalanceInfo(balance=float(response["balance"]), currency=response["currency"])
