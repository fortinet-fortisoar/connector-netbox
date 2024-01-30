"""
Copyright start
MIT License
Copyright (c) 2024 Fortinet Inc
Copyright end
"""

import json

import requests
from connectors.core.connector import get_logger, ConnectorError

from .constants import *

logger = get_logger('netbox')


class Netbox:
    def __init__(self, config):
        self.server_url = config.get('server_url')
        if not (self.server_url.startswith('https://') or self.server_url.startswith('http://')):
            self.server_url = 'https://' + self.server_url
        self.server_url = self.server_url.strip('/')
        self.api_key = config.get('api_key')
        self.verify_ssl = config.get('verify_ssl')

    def make_request(self, endpoint, method='get', data=None, params=None, files=None):
        try:
            url = self.server_url + endpoint
            logger.info('Executing url {}'.format(url))
            headers = {'Authorization': f"Token {self.api_key}", 'Content-Type': 'application/json'}

            # CURL UTILS CODE
            try:
                from connectors.debug_utils.curl_script import make_curl
                make_curl(method, endpoint, headers=headers, params=params, data=data, verify_ssl=self.verify_ssl)
            except Exception as err:
                logger.error(f"Error in curl utils: {str(err)}")

            response = requests.request(method, url, params=params, files=files, data=data, headers=headers,
                                        verify=self.verify_ssl)
            if response.ok:
                logger.info('successfully get response for url {}'.format(url))
                if method.lower() == 'delete':
                    return "Successfully Deleted"
                else:
                    return response.json()
            elif response.status_code == 400:
                error_response = response.json()
                if error_response.get("detail") is not None:
                    raise ConnectorError(error_response.get("detail"))
                else:
                    raise ConnectorError(error_response)
            elif response.status_code == 401:
                error_response = response.json()
                if error_response.get('error'):
                    error_description = error_response['error']
                else:
                    error_description = error_response.get('detail')
                raise ConnectorError({'error_description': error_description})
            elif response.status_code == 404:
                error_response = response.json()
                error_description = error_response.get('detail')
                raise ConnectorError(error_description)
            else:
                logger.error(response.json())
        except requests.exceptions.SSLError:
            raise ConnectorError('SSL certificate validation failed')
        except requests.exceptions.ConnectTimeout:
            raise ConnectorError('The request timed out while trying to connect to the server')
        except requests.exceptions.ReadTimeout:
            raise ConnectorError('The server did not send any data in the allotted amount of time')
        except requests.exceptions.ConnectionError:
            raise ConnectorError('Invalid endpoint or credentials')
        except Exception as err:
            raise ConnectorError(str(err))
        raise ConnectorError(response.text)


def get_ip_address_list(config: dict, params: dict):
    try:
        nb = Netbox(config)
        params = _build_payload(params)

        endpoint = f'/api/ipam/ip-addresses/'
        return nb.make_request(endpoint=endpoint, method='GET', params=params)
    except Exception as err:
        logger.error(str(err))
        raise ConnectorError(str(err))


def get_ip_address(config: dict, params: dict):
    try:
        nb = Netbox(config)
        params = _build_payload(params)

        endpoint = f'/api/ipam/ip-addresses/{params.get("id")}/'
        return nb.make_request(endpoint=endpoint, method='GET', params=params)
    except Exception as err:
        logger.error(str(err))
        raise ConnectorError(str(err))


def update_ip_address(config: dict, params: dict):
    try:
        nb = Netbox(config)
        params = _build_payload(params)

        endpoint = f'/api/ipam/ip-addresses/{params.pop("id")}/'
        return nb.make_request(endpoint=endpoint, method='PATCH', data=json.dumps(params.get("patch_fields")))
    except Exception as err:
        logger.error(str(err))
        raise ConnectorError(str(err))


def delete_ip_address(config: dict, params: dict):
    try:
        nb = Netbox(config)
        params = _build_payload(params)

        endpoint = f'/api/ipam/ip-addresses/{params.pop("id")}/'
        return nb.make_request(endpoint=endpoint, method='DELETE')
    except Exception as err:
        logger.error(str(err))
        raise ConnectorError(str(err))


def get_prefix_list(config: dict, params: dict):
    try:
        nb = Netbox(config)
        params = _build_payload(params)

        endpoint = '/api/ipam/prefixes/'
        return nb.make_request(endpoint=endpoint, method='GET', params=params)
    except Exception as err:
        logger.error(str(err))
        raise ConnectorError(str(err))


