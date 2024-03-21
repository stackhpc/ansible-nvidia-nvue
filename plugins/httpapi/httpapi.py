# Copyright: (c) 2022, NVIDIA <nvidia.com>
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
author: Nvidia NBU Team (@nvidia-nbu)
name: httpapi
short_description: httpapi plugin for NVIDIA's NVUE API
description:
- This connection plugin provides a connection to devices with
  NVIDIA's NVUE API over HTTP(S)-based
"""

from ansible.module_utils.six.moves.urllib.error import HTTPError
from ansible_collections.ansible.netcommon.plugins.plugin_utils.httpapi_base \
    import HttpApiBase
import urllib
import json
import time


class HttpApi(HttpApiBase):

    def __init__(self, connection):
        super(HttpApi, self).__init__(connection)
        self.prefix = "/nvue_v1"
        self.headers = {"Content-Type": "application/json"}

    def send_request(self, data, path, operation, **kwargs):
        if path == "revision":
            if operation == "new":
                return self.create_revision()
            elif operation == "apply":
                self.revisionID = kwargs.get("revid")
                return self.apply_config(**kwargs)
        if operation == "set":
            return self.set_operation(data, path, **kwargs)
        elif operation == "get":
            params = {"rev": "applied"}
            if path == "/":
                path = ""
                if not kwargs.get("filled"):
                    params['filled'] = 'false'
            path = f"{self.prefix}/{path}?{urllib.parse.urlencode(params)}"
            return self.get_operation(path)

    def get_operation(self, path):
        response, response_data = self.connection.send(
            path, "", headers=self.headers, method="GET"
        )
        return handle_response(response, response_data)

    def set_operation(self, data, path, **kwargs):
        """
          If revid is not passed as part of the list of paramaters,
          create a new revision ID
        """
        if kwargs.get("revid"):
            self.revisionID = kwargs.get("revid")
        else:
            self.revisionID = self.create_revision()
        normalized_keys_data = self.normalize_keys(data)
        normalized_data = self.normalize_spec(normalized_keys_data)
        result = self.patch_revision(path, normalized_data)
        if kwargs.get("revid"):
            return result
        else:
            return self.apply_config(**kwargs)

    def normalize_keys(self, data):
        """
        Function normalize all the keys
        Replace all underscore seperated keys with hyphen seperated keys.
        For example, mac_flooding is replaced with mac-flooding
        """
        new_config = {}
        if isinstance(data, dict):
            if not bool(data):
                return new_config
            for key, value in data.items():
                new_config[key.replace("_", "-")] = self.normalize_keys(value)
        elif isinstance(data, list):
            if not len(data):
                return new_config
            new_config = []
            for items in data:
                new_config.append(self.normalize_keys(items))
        else:
            return data
        return new_config

    def normalize_spec(self, data):
        """
        Function to normalize config parameters
        Remove the input value id and make it a dictionary
        with the rest of the values.
        For example, in bridges, we take id as an input:
        config:
            - id: br_default
              untagged: 1
              type: vlan-aware
              vlan:
                - id: 10
                  vni:
                    - id: 10
                - id: 20
                  vni:
                    - id: 20
        This needs to be converted for the API as below:
        {
            'br_default':
            {
                'type': 'vlan-aware',
                'untagged': '1',
                'vlan':
                {
                    '10':
                    {
                        'vni':
                        {
                            '10': {}
                        }
                    },
                    '20':
                    {
                        'vni':
                        {
                            '20': {}
                        }
                    }
                }
            }
        }

        """
        new_config = {}
        if isinstance(data, dict):
            if not bool(data):
                return new_config
            for key, value in data.items():
                new_config[key] = self.normalize_spec(value)
        elif isinstance(data, list):
            if not len(data):
                return new_config
            for item in data:
                if "id" in item:
                    id = item.pop('id')
                    if any(item.values()):
                        new_config[id] = item
                    else:
                        new_config[id] = {}
                    for key, value in item.items():
                        if value:
                            new_config[id][key] = self.normalize_spec(value)
        else:
            return data

        return new_config

    def create_revision(self):
        path = "/".join([self.prefix, "revision"])
        response, response_data = self.connection.send(
            path, dict(), method="POST", headers=self.headers
        )

        for k in handle_response(response, response_data):
            return k

    def patch_revision(self, path, data):
        params = {"rev": self.revisionID}
        if path == "/":
            path = ""
        path = f"{self.prefix}/{path}?{urllib.parse.urlencode(params)}"
        response, response_data = self.connection.send(
            path, json.dumps(data), headers=self.headers, method="PATCH"
        )

        return handle_response(response, response_data)

    def apply_config(self, **kwargs):

        force = kwargs.get("force", False)
        wait = kwargs.get("wait", 0)
        path = "/".join(
            [self.prefix, "revision", self.revisionID.replace("/", "%2F")])

        data = {"state": "apply"}
        if force:
            data["auto-prompt"] = {
                "ays": "ays_yes",
                "ignore_fail": "ignore_fail_yes",
            }

        response, response_data = self.connection.send(
            path,
            json.dumps(data),
            headers=self.headers,
            method="PATCH",
        )

        result = handle_response(response, response_data)

        while wait >= 0:
            result = self.get_operation(path)
            if result.get("state") == "applied":
                break
            time.sleep(1)
            wait -= 1
        return result


def handle_response(response, response_data):
    try:
        response_data = json.loads(response_data.read())
    except ValueError:
        response_data.seek(0)
        response_data = response_data.read()

    if isinstance(response, HTTPError):
        raise Exception(f"Connection error: {response}, data: {response_data}")

    return response_data
