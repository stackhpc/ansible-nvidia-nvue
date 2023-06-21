#!/usr/bin/python

# Copyright: (c) 2022 NVIDIA
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = r'''
---
module: evpn

short_description: This is the Cumulus Linux EVPN module

version_added: '1.0.0'

description: This is a Cumulus Linux module to interact with the EVPN object. Enables the EVPN control plane. When enabled,
             it also means that the EVPN service offered is vlan-based service and an EVI is auto-created for each extended VLAN.

options:
    filters:
        description: Filters used while fetching information about router
        type: dict
        suboptions:
            rev:
                description: The default is to query the operational state. However, this parameter can be used to query desired state on configuration
                             branches, such as startup and applied. This could be a branch name, tag name or specific commit.
                required: false
                type: str
                default: operational
            omit:
                description: Drop any JSON properties matched by an omit pattern from the response.
                required: false
                type: list
                elements: str
            include:
                description: Only include JSON properties matched by an include pattern in the response.
                required: false
                type: list
                elements: str
    data:
        description: Provided configuration
        type: dict
        suboptions:
            enable:
                description: Turn the feature 'on' or 'off'.
                required: false
                type: str
                default: 'off'
                choices:
                    - 'on'
                    - 'off'
            dad:
                description: Advertise
                required: false
                type: dict
                suboptions:
                    enable:
                        description: Turn the feature 'on' or 'off'.
                        required: false
                        type: str
                        default: 'off'
                        choices:
                            - 'on'
                            - 'off'
            multihoming:
                description: Multihoming global configuration parameters
                required: false
                type: dict
                suboptions:
                    enable:
                        description: Turn the feature 'on' or 'off'.
                        required: false
                        type: str
                        default: 'off'
                        choices:
                            - 'on'
                            - 'off'
                    startup_delay:
                        description: The duration for which a switch holds the Ethernet segment-bond in a protodown state after a reboot or process restart.
                        required: false
                        type: int
                        default: 180
            route_advertise:
                description: Route advertising
                required: false
                type: dict
                suboptions:
                    nexthop_setting:
                        description: Specifies the next hop IP and MAC (Router MAC) to use in the advertisement of type-5 routes and 'self' type-2
                                     routes ('self' = SVI IP/MAC). Relevant only in an MLAG configuration.
                        required: false
                        type: str
                        default: system-ip-mac
                        choices:
                            - system-ip-mac
                            - shared-ip-mac
                    svi_ip:
                        description: If 'on', the IP addresses of SVIs in all EVIs are announced as type-2 routes.
                                     This configuration should not be enabled if SVI IPs are reused in the network.
                        required: false
                        type: str
                        default: 'off'
                        choices:
                            - 'on'
                            - 'off'
                    default_gateway:
                        description: This configuration should be turned 'on' only in a centralized-routing deployment and only on the centralized GW router(s).
                                     If 'on', the IP addresses of SVIs in all EVIs are announced as type-2 routes with the gateway extended community.
                                     The purpose is for remote L2-only VTEPs to do ARP suppression and for hosts to learn of the gateway's IP to MAC binding.
                        required: false
                        type: str
                        default: 'off'
                        choices:
                            - 'on'
                            - 'off'

    revid:
        description: Revision ID to query/to apply config to.
        required: false
        type: str
    state:
        description: Defines the action to be taken.
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
    - Nvidia NBU Team (@nvidia-nbu)
    - Krishna Vasudevan (@krisvasudevan)
'''

EXAMPLES = r'''
# Pass in a message
- name: Display global EVPN configuration
  nvidia.nvue.evpn:
    state: gathered
'''

RETURN = r'''
# These are examples of possible return values, and in general should use other names for return values.

'''

import json
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.connection import Connection
from ansible.module_utils.six import string_types


def main():
    # define supported filters for the endpoint
    filter_spec = dict(
        rev=dict(type='str', required=False, default='operational'),
        omit=dict(type='list', required=False, elements='str'),
        include=dict(type='list', required=False, elements='str')
    )

    # define the bridge spec - used for creation/modification
    evpn_spec = dict(
        enable=dict(type='str', required=False, default='off', choices=['on', 'off']),
        dad=dict(type='dict', required=False, options=dict(
            enable=dict(type='str', required=False, default='off', choices=['on', 'off'])
        )),
        multihoming=dict(type='dict', required=False, options=dict(
            enable=dict(type='str', required=False, default='off', choices=['on', 'off']),
            startup_delay=dict(type='int', required=False, default=180)
        )),
        route_advertise=dict(type='dict', required=False, options=dict(
            nexthop_setting=dict(type='str', required=False, default='system-ip-mac', choices=['system-ip-mac', 'shared-ip-mac']),
            svi_ip=dict(type='str', required=False, default='off', choices=['on', 'off']),
            default_gateway=dict(type='str', required=False, default='off', choices=['on', 'off'])
        ))
    )

    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        force=dict(type='bool', required=False, default=False),
        wait=dict(type="int", required=False, default=0),
        state=dict(type='str', required=True, choices=['gathered', 'deleted', 'merged']),
        revid=dict(type='str', required=False),
        data=dict(type='dict', required=False, options=evpn_spec),
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

    path = "evpn"
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