def get_prefix(config: dict, params: dict):
    try:
        nb = Netbox(config)
        params = _build_payload(params)

        endpoint = f'/api/ipam/prefixes/{params.get("id")}/'
        return nb.make_request(endpoint=endpoint, method='GET', params=params)
    except Exception as err:
        logger.error(str(err))
        raise ConnectorError(str(err))


def update_prefix(config: dict, params: dict):
    try:
        nb = Netbox(config)
        params = _build_payload(params)

        endpoint = f'/api/ipam/prefixes/{params.get("id")}/'
        return nb.make_request(endpoint=endpoint, method='PATCH', data=json.dumps(params.get("patch_fields")))
    except Exception as err:
        logger.error(str(err))
        raise ConnectorError(str(err))


def delete_prefix(config: dict, params: dict):
    try:
        nb = Netbox(config)
        params = _build_payload(params)

        endpoint = f'/api/ipam/prefixes/{params.get("id")}/'
        return nb.make_request(endpoint=endpoint, method='DELETE')
    except Exception as err:
        logger.error(str(err))
        raise ConnectorError(str(err))


def get_vm_list(config: dict, params: dict):
    try:
        nb = Netbox(config)
        params = _build_payload(params)

        endpoint = '/api/virtualization/virtual-machines/'
        return nb.make_request(endpoint=endpoint, method='GET', params=params)
    except Exception as err:
        logger.error(str(err))
        raise ConnectorError(str(err))


def get_vm(config: dict, params: dict):
    try:
        nb = Netbox(config)
        params = _build_payload(params)

        endpoint = f'/api/virtualization/virtual-machines/{params.get("id")}/'
        return nb.make_request(endpoint=endpoint, method='GET', params=params)
    except Exception as err:
        logger.error(str(err))
        raise ConnectorError(str(err))


def update_vm(config: dict, params: dict):
    try:
        nb = Netbox(config)
        params = _build_payload(params)

        endpoint = f'/api/virtualization/virtual-machines/{params.get("id")}/'
        return nb.make_request(endpoint=endpoint, method='PATCH', data=json.dumps(params.get("patch_fields")))
    except Exception as err:
        logger.error(str(err))
        raise ConnectorError(str(err))


def delete_vm(config: dict, params: dict):
    try:
        nb = Netbox(config)
        params = _build_payload(params)

        endpoint = f'/api/virtualization/virtual-machines/{params.get("id")}/'
        return nb.make_request(endpoint=endpoint, method='DELETE')
    except Exception as err:
        logger.error(str(err))
        raise ConnectorError(str(err))


def get_rack_list(config: dict, params: dict):
    try:
        nb = Netbox(config)
        params = _build_payload(params)

        endpoint = '/api/dcim/racks/'
        return nb.make_request(endpoint=endpoint, method='GET', params=params)
    except Exception as err:
        logger.error(str(err))
        raise ConnectorError(str(err))


def get_rack(config: dict, params: dict):
    try:
        nb = Netbox(config)
        params = _build_payload(params)

        endpoint = f'/api/dcim/racks/{params.get("id")}/'
        return nb.make_request(endpoint=endpoint, method='GET', params=params)
    except Exception as err:
        logger.error(str(err))
        raise ConnectorError(str(err))


def update_rack(config: dict, params: dict):
    try:
        nb = Netbox(config)
        params = _build_payload(params)

        endpoint = f'/api/dcim/racks/{params.get("id")}/'
        return nb.make_request(endpoint=endpoint, method='PATCH', data=json.dumps(params.get("patch_fields")))
    except Exception as err:
        logger.error(str(err))
        raise ConnectorError(str(err))


def delete_rack(config: dict, params: dict):
    try:
        nb = Netbox(config)
        params = _build_payload(params)

        endpoint = f'/api/dcim/racks/{params.get("id")}/'
        return nb.make_request(endpoint=endpoint, method='DELETE')
    except Exception as err:
        logger.error(str(err))
        raise ConnectorError(str(err))


def get_device_list(config: dict, params: dict):
    try:
        nb = Netbox(config)
        params = _build_payload(params)
        endpoint = '/api/dcim/devices/'
        return nb.make_request(endpoint=endpoint, method='GET', params=params)
    except Exception as err:
        logger.error(str(err))
        raise ConnectorError(str(err))


