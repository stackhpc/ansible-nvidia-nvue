#!/usr/bin/python

# Copyright: (c) 2022 NVIDIA
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = r'''
---
module: service

short_description: This is the Cumulus Linux service module

version_added: "1.0.0"

description: This is a Cumulus Linux module to interact with the services object.

options:
    filters:
        description: Filters used while fetching information about services
        type: dict
        suboptions:
            rev:
                description: The default is to query the operational state. However, this parameter can be used to query desired state on configuration
                             branches, such as startup and applied. This could be a branch name, tag name or specific commit.
                required: false
                type: str
                default: applied
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
            dhcp_relay:
                description: Config of DHCP relay service.
                required: false
                type: list
                elements: dict
                suboptions:
                    id:
                        description: DHCP-relay.
                        required: false
                        type: str
                    interface:
                        description: Set of interfaces on which to handle DHCP relay traffic.
                        required: false
                        type: list
                        elements: dict
                        suboptions:
                            id:
                                description: An interface on which DHCP relay is configured.
                                required: false
                                type: str
                    server:
                        description: DHCP servers.
                        required: false
                        type: list
                        elements: dict
                        suboptions:
                            id:
                                description: A dhcp server.
                                required: false
                                type: str
                    source_ip:
                        description: Source IP to use on the relayed packet. If "giaddr", it will be taken from giaddress. 
                        Otherwise, if "auto", it will be taken from an L3 interface on this switch using normal routing methods. 
                        This is the default.
                        required: false
                        type: str
                        default: auto
                    gateway_interface:
                        description: Configures DHCP relay gateway on the interfaes.
                        required: false
                        type: list
                        elements: dict
                        suboptions:
                            id:
                                description: An interface on which DHCP relay gateway is configured.
                                required: false
                                type: str
                            address:
                                description: ipv4 address on gateway interface.
                                required: false
                                type: str
                                default: auto
            dns:
                description: Collection of DNS.
                required: false
                type: list
                elements: dict
                suboptions:
                    id:
                        description: VRF name.
                        required: false
                        type: str
                    server:
                        description: Remote DNS servers.
                        required: false
                        type: list
                        elements: dict
                        suboptions:
                            id:
                                description: Remote DNS Server.
                                required: false
                                type: str
            ntp:
                description: Collection of NTPs.
                required: false
                type: list
                elements: dict
                suboptions:
                    id:
                        description: VRF name.
                        required: false
                        type: str
                    server:
                        description: Remote NTP servers.
                        required: false
                        type: list
                        elements: dict
                        suboptions:
                            id:
                                description: Remote NTP Server.
                                required: false
                                type: str
                            iburst:
                                description: When the server is unreachable, send a burst of eight packets instead of the usual one.
                                required: false
                                type: str
                                default: 'on'
                                choices:
                                    - 'on'
                                    - 'off'
            syslog:
                description: Collection of syslog.
                required: false
                type: list
                elements: dict
                suboptions:
                    id:
                        description: VRF name.
                        required: false
                        type: str
                    server:
                        description: Remote syslog servers.
                        required: false
                        type: list
                        elements: dict
                        suboptions:
                            id:
                                description: Remote syslog server.
                                required: false
                                type: str
                            port:
                                description: Port number of the remote syslog server.
                                required: false
                                type: int
                                default: 514
                            protocol:
                                description: Protocol, udp or tcp, of the remote syslog server.
                                required: false
                                type: str
                                default: udp
                                choices:
                                    - udp
                                    - tcp
            snmp_server:
                description: SNMP configuration
                required: false
                type: list
                elements: dict
                suboptions:
                    enable:
                        description: Turn the feature on or off. The feature is disabled by default.
                        required: false
                        type: str
                        choices:
                            - 'on'
                            - 'off'
                        default: 'off'
                    listening_address:
                        description: Collection of listening addresses.
                        required: false
                        type: list
                        elements: dict
                        suboptions:
                            id:
                                description: A listening address.
                                required: false
                                type: str
                            vrf:
                                description: The listening address VRF.
                                required: false
                                type: str
                    readonly_community:
                        description: Collection of readonly community string passwords for version 1 or 2c access for IPv4.
                        required: false
                        type: list
                        elements: dict
                        suboptions:
                            id:
                                description: A readonly community string password for version 1 or 2c access for IPv4.
                                required: false
                                type: str
                            access:
                                description: Assign addresses to readonly community string password.
                                required: false
                                type: list
                                elements: dict
                                suboptions:
                                    id:
                                        description: An address for readonly community string password.
                                        required: false
                                        type: str
                                    oid:
                                        description: An object identifier (OID) that represents a managed object in the MIB hierarchy.
                                        required: false
                                        type: str
                                    view:
                                        description: A name of a view that restricts MIB tree exposure.
                                        required: false
                                        type: str
                    system_contact:
                        description: SNMP server system contact info.
                        type: str
                        required: false
                    system_location:
                        description: SNMP server system location info.
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
    - Alexander Dibbo (UKRI - STFC) (@apdibbo)
'''

