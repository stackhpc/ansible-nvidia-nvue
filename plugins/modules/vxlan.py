#!/usr/bin/python

# Copyright: (c) 2022 NVIDIA
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
import json
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.connection import Connection
from ansible.module_utils.six import string_types

__metaclass__ = type

DOCUMENTATION = r'''
---
module: vxlan

short_description: This is the Cumulus Linux VxLAN module

version_added: '1.0.0'

description: This is a Cumulus Linux module to interact with global VxLAN configuration and operational properties.

options:
    filters:
        description: Filters used while fetching information about VxLAN
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
            mac_learning:
                description: Controls dynamic MAC learning over VXLAN tunnels based on received packets. This applies to all overlays (VNIs),
                             but can be overridden by VNI-specific configuration.
                required: false
                type: str
                default: off
                choices:
                    - on
                    - off
            arp_nd_suppress:
                description: Controls dynamic MAC learning over VXLAN tunnels based on received packets. This applies to all overlays (VNIs).
                required: false
                type: str
                default: on
                choices:
                    - on
                    - off
            source:
                description: Source address.
                type: dict
                elements: dict
                suboptions:
                    address:
                        description: IP addresses of this node's VTEP or 'auto'. If 'auto', use the primary IP loopback (not 127.0.0.1).
                                     This is the default.
                        required: false
                        type: str
                        default: auto
            mlag:
                description: VxLAN specific MLAG address.
                type: dict
                elements: dict
                suboptions:
                    shared_address:
                        description: Shared anycast address for MLAG peers.
                        required: false
                        type: str
                        default: none


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
- name: Display VxLAN configuration
  nvidia.nvue.vxlan:
    state: gathered
'''

RETURN = r'''
# These are examples of possible return values, and in general should use other names for return values.

'''


def main():
    # define supported filters for the endpoint
    filter_spec = dict(
        rev=dict(type='str', required=False, default='operational'),
        omit=dict(type='list', required=False),
        include=dict(type='list', required=False)
    )

    # define the bridge spec - used for creation/modification
    vxlan_spec = dict(
        enable=dict(type='str', required=False, default='off', choices=['on', 'off']),
        mac_learning=dict(type='str', required=False, default='off', choices=['on', 'off']),
        arp_nd_suppress=dict(type='str', required=False, default='on', choices=['on', 'off']),
        source=dict(type='dict', required=False, options=dict(
            address=dict(type="str", required=False, default="auto")
        )),
        mlag=dict(type='dict', required=False, options=dict(
            shared_address=dict(type="str", required=False, default="none")
        ))
    )

    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        force=dict(type='bool', required=False, default=False),
        wait=dict(type="int", required=False, default=0),
        state=dict(type='str', required=True, choices=['gathered', 'deleted', 'merged']),
        revid=dict(type='str', required=False),
        data=dict(type='dict', required=False, options=vxlan_spec),
        filters=dict(type='dict', required=False, options=filter_spec)
    )

    required_if = [
        ["state", "merged", ["data"]],
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

    path = "nve/vxlan"
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