def get_device(config: dict, params: dict):
    try:
        nb = Netbox(config)
        params = _build_payload(params)

        endpoint = f'/api/dcim/devices/{params.get("id")}/'
        return nb.make_request(endpoint=endpoint, method='GET', params=params)
    except Exception as err:
        logger.error(str(err))
        raise ConnectorError(str(err))


def update_device(config: dict, params: dict):
    try:
        nb = Netbox(config)
        params = _build_payload(params, False)
        logger.info(f"After Build Payload params is {params}")
        endpoint = f'/api/dcim/devices/{params.get("id")}/'
        return nb.make_request(endpoint=endpoint, method='PATCH', data=json.dumps(params))
    except Exception as err:
        logger.error(str(err))
        raise ConnectorError(str(err))


def delete_device(config: dict, params: dict):
    try:
        nb = Netbox(config)
        params = _build_payload(params)

        endpoint = f'/api/dcim/devices/{params.get("id")}/'
        return nb.make_request(endpoint=endpoint, method='DELETE')
    except Exception as err:
        logger.error(str(err))
        raise ConnectorError(str(err))


def get_cable_list(config: dict, params: dict):
    try:
        nb = Netbox(config)
        params = _build_payload(params)

        endpoint = '/api/dcim/cables/'
        return nb.make_request(endpoint=endpoint, method='GET', params=params)
    except Exception as err:
        logger.error(str(err))
        raise ConnectorError(str(err))


def get_cable(config: dict, params: dict):
    try:
        nb = Netbox(config)
        params = _build_payload(params)

        endpoint = f'/api/dcim/cables/{params.get("id")}/'
        return nb.make_request(endpoint=endpoint, method='GET', params=params)
    except Exception as err:
        logger.error(str(err))
        raise ConnectorError(str(err))


def update_cable(config: dict, params: dict):
    try:
        nb = Netbox(config)
        params = _build_payload(params)

        endpoint = f'/api/dcim/cables/{params.get("id")}/'
        return nb.make_request(endpoint=endpoint, method='PATCH', data=json.dumps(params.get("patch_fields")))
    except Exception as err:
        logger.error(str(err))
        raise ConnectorError(str(err))


def delete_cable(config: dict, params: dict):
    try:
        nb = Netbox(config)
        params = _build_payload(params)

        endpoint = f'/api/dcim/cables/{params.get("id")}/'
        return nb.make_request(endpoint=endpoint, method='DELETE')
    except Exception as err:
        logger.error(str(err))
        raise ConnectorError(str(err))


def _check_health(config):
    try:
        tg = Netbox(config)
        endpoint = '/api/dcim/sites/'
        response = tg.make_request(endpoint=endpoint, params={'limit': 5})
        if response:
            logger.info("Connector Available")
            return True
        return False
    except Exception as err:
        logger.error(str(err))
        raise ConnectorError(str(err))


def _build_payload(params, use_csv_params=True):
    logger.info(f"Inside Build Payload params is {params}")
    if use_csv_params:
        csv_params = ["site", "region", "rack_id", "asset_tag", "tenant", "tag", "type", "name", "role", "prefix"]
        for p in csv_params:
            if params.get(p) is not None and params.get(p) != "":
                params.update({f"{p}": params.get(p).split(",")})

    if params.get('family') is not None and params.get('family') != "":
        params.update({'family': format_dict.get(params.get('family'))})

    if params.get("other_fields") is not None:
        other_fields = params.pop("other_fields")
        params.update(other_fields)

    return {key: val for key, val in params.items() if val is not None and val != ''}


operations = {
    "get_ip_address_list": get_ip_address_list,
    "get_ip_address": get_ip_address,
    "update_ip_address": update_ip_address,
    "delete_ip_address": delete_ip_address,
    "get_prefix_list": get_prefix_list,
    "get_prefix": get_prefix,
    "update_prefix": update_prefix,
    "delete_prefix": delete_prefix,
    "get_vm_list": get_vm_list,
    "get_vm": get_vm,
    "update_vm": update_vm,
    "delete_vm": delete_vm,
    "get_rack_list": get_rack_list,
    "get_rack": get_rack,
    "update_rack": update_rack,
    "delete_rack": delete_rack,
    "get_device_list": get_device_list,
    "get_device": get_device,
    "update_device": update_device,
    "delete_device": delete_device,
    "get_cable_list": get_cable_list,
    "get_cable": get_cable,
    "update_cable": update_cable,
    "delete_cable": delete_cable
}