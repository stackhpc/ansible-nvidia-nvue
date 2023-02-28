#!/usr/bin/python

# Copyright: (c) 2022 NVIDIA
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: mlag

short_description: This is the Cumulus Linux MLAG module

version_added: '1.0.0'

description: This is a Cumulus Linux module to interact with the MLAG object.

options:
    filters:
        description: Filters used while fetching information about mlag
        type: dict
        elements: dict
        suboptions:
            rev:
                description: The default is to query the operational state. However, this parameter can be used to query desired state on configuration
                             branches, such as startup and applied. This could be a branch name, tag name or specific commit.
                required: false
                type: str
            omit:
                description: Drop any JSON properties matched by an omit pattern from the response.
                required: false
                type: list
            include:
                description: Only include JSON properties matched by an include pattern in the response.
                required: false
                type: list
    data:
        description: Provided configuration
        type: dict
        elements: dict
        suboptions:
            enable:
                description: Turn the feature 'on' or 'off'.
                required: false
                type: str
                default: off
                choices:
                    - on
                    - off
            backup:
                description: MLAG Backup
                required: false
                type: dict
                elements: dict
                suboptions:
                    id:
                        description: Alternative ip address or interface for peer to reach us.
                        required: false
                        type: str
                    vrf:
                        description: The backup IP's VRF.
                        required: false
                        type: str
            init_delay:
                description: MLAG delay
                required: false
                type: int
            mac_address:
                description: Mac Address
                required: false
                type: str
            priority:
                description: MLAG Priority
                required: false
                type: str
            peer_ip:
                description: Peer IP address
                required: false
                type: str


    state:
        description: Defines the action to be taken
        required: true
        type: str
        choices:
            - gathered
            - deleted
            - merged
    force:
        description: When true, replies "yes" to NVUE prompts.
        required: false
        default: false
        type: bool
    wait:
        description: How long to poll for "merged/deleted" operation results.
        required: false
        default: 0
        type: int

author:
    - Krishna Vasudevan
'''

EXAMPLES = r'''
# Pass in a message
- name: Display global MLAG configuration
  nvidia.nvue.mlag:
    state: gathered
'''

RETURN = r'''
# These are examples of possible return values, and in general should use other names for return values.

'''

import json
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.connection import Connection
from ansible.module_utils.six import string_types
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.utils import (
    dict_diff,
)


def main():
    # define supported filters for the endpoint
    filter_spec = dict(
        rev=dict(type='str', required=False, default='operational'),
        omit=dict(type='list', required=False),
        include=dict(type='list', required=False)
    )

    # define the bridge spec - used for creation/modification
    mlag_spec = dict(
        enable=dict(type='str', required=False, default='off', choices=['on', 'off']),
        backup=dict(type='list', required=False, options=dict(
            id=dict(type='str', required=False),
            vrf=dict(type="str", required=False)
        )),
        init_delay=dict(type='int', required=False),
        peer_ip=dict(type='str', required=False),
        mac_address=dict(type='str', required=False),
        priority=dict(type='int', required=False)
    )

    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        force=dict(type='bool', required=False, default=False),
        wait=dict(type="int", required=False, default=0),
        state=dict(type='str', required=True, choices=['gathered', 'deleted', 'merged']),
        revid=dict(type='str', required=False),
        data=dict(type='dict', required=False, options=mlag_spec),
        filters=dict(type='dict', required=False, options=filter_spec)
    )

    required_if = [
        ["operation", "merged", ["data"]],
    ]
    # the AnsibleModule object will be our abstraction working with Ansible
    # this includes instantiation, a couple of common attr would be the
    # args/params passed to the execution, as well as if the module
    # supports check mode
    module = AnsibleModule(
        argument_spec=module_args,
        required_if=required_if,
        supports_check_mode=True
    )

    path = "mlag/"
    if module.params["state"] == "gathered":
        operation = "get"
    else:
        operation = "set"
    data = module.params["data"]
    force = module.params["force"]
    wait = module.params["wait"]
    revid = module.params["revid"]

    if isinstance(data, string_types):
        data = json.loads(data)

    warnings = list()
    result = {"changed": False, "warnings": warnings}

    running = None
    commit = not module.check_mode

    # if the user is working with this module in only check mode we do not
    # want to make any changes to the environment, just return the current
    # state with no modifications
    if module.check_mode:
        module.exit_json(**result)

    connection = Connection(module._socket_path)
    response = connection.send_request(data, path, operation, force=force, wait=wait, revid=revid)
    if operation == "set" and response:
        result["changed"] = True
    result["message"] = response

    module.exit_json(**result)


if __name__ == '__main__':
    main()
