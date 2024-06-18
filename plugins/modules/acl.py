#!/usr/bin/python

# Copyright: (c) 2022 NVIDIA
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = r'''
---
module: acl

short_description: This is the Cumulus Linux ACL rules module

version_added: "1.1.0"

description: This is a Cumulus Linux module to interact with the ACL rules object and the properties associated with an instance of an ACL rule.

options:
    filters:
        description: Filters used while fetching information about ACL rules.
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
                description: An ACL is used for matching packets and take actions.
                required: true
                type: str
            type:
                description: ACL type.
                required: false
                type: str
                choices:
                    - 'ipv4'
                    - 'ipv6'
                    - 'mac'
            rule:
                description: ACL rule.
                required: false
                type: list
                elements: dict
                suboptions:
                    id:
                        description: ACL Matching criteria and action rule.
                        required: false
                        type: str
                    remark:
                        description: Rule remarks.
                        required: false
                        type: str
                    match:
                        description: ACL match criteria.
                        required: false
                        type: dict
                        suboptions:
                            ip:
                                description: IPv4 and IPv6 match.
                                required: false
                                type: dict
                                suboptions:
                                    source_ip:
                                        description: Source IP Address.
                                        required: false
                                        type: str
                                    dest_ip:
                                        description: Destination IP Address.
                                        required: false
                                        type: str
                                    protocol:
                                        description: IP protocol.
                                        required: false
                                        type: str
                                    dscp:
                                        description: DSCP.
                                        required: false
                                        type: str
                                    icmp_type:
                                        description: ICMP message type.
                                        required: false
                                        type: str
                                    icmpv6_type:
                                        description: ICMPv6 message type.
                                        required: false
                                        type: str
                                    ttl:
                                        description: ttl in ipv4 and hl in ipv6.
                                        required: false
                                        type: int
                                    tcp:
                                        description: TCP protocol packet match.
                                        required: false
                                        type: dict
                                        suboptions:
                                            dest_port:
                                                description: Destination port.
                                                required: false
                                                type: list
                                                elements: dict
                                                suboptions:
                                                    id:
                                                        description: L4 port.
                                                        required: false
                                                        type: str
                                            source_port:
                                                description: Source port.
                                                required: false
                                                type: list
                                                elements: dict
                                                suboptions:
                                                    id:
                                                        description: L4 port.
                                                        required: false
                                                        type: str
                                    udp:
                                        description: UDP protocol packet match.
                                        required: false
                                        type: dict
                                        suboptions:
                                            dest_port:
                                                description: Destination port.
                                                required: false
                                                type: list
                                                elements: dict
                                                suboptions:
                                                    id:
                                                        description: L4 port.
                                                        required: false
                                                        type: str
                                            source_port:
                                                description: Source port.
                                                required: false
                                                type: list
                                                elements: dict
                                                suboptions:
                                                    id:
                                                        description: L4 port.
                                                        required: false
                                                        type: str
                            mac:
                                description: MAC match.
                                required: false
                                type: dict
                                suboptions:
                                    source_mac:
                                        description: Source MAC Address.
                                        required: false
                                        type: str
                                    dest_mac:
                                        description: Destination MAC Address.
                                        required: false
                                        type: str
                                    source_mac_mask:
                                        description: Source MAC Address mask.
                                        required: false
                                        type: str
                                    dest_mac_mask:
                                        description: Destination MAC Address mask.
                                        required: false
                                        type: str
                                    protocol:
                                        description: MAC protocol.
                                        required: false
                                        type: str
                            vlan:
                                description: VLAN ID.
                                required: false
                                type: int
                    action:
                        description: ACL action
                        required: false
                        type: dict
                        suboptions:
                            deny:
                                description: Deny action.
                                required: false
                                type: dict
                            permit:
                                description: Permit action.
                                required: false
                                type: dict
                            log:
                                description: Provides ACL logging facility.
                                required: false
                                type: dict
                                suboptions:
                                    log_prefix:
                                        description: Log the matching packets with prefix.
                                        required: false
                                        type: str
    revid:
        description: Revision ID to query/to apply config to.
        required: false
        type: str
    aclid:
        description: Specific ACL to query/modify.
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
- name: Display all the ACLs in the environment
  nvidia.nvue.acl:
    state: gathered

- name: Add ACL
  nvidia.nvue.acl:
    state: merged
    force: yes
    wait: 15
    data:
        - id: 'acl1'
          rule:
            - id: '475'
              action:
                permit:
              match:
                ip:
                  dest_ip: '10.115.28.0/32'
                  dest_port:
                    - id: 'ANY'
                  source_ip: '10.110.0.11/32'
                  source_port:
                    - id: 'smtp'
                  protocol: 'tcp'
          type: 'ipv4'
    '''

