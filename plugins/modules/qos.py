#!/usr/bin/python

# Copyright: (c) 2022 NVIDIA
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = r'''
---
module: qos

short_description: This is the Cumulus Linux QoS module

version_added: '1.2.0'

description: This is a Cumulus Linux module to interact with QoS configuration and operational properties.

options:
    filters:
        description: Filters used while fetching information about QoS
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
            roce:
                description: Properties associated with the RDMA over Converged Ethernet (RoCE) feature.
                type: dict
                suboptions:
                    enable:
                        description: Turn the feature 'on' or 'off'.
                        required: false
                        type: str
                        choices:
                            - 'on'
                            - 'off'
                    mode:
                        description: ROCE mode
                        required: false
                        type: str
                        choices:
                            - 'lossy'
                            - 'lossless'
            pfc_watchdog:
                description: Properties associated with PFC Watchdog Feature.
                type: dict
                suboptions:
                    polling_interval:
                        description: polling cycle(in msec) for pause storm detection and mitigation.
                        required: false
                        type: int
                    robustness:
                        description: number of consecutive polling-iterval to detect pause storm before taking
                                     action to mitigate pause storm.
                        required: false
                        type: int
            pfc:
                description: Collection of Priority Flow Control Profiles.
                required: false
                type: list
                elements: dict
                suboptions:
                    id:
                        description: Properties associated with the Priority Flow Control Feature.
                        required: false
                        type: str
                    xoff_threshold:
                        description: XOff threshold (in bytes).
                        required: false
                        type: int
                    xon_threshold:
                        description: XOn threshold (in bytes).
                        required: false
                        type: int
                    port_buffer:
                        description: Port Buffer (in bytes).
                        required: false
                        type: int
                    cable_length:
                        description: Cable Length (in meters).
                        required: false
                        type: int
                    tx:
                        description: PFC Tx State.
                        required: false
                        type: str
                        choices:
                            - 'enable'
                            - 'disable'
                    rx:
                        description: PFC Rx State.
                        required: false
                        type: str
                        choices:
                            - 'enable'
                            - 'disable'
                    switch_priority:
                        description: Collection of switch priorities.
                        required: false
                        type: list
                        elements: dict
                        suboptions:
                            id:
                                description: Internal switch priority config.
                                required: false
                                type: str
            link_pause:
                description: Collection of Link Pause Profiles.
                required: false
                type: list
                elements: dict
                suboptions:
                    id:
                        description: Properties associated with the Link Pause Feature.
                        required: false
                        type: str
                    xoff_threshold:
                        description: XOff threshold (in bytes).
                        required: false
                        type: int
                    xon_threshold:
                        description: XOn threshold (in bytes).
                        required: false
                        type: int
                    port_buffer:
                        description: Port Buffer (in bytes).
                        required: false
                        type: int
                    cable_length:
                        description: Cable Length (in meters).
                        required: false
                        type: int
                    tx:
                        description: PFC Tx State.
                        required: false
                        type: str
                        choices:
                            - 'enable'
                            - 'disable'
                    rx:
                        description: PFC Rx State.
                        required: false
                        type: str
                        choices:
                            - 'enable'
                            - 'disable'
            traffic_pool:
                description: Collection of Traffic Pool Profiles.
                type: list
                elements: dict
                suboptions:
                    id:
                        description: Properties associated with the QoS Traffic Pools.
                        required: false
                        type: str
                    memory_percent:
                        description: Traffic Pool Memory Percent.
                        required: false
                        type: int
                    switch_priority:
                        description: Collection of switch priorities.
                        required: false
                        type: list
                        elements: dict
                        suboptions:
                            id:
                                description: Internal switch priority config.
                                required: false
                                type: str
            egress_queue_mapping:
                description: Collection of Egress Queue SP->TC mapping Profiles.
                type: list
                elements: dict
                suboptions:
                    id:
                        description: Properties associated with egress queue mapping feature.
                        required: false
                        type: str
                    switch_priority:
                        description: SP->TC mapping configurations.
                        required: false
                        type: list
                        elements: dict
                        suboptions:
                            id:
                                description: Egress traffic-class mapped to internal switch-priority.
                                required: false
                                type: str
                            traffic_class:
                                description: Traffic Class.
                                required: false
                                type: int
            mapping:
                description: Collection of PCP/DSCP->SP mapping Profiles.
                type: list
                elements: dict
                suboptions:
                    id:
                        description: Properties associated with PCP/DSCP->SP mapping feature.
                        required: false
                        type: str
                    port_default_sp:
                        description: Port Default Switch Priority.
                        required: false
                        type: int
                    trust:
                        description: Port Trust configuration.
                        required: false
                        type: str
                        choices:
                            - 'l2'
                            - 'l3'
                            - 'port'
                            - 'both'
                    pcp:
                        description: PCP->SP mapping configurations.
                        required: false
                        type: list
                        elements: dict
                        suboptions:
                            id:
                                description: PCP->SP mapping configuration.
                                required: false
                                type: str
                            switch_priority:
                                description: Internal Switch Priority.
                                required: false
                                type: int
                    dscp:
                        description: DSCP->SP mapping configurations.
                        required: false
                        type: list
                        elements: dict
                        suboptions:
                            id:
                                description: DSCP->SP mapping configuration.
                                required: false
                                type: str
                            switch_priority:
                                description: Internal Switch Priority.
                                required: false
                                type: int
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
- name: Display QoS configuration
  nvidia.nvue.qos:
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

    # define the QoS spec - used for creation/modification
    qos_spec = dict(
        roce=dict(type='dict', required=False, options=dict(
            enable=dict(type='str', required=False, choices=['on', 'off']),
            mode=dict(type='str', required=False, choices=['lossy', 'lossless'])
        )),
        pfc_watchdog=dict(type='dict', required=False, options=dict(
            polling_interval=dict(type='int', required=False),
            robustness=dict(type='int', required=False)
        )),
        pfc=dict(type='list', required=False, elements='dict', options=dict(
            id=dict(type='str', required=False),
            xoff_threshold=dict(type='int', required=False),
            xon_threshold=dict(type='int', required=False),
            port_buffer=dict(type='int', required=False),
            cable_length=dict(type='int', required=False),
            tx=dict(type='str', required=False, choices=['enable', 'disable']),
            rx=dict(type='str', required=False, choices=['enable', 'disable']),
            switch_priority=dict(type='list', required=False, elements='dict', options=dict(
                id=dict(type='str', required=False)
            ))
        )),
        link_pause=dict(type='list', required=False, elements='dict', options=dict(
            id=dict(type='str', required=False),
            xoff_threshold=dict(type='int', required=False),
            xon_threshold=dict(type='int', required=False),
            port_buffer=dict(type='int', required=False),
            cable_length=dict(type='int', required=False),
            tx=dict(type='str', required=False, choices=['enable', 'disable']),
            rx=dict(type='str', required=False, choices=['enable', 'disable'])
        )),
        traffic_pool=dict(type='list', required=False, elements='dict', options=dict(
            id=dict(type='str', required=False),
            memory_percent=dict(type='int', required=False),
            switch_priority=dict(type='list', required=False, elements='dict', options=dict(
                id=dict(type='str', required=False)
            ))
        )),
        egress_queue_mapping=dict(type='list', required=False, elements='dict', options=dict(
            id=dict(type='str', required=False),
            switch_priority=dict(type='list', required=False, elements='dict', options=dict(
                id=dict(type='str', required=False),
                traffic_class=dict(type='int', required=False),
            ))
        )),
        mapping=dict(type='list', required=False, elements='dict', options=dict(
            id=dict(type='str', required=False),
            port_default_sp=dict(type='int', required=False),
            trust=dict(type='str', required=False, choices=['l2', 'l3', 'port', 'both']),
            pcp=dict(type='list', required=False, elements='dict', options=dict(
                id=dict(type='str', required=False),
                switch_priority=dict(type='int', required=False)
            )),
            dscp=dict(type='list', required=False, elements='dict', options=dict(
                id=dict(type='str', required=False),
                switch_priority=dict(type='int', required=False)
            ))
        ))
    )

    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        force=dict(type='bool', required=False, default=False),
        wait=dict(type="int", required=False, default=0),
        state=dict(type='str', required=True, choices=['gathered', 'deleted', 'merged']),
        revid=dict(type='str', required=False),
        data=dict(type='dict', required=False, options=qos_spec),
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

    path = "qos"
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
