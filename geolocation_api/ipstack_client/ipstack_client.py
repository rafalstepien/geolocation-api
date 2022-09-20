import json

import requests
from pydantic.error_wrappers import ValidationError

from geolocation_api.config_loader import config
from geolocation_api.error_handler import ErrorHandler, handle_errors
from geolocation_api.ipstack_client.constants import IPSTACK_BASE_URL
from geolocation_api.ipstack_client.models import IpstackGeneralInformationModel


class IpstackClient:
    def get_data_for_ip_address(self, ip_address: str):
        response = requests.get(f"{IPSTACK_BASE_URL}{ip_address}?access_key={config.IPSTACK_ACCESS_KEY}")
        return self._parse_upstream_response(response)

    @staticmethod
    def _parse_upstream_response(response: requests.Response) -> IpstackGeneralInformationModel:
        with handle_errors(json.JSONDecodeError):
            response_as_dictionary = json.loads(response.content.decode("utf-8"))

        if IpstackClient._is_success_response(response_as_dictionary):
            with handle_errors(ValidationError):
                return IpstackGeneralInformationModel(**response_as_dictionary)

        else:
            ErrorHandler().handle_ipstack_error_response(response_as_dictionary)

    @staticmethod
    def _is_success_response(response: dict) -> bool:
        if response.get("success") is not None:
            return response.get("success")
        return True