RETURN = r'''
# These are examples of possible return values, and in general should use other names for return values.
changed:
  description: whether a configuration was changed
  returned: always
  type: bool
  sample: true
message:
    description: details of the ACL (for gathered) or whether the change was applied (for merged)
    type: dict
    returned: always
    sample:
     - "acl1": {
                "rule": {
                    "475": {
                        "action": {},
                        "match": {
                            "ip": {
                                "dest-ip": "10.115.28.0/32",
                                "dest-port": {
                                    "ANY": {}
                                },
                                "protocol": "tcp",
                                "source-ip": "10.110.0.11/32",
                                "source-port": {
                                    "smtp": {}
                                }
                            }
                        }
                    }
                },
                "type": "ipv4"
            }
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

    # define the acl spec - used for creation/modification
    acl_spec = dict(
        id=dict(type='str', required=True),
        type=dict(type='str', required=False, choices=['ipv4', 'ipv6', 'mac']),
        rule=dict(type='list', required=False, elements='dict', options=dict(
            id=dict(type='str', required=False),
            remark=dict(type='str', required=False),
            match=dict(type='dict', required=False, options=dict(
                ip=dict(type='dict', required=False, options=dict(
                    source_ip=dict(type='str', required=False),
                    dest_ip=dict(type='str', required=False),
                    protocol=dict(type='str', required=False),
                    dscp=dict(type='str', required=False),
                    icmp_type=dict(type='str', required=False),
                    icmpv6_type=dict(type='str', required=False),
                    ttl=dict(type='int', required=False),
                    tcp=dict(type='dict', required=False, options=dict(
                        source_port=dict(type='list', required=False, elements='dict', options=dict(
                            id=dict(type='str', required=False)
                        )),
                        dest_port=dict(type='list', required=False, elements='dict', options=dict(
                            id=dict(type='str', required=False)
                        ))
                    )),
                    udp=dict(type='dict', required=False, options=dict(
                        source_port=dict(type='list', required=False, elements='dict', options=dict(
                            id=dict(type='str', required=False)
                        )),
                        dest_port=dict(type='list', required=False, elements='dict', options=dict(
                            id=dict(type='str', required=False)
                        ))
                    ))
                )),
                mac=dict(type='dict', required=False, options=dict(
                    source_mac=dict(type='str', required=False),
                    dest_mac=dict(type='str', required=False),
                    source_mac_mask=dict(type='str', required=False),
                    dest_mac_mask=dict(type='str', required=False),
                    protocol=dict(type='str', required=False)
                )),
                vlan=dict(type='int', required=False)
            )),
            action=dict(type='dict', required=False, options=dict(
                deny=dict(type='dict', required=False, options=dict(
                )),
                permit=dict(type='dict', required=False, options=dict(
                )),
                log=dict(type='dict', required=False, options=dict(
                    log_prefix=dict(type='str', required=False)
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
        aclid=dict(type='str', required=False),
        data=dict(type='list', required=False, elements='dict', options=acl_spec),
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

    path = "acl"
    if module.params["aclid"] is not None:
        path = path + "/" + module.params["aclid"]
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
