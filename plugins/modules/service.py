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
                                default: on
                                choices:
                                    - on
                                    - off
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
- name: Display all the services in the environment
  nvidia.nvue.service:
    state: gathered
'''

RETURN = r'''
# These are examples of possible return values, and in general should use other names for return values.

'''

import json
import q
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.connection import Connection
from ansible.module_utils.six import string_types
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.utils import (
    dict_diff,
)


def main():
    # define supported filters for the endpoint
    # since router object doesn't support querying the operational state, we will default to applied state
    filter_spec = dict(
        rev=dict(type='str', required=False, default='applied'),
        omit=dict(type='list', required=False),
        include=dict(type='list', required=False)
    )

    # define the service spec - used for creation/modification
    service_spec = dict(
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
                port=dict(type='str', required=False, default='514'),
                protocol=dict(type='str', required=False, default='udp', choices=['udp', 'tcp'])
            ))
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
    q(path)
    response = connection.send_request(data, path, operation, force=force, wait=wait, revid=revid)
    if operation == "set" and response:
        result["changed"] = True
    result["message"] = response

    module.exit_json(**result)


if __name__ == '__main__':
    main()
