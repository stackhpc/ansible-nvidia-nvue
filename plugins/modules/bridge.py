#!/usr/bin/python

# Copyright: (c) 2022 NVIDIA
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = r'''
---
module: bridge

short_description: This is the Cumulus Linux bridge module

version_added: "1.0.0"

description: This is a Cumulus Linux module to interact with the bridges object and the properties associated with an instance of a bridge.

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
        type: list
        elements: dict
        suboptions:
            id:
                description: Bridge domain.
                required: true
                type: str
            untagged:
                description: Interfaces added to this domain will, by default, be trunk interfaces with a single untagged vlan.
                             Untagged packets on domain ports will be put in this vlan. If none, then untagged packets will be dropped.
                required: false
                type: int
            encap:
                description: Interfaces added to this domain will, by default, use this encapsulation.
                default: 802.1Q
                required: false
                type: str
            mac_address:
                description: Override global mac address.
                default: auto
                required: false
                type: str
            type:
                description: Type of bridge domain.
                default: vlan-aware
                required: false
                type: str
            vlan:
                description: Set of vlans in the bridge domain. Only applicable when the domain type is "vlan-aware".
                required: false
                type: list
                elements: dict
                suboptions:
                    id:
                        description: A VLAN tag identifier
                        required: false
                        type: str
                    vni:
                        description: L2 VNI
                        required: false
                        type: list
                        elements: dict
                        suboptions:
                            id:
                                description: VNI
                                required: false
                                type: str
                            flooding:
                                description: Handling of BUM traffic
                                required: false
                                type: dict
                                suboptions:
                                    enable:
                                        description: Turn the feature 'on' or 'off' or 'auto'.
                                        required: false
                                        type: str
                                        default: auto
                                        choices:
                                            - 'on'
                                            - 'off'
                                            - auto
                                    multicast_group:
                                        description: BUM traffic is sent to the specified multicast group and will be received by receivers
                                                     who are interested in that group. This usually requires PIM-SM to be used in the network.
                                        type: str
                                        required: false
                                    head_end_replication:
                                        description: BUM traffic is replicated and individual copies sent to remote destinations.
                                        required: false
                                        type: list
                                        elements: dict
                                        suboptions:
                                            id:
                                                description: An IPv4 address.
                                                required: false
                                                type: str

    domainid:
        description: Name of the domain to fetch/delete.
        type: str
        required: false

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
- name: Display all the bridge domains in the environment
  nvidia.nvue.bridge:
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
        omit=dict(type='list', elements='str', required=False),
        include=dict(type='list', elements='str', required=False)
    )

    # define the bridge spec - used for creation/modification
    bridge_spec = dict(
        id=dict(type='str', required=True),
        untagged=dict(type='int', required=False),
        type=dict(type='str', required=False, default="vlan-aware"),
        encap=dict(type='str', required=False, default="802.1Q"),
        mac_address=dict(type='str', required=False, default="auto"),
        vlan=dict(type='list', required=False, elements='dict', options=dict(
            id=dict(type='str', required=False),
            vni=dict(type='list', required=False, elements='dict', options=dict(
                id=dict(type='str', required=False),
                flooding=dict(type='dict', required=False, options=dict(
                    enable=dict(type='str', required=False, choices=['on', 'off', 'auto'], default='auto'),
                    multicast_group=dict(type='str', required=False),
                    head_end_replication=dict(type='list', required=False, elements='dict', options=dict(
                        id=dict(type='str', required=False)
                    ))
                ))
            ))
        ))
    )

    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        force=dict(type='bool', required=False, default=False),
        wait=dict(type="int", required=False, default=0),
        state=dict(type='str', required=True, choices=["gathered", "deleted", "merged"]),
        revid=dict(type='str', required=False),
        domainid=dict(type='str', required=False),
        data=dict(type='list', required=False, elements='dict', options=bridge_spec),
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
        mutually_exclusive=[["data", "domainid"]],
        required_if=required_if,
        supports_check_mode=True
    )

    path = "bridge"
    if module.params["domainid"] is not None:
        path = path + "/domain/" + module.params["domainid"]
    else:
        path = path + "/domain"
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
