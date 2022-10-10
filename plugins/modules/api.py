#!/usr/bin/python

# Copyright: (c) 2022, NVIDIA <nvidia.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from __future__ import absolute_import, division, print_function

__metaclass__ = type


DOCUMENTATION = r"""
author: Nvidia NBU team
short_description: Use httpapi to run command on NVUE devices
description:
- This connection plugin provides a connection to NVUE over an HTTP(S)-based
  api.
"""
EXAMPLES = r"""
# Pass in a message
- name: Test with a message
  my_namespace.my_collection.my_test:
    name: hello world

# pass in a message and have changed true
- name: Test with a message and changed output
  my_namespace.my_collection.my_test:
    name: hello world
    new: true

# fail the module
- name: Test failure of the module
  my_namespace.my_collection.my_test:
    name: fail me
"""

RETURN = r"""
# These are examples of possible return values, and in general should use other names for return values.
original_message:
    description: The original name param that was passed in.
    type: str
    returned: always
    sample: "hello world"
message:
    description: The output message that the test module generates.
    type: str
    returned: always
    sample: "goodbye"
"""

import json
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.connection import Connection
from ansible.module_utils.six import string_types
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.utils import (
    dict_diff,
)


def main():
    """entry point for module execution"""
    module_args = {
        "operation": {
            "type": str,
            "choices": ["get", "set"],
            "default": "get",
        },
        "force": {"type": bool, "required": False, "default": False},
        "wait": {"type": int, "required": False, "default": 0},
        "path": {"type": str, "required": False, "default": "/"},
        "data": {"type": dict, "required": False, "default": {}},
    }

    required_if = [
        ["operation", "set", ["data"]],
    ]

    module = AnsibleModule(
        argument_spec=module_args,
        required_if=required_if,
        supports_check_mode=True,
    )

    path = module.params["path"]
    data = module.params["data"]
    operation = module.params["operation"]
    force = module.params["force"]
    wait = module.params["wait"]

    if isinstance(data, string_types):
        data = json.loads(data)

    warnings = list()
    result = {"changed": False, "warnings": warnings}

    running = None
    commit = not module.check_mode

    connection = Connection(module._socket_path)
    response = connection.send_request(data, path, operation, force=force, wait=wait)
    if operation == "set" and response:
        result["changed"] = True
    result["message"] = response

    module.exit_json(**result)


if __name__ == "__main__":
    main()
