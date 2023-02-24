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
        description: Filters used while fetching information about bridges
        type: dict
        elements: dict
        suboptions:
            rev:
                description: The default is to query the operational state. However, this parameter can be used to query desired state on configuration branches, such as startup and applied. This could be a branch name, tag name or specific commit.
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
    config:
        description: Provided configuration
        type: list 
        elements: dict
        suboptions:
            id:
                description: Bridge domain.
                required: true
                type: str
            untagged:
                description: Interfaces added to this domain will, by default, be trunk interfaces with a single untagged vlan. Untagged packets on domain ports will be put in this vlan. If none, then untagged packets will be dropped.
                required: false
                type: int
            encap:
                description: Interfaces added to this domain will, by default, use this encapsulation.
                default: 802.1Q
                required: false
                type: str
            encap:
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
                                elements: dict
                                suboptions:
                                    enable:
                                        description: Turn the feature 'on' or 'off' or 'auto'.
                                        required: false
                                        type: str
                                        default: auto
                                        choices:
                                            - on
                                            - off
                                            - auto
                                    multicast_group:
                                        description: BUM traffic is sent to the specified multicast group and will be received by receivers who are interested in that group. This usually requires PIM-SM to be used in the network.
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
        description: Name of the domain to fetch/delete
        type: str
        required: false


    state: 
        description: Defines the action to be taken
        required:true
        type: string
        choices: 
            - gathered
            - deleted
            - merged

author:
    - Krishna Vasudevan
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

from ansible.module_utils.basic import AnsibleModule
from ..module_utils.cl_common import run

def main():
    # define paremeters to connect to the CL instance
    provider_spec = dict(
        cl_url=dict(type='str', required=True),
        cl_port=dict(type='str', required=True),
        cl_username = dict(type='str', required=True),
        cl_password = dict(type='str', required=True, no_log=True)
    )

    # define supported filters for the endpoint
    filter_spec = dict(
        rev=dict(type='str', required=False, default='operational'),
        omit=dict(type='list', required=False),
        include=dict(type='list', required=False)
    )
    
    # define the bridge spec - used for creation/modification
    bridge_spec = dict(
        id=dict(type='str', required=True),
        untagged=dict(type='int',required=False),
        type=dict(type='str',required=False, default="vlan-aware"),
        encap=dict(type='str',required=False, default="802.1Q"),
        mac_address=dict(type='str',required=False),
        vlan=dict(type='list',required=False,options=dict(
            id=dict(type='str',required=False),
            vni=dict(type='list',required=False,options=dict(
                id=dict(type='str',required=False)),
                flooding=dict(type='dict',required=False,options=dict(
                    enable=dict(type='str', required=False, default='auto',choices=['on','off','auto']),
                    multicast_group=dict(type='str',required=False),
                    head_end_replication=dict(type='list',required=False,options=dict(
                        id=dict(type='str',required=False)
                    ))
                ))
            )
        ))
    )

    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        provider=dict(type='dict', required=True, options=provider_spec),
        state=dict(type='str', required=True,choices=["gathered","deleted","merged"]),
        revid=dict(type='str', required=False),
        domainid=dict(type='str', required=False),
        config=dict(type='list',required=False,elements='dict',options=bridge_spec),
        filters=dict(type='dict', required=False, options=filter_spec)
    )

    # the AnsibleModule object will be our abstraction working with Ansible
    # this includes instantiation, a couple of common attr would be the
    # args/params passed to the execution, as well as if the module
    # supports check mode
    module = AnsibleModule(
        argument_spec=module_args,
        mutually_exclusive=[["config", "domainid"]],
        supports_check_mode=True
    )

    # if the user is working with this module in only check mode we do not
    # want to make any changes to the environment, just return the current
    # state with no modifications
    if module.check_mode:
        module.exit_json(**result)

    endpoint = "bridge"
    if(module.params["state"] == "gathered"):
        if module.params["domainid"] is not None:
            endpoint = endpoint + "/domain/" + module.params["domainid"]
    elif(module.params["state"] == "deleted"):
        if module.params["domainid"] is not None:
            endpoint = endpoint + "/domain/" + module.params["domainid"]
    else:
        endpoint = endpoint + "/domain"

    result = run(endpoint,module.params)

    # during the execution of the module, if there is an exception or a
    # conditional state that effectively causes a failure, run
    # AnsibleModule.fail_json() to pass in the message and the result
    if result["status_code"] != 200:
        module.fail_json(msg='Your request failed',**result)

    # in the event of a successful module execution, you will want to
    # simple AnsibleModule.exit_json(), passing the key/value results
    module.exit_json(**result)


if __name__ == '__main__':
    main()