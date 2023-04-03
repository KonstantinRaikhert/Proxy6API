from dataclasses import dataclass
from typing import Dict, Union

import requests
from requests.exceptions import ConnectTimeout
from settings.bases import COUNTRIES_HUMAN_NAME_KEYS, COUNTRIES_ISO2_KEYS
from settings.config import PROXY_6_API_KEY
from settings.errors import CODES_OF_ERRORS


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
    def _params_of_method(**params) -> str:
        """Converts the request parameters to a string"""
        params_string: str = "?"
        for key, value in params.items():
            params_string += f"{key}={value}&"
        return params_string

    def request(self, method: str, **params) -> Union[Dict, str]:
        try:
            url = f"{self.url}/{self.api_key}/{method}"
            if params:
                params_of_method = Proxy_6_Client._params_of_method(**params)
                url += params_of_method
            response_json = requests.get(url=url).json()
            if response_json.get("error"):
                return CODES_OF_ERRORS.get(response_json["error_id"])
            return response_json
        except ConnectTimeout as er:
            return er

    def get_price(self, count: int, period: int, version: int = None) -> request:
        """
        Used to get information about the cost of the order, depending on
        the version, period and number of proxy.

        Method paremeters:
            count - (Required) - Number of proxies;
            period - (Required) - Period – number of days;
            version - Proxies version: 4 - IPv4, 3 - IPv4 Shared,
            6 - IPv6 (default).
        """
        return self.request(
            method="getprice",
            count=count,
            period=period,
            version=version,
        )

    def get_count_in_country(self, country: str, version: int = None) -> request:
        """
        Displays the information on amount of proxies available to purchase for a selected country.

        Method parameters:
            country - (Required) - Country code in iso2 format
            version - Proxies version: 4 - IPv4, 3 - IPv4 Shared, 6 - IPv6 (default)
        """
        country = COUNTRIES_HUMAN_NAME_KEYS.get(country)
        return self.request(
            method="getcount",
            country=country,
            version=version,
        )

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


if __name__ == "__main__":
    api_url = Proxy_6_API_URL(api_key=PROXY_6_API_KEY)
    client = Proxy_6_Client(api_url=api_url)
    print(client.get_price(count=5, period=5, version=3))
    # print(client.get_count_in_country(country="Германия", version=6))