EXAMPLES = r'''
# Pass in a message
- name: Display all the services in the environment
  nvidia.nvue.service:
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
    # since router object doesn't support querying the operational state, we will default to applied state
    filter_spec = dict(
        rev=dict(type='str', required=False, default='applied'),
        omit=dict(type='list', required=False, elements='str'),
        include=dict(type='list', required=False, elements='str')
    )

    # define the service spec - used for creation/modification
    service_spec = dict(
        dhcp_relay=dict(type='list', required=False, elements='dict', options=dict(
            id=dict(type='str', required=False),
            interface=dict(type='list', required=False, elements='dict', options=dict(
                id=dict(type='str', required=False)
            )),
            server=dict(type='list', required=False, elements='dict', options=dict(
                id=dict(type='str', required=False)
            )),
            source_ip=dict(type='str', required=False, default='auto'),
            gateway_interface=dict(type='list', required=False, elements='dict', options=dict(
                id=dict(type='str', required=False),
                address=dict(type='str', required=False, default='auto')
            )))
        ),
        dns=dict(type='list', required=False, elements='dict', options=dict(
            id=dict(type='str', required=False),
            server=dict(type='list', required=False, elements='dict', options=dict(
                id=dict(type='str', required=False)
            ))
        )),
        ntp=dict(type='list', required=False, elements='dict', options=dict(
            id=dict(type='str', required=False),
            server=dict(type='list', required=False, elements='dict', options=dict(
                id=dict(type='str', required=False),
                iburst=dict(type='str', required=False, default='on', choices=['on', 'off'])
            ))
        )),
        syslog=dict(type='list', required=False, elements='dict', options=dict(
            id=dict(type='str', required=False),
            server=dict(type='list', required=False, elements='dict', options=dict(
                id=dict(type='str', required=False),
                port=dict(type='int', required=False, default='514'),
                protocol=dict(type='str', required=False, default='udp', choices=['udp', 'tcp'])
            ))
        )),
        snmp_server=dict(type='list', required=False, elements='dict', options=dict(
            enable=dict(type='str', required=False, default='off', choices=['on', 'off']),
            listening_address=dict(type='list', required=False, elements='dict', options=dict(
                id=dict(type='str', required=False),
                vrf=dict(type='str', required=False)
            )),
            readonly_community=dict(type='list', required=False, elements='dict', options=dict(
                id=dict(type='str', required=False),
                access=dict(type='list', required=False, elements='dict', options=dict(
                    id=dict(type='str', required=False),
                    oid=dict(type='str', required=False),
                    view=dict(type='str', required=False)
                ))
            )
            ),
            system_contact=dict(type='str', required=False),
            system_location=dict(type='str', required=False)
        ))
    )

    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        force=dict(type='bool', required=False, default=False),
        wait=dict(type="int", required=False, default=0),
        state=dict(type='str', required=True, choices=["gathered", "deleted", "merged"]),
        revid=dict(type='str', required=False),
        data=dict(type='dict', required=False, options=service_spec),
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

    path = "service"
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
