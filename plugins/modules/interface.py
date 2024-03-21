#!/usr/bin/python

# Copyright: (c) 2022 NVIDIA
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = r'''
---
module: interface

short_description: This is the Cumulus Linux interface module

version_added: "1.0.0"

description: This is a Cumulus Linux module to interact with the interfaces object and the properties associated with an interface.

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
                description: Interface name.
                required: true
                type: str
            description:
                description: Details about the interface.
                required: false
                type: str
            type:
                description: Type of interface.
                required: false
                type: str
                choices:
                    - swp
                    - eth
                    - bond
                    - loopback
                    - svi
                    - sub
                    - peerlink
                    - tunnel
            base_interface:
                description: Base interface.
                required: false
                type: str
            vlan:
                description: VLAN ID.
                required: false
                type: int
            bond:
                description: Bond configuration on the interface.
                required: false
                type: dict
                suboptions:
                    mode:
                        description: Bond mode.
                        required: false
                        type: str
                        default: lacp
                        choices:
                            - lacp
                            - static
                    lacp_bypass:
                        description: Turn the feature 'on' or 'off'.
                        required: false
                        type: str
                        default: 'off'
                        choices:
                            - 'on'
                            - 'off'
                    member:
                        description: Bond member interface
                        required: false
                        type: list
                        elements: dict
                        suboptions:
                            id:
                                description: interface
                                required: false
                                type: str
                    mlag:
                        description: Bond MLAG config
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
                            id:
                                description: MLAG ID
                                required: false
                                type: int
            bridge:
                description: Bridge configuration on the interface.
                required: false
                type: dict
                suboptions:
                    domain:
                        description: Bridge domain.
                        required: false
                        type: list
                        elements: dict
                        suboptions:
                            id:
                                description: Bridge domain identifier.
                                required: false
                                type: str
                            access:
                                description: Access.
                                required: false
                                type: int
                            untagged:
                                description: Untagged packets ingressing on the interface will be put in this vlan. Egress packets are always
                                             tagged. If none, then untagged packets will be dropped. If auto, inherit from bridge domain.
                                required: false
                                type: int
                            vlan:
                                description: Set of allowed vlans for this bridge domain on this interface. If "all", inherit all vlans from the
                                             bridge domain, if appropriate. This is the default.
                                required: false
                                type: list
                                elements: dict
                                suboptions:
                                    id:
                                        description: VLAN tag identifier.
                                        required: false
                                        type: str
                            stp:
                                description: Bridge STP config.
                                required: false
                                type: dict
                                suboptions:
                                    admin_edge:
                                        description: Admin Edge.
                                        required: false
                                        type: str
                                        choices:
                                            - 'on'
                                            - 'off'
                                    auto_edge:
                                        description: Auto Edge.
                                        required: false
                                        type: str
                                        choices:
                                            - 'on'
                                            - 'off'
                                    bpdu_guard:
                                        description: BPDU Guard.
                                        required: false
                                        type: str
                                        choices:
                                            - 'on'
                                            - 'off'
            router:
                description: Interface router.
                required: false
                type: dict
                suboptions:
                    ospf:
                        description: OSPF interface configuration.
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
                            area:
                                description: Area number for enabling ospf on this interface.
                                required: false
                                type: str
                            network_type:
                                description: Network type.
                                required: false
                                type: str
                                default: broadcast
                                choices:
                                    - broadcast
                                    - non-broadcast
                                    - point-to-point
                                    - point-to-multipoint
                            passive:
                                description: Stops the creation of peers on this interface.
                                required: false
                                type: str
                                choices:
                                    - 'on'
                                    - 'off'
                            timers:
                                description: Timers configuration.
                                required: false
                                type: dict
                                suboptions:
                                    dead_interval:
                                        description: Length of time, in seconds, without a hello before declaring the neighbor dead.
                                                     If minimal, hello-multiplier must be set.
                                        required: false
                                        type: str
                                    hello_interval:
                                        description: How often to transmit a hello packet, in seconds. Only valid if dead-interval is not minimal.
                                        required: false
                                        type: int
                                    hello_multiplier:
                                        description: Required and only valid if dead-interval is minimal.
                                        required: false
                                        type: int
                    pim:
                        description: PIM interface configuration.
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
                            address_family:
                                description: Address family specific configuration.
                                required: false
                                type: dict
                                suboptions:
                                    ipv4_unicast:
                                        description: IPv4 unicast address family.
                                        required: false
                                        type: dict
                                        suboptions:
                                            use_source:
                                                description: Use unique source address in PIM Hello source field.
                                                required: false
                                                type: str
            link:
                description: Link configuration on the interface.
                required: false
                type: dict
                suboptions:
                    breakout:
                        description: sub-divide or disable ports (only valid on plug interfaces).
                        type: list
                        required: false
                        elements: dict
                        suboptions:
                            id:
                                description: A breakout mode.
                                type: str
                                required: false
                                choices:
                                    - '1x'
                                    - '2x'
                                    - '4x'
                                    - '8x'
                                    - 'disabled'
                                    - 'loopback'
                            lanes_per_port:
                                description: Number of serdes lanes to be mapped/enabled for a split-port.
                                type: str
                                required: false
                                choices:
                                    - '1'
                                    - '2'
                                    - '4'
                                    - '8'
                    mtu:
                        description: MTU size.
                        required: false
                        type: int
                    state:
                        description: Link state
                        required: false
                        type: list
                        elements: dict
                        suboptions:
                            id:
                                description: Up/Down
                                required: false
                                type: str
            ip:
                description: IP configuration on the interface.
                required: false
                type: dict
                suboptions:
                    address:
                        description: IPv4 and IPv6 address.
                        required: false
                        type: list
                        elements: dict
                        suboptions:
                            id:
                                description: An IP address with prefix.
                                required: false
                                type: str
                    gateway:
                        description: Default IPv4 and IPv6 gateways.
                        required: false
                        type: list
                        elements: dict
                        suboptions:
                            id:
                                description: An IP address.
                                required: false
                                type: str
                    vrf:
                        description: Virtual routing and forwarding.
                        required: false
                        type: str
                        default: default
                    vrr:
                        description: VRR
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
                            address:
                                description: VRR address on the interface.
                                required: false
                                type: list
                                elements: dict
                                suboptions:
                                    id:
                                        description: VRR address.
                                        required: false
                                        type: str
                            mac_address:
                                description: MAC Address.
                                required: false
                                type: str
                            state:
                                description: VRR state
                                required: false
                                type: list
                                elements: dict
                                suboptions:
                                    id:
                                        description: Up/Down
                                        required: false
                                        type: str
                    igmp:
                        description: Configuration for IGMP.
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
            evpn:
                description: EVPN control plane config and info for VRF.
                required: false
                type: dict
                suboptions:
                    multihoming:
                        description: Multihoming interface configuration parameters.
                        required: false
                        type: dict
                        suboptions:
                            uplink:
                                description: Enable evpn multihoming tracking to prevent traffic loss due to NVE connectivity loss,
                                             uplink's operational state is tracked when enabled.
                                required: false
                                type: str
                                default: 'off'
                                choices:
                                    - 'on'
                                    - 'off'
                            segment:
                                description: Multihoming interface segment.
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
                                    local_id:
                                        description: Ethernet segment local-id. If provided, it will be combined with the global multihoming mac-address to
                                                     create the ethernet segment identifier, which must be unique for each segment
                                                     and match other bonds in the segment.
                                        required: false
                                        type: int
                                    identifier:
                                        description: Ethernet segment identifier. This must be unique for each segment and match other bonds in the segment.
                                        required: false
                                        type: str
                                    mac_address:
                                        description: MAC address for this ethernet segment. If 'auto', the global evpn multihoming mac-address will be used.
                                                     This is the default.
                                        required: false
                                        type: str
                                        default: auto
                                    df_preference:
                                        description: Designated forwarder preference value for this ethernet segment. If 'auto', the global evpn multihoming
                                                     preference will be used. This is the default.
                                        required: false
                                        type: int
            tunnel:
                description: The state of the interface.
                required: false
                type: dict
                suboptions:
                    source_ip:
                        description: Source underlay IP address.
                        required: false
                        type: str
                    dest_ip:
                        description: Destination underlay IP address.
                        required: false
                        type: str
                    ttl:
                        description: Time to live.
                        required: false
                        type: int
                        default: 64
                    mode:
                        description: Tunnel mode.
                        required: false
                        type: str
                        default: gre
                    interface:
                        description: Physical underlay interface to used for Tunnel packets.
                        required: false
                        type: str
    revid:
        description: Revision ID to query/to apply config to.
        required: false
        type: str
    interfaceid:
        description: Specific interface to query/modify.
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
- name: Display all the interfaces in the environment
  nvidia.nvue.interface:
    state: gathered

- name: Add IP address to an interface
  nvidia.nvue.interface:
    state: merged
    force: yes
    wait: 15
    data:
        - id: lo
          ip:
            address:
                - id: '10.10.10.1/32'
          type: 'loopback'
'''

RETURN = r'''
# These are examples of possible return values, and in general should use other names for return values.
changed:
  description: whether a configuration was changed
  returned: always
  type: bool
  sample: true
message:
    description: details of the interface (for gathered) or whether the change was applied (for merged)
    type: dict
    returned: always
    sample:
        - eth0:
            acl: {}
            ip:
                address:
                    dhcp: {}
                gateway: {}
                ipv4:
                    forward: off
                ipv6:
                    enable: on
                    forward: off
                vrf: mgmt
            link:
                auto-negotiate: on
                duplex: full
                fec: auto
                mtu: 9216
                speed: auto
                state:
                    up: {}
            type: eth
        - message: Config update by cumulus
          state: applied
          transition:
            issue: {}
            progress: ""
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
    #  define the interface spec - used for creation/modification
    interface_spec = dict(
        id=dict(type='str', required=True),
        description=dict(type='str', required=False),
        type=dict(type='str', required=False, choices=['swp', 'eth', 'bond', 'loopback', 'svi', 'sub', 'peerlink', 'tunnel']),
        bond=dict(type='dict', required=False, options=dict(
            mode=dict(type='str', required=False, choices=['lacp', 'static'], default='lacp'),
            lacp_bypass=dict(type='str', required=False, choices=['on', 'off'], default='off'),
            member=dict(type='list', required=False, elements='dict', options=dict(
                id=dict(type='str', required=False)
            )),
            mlag=dict(type='dict', required=False, options=dict(
                enable=dict(type='str', required=False, choices=['on', 'off'], default='off'),
                id=dict(type='int', required=False)
            ))
        )),
        bridge=dict(type='dict', required=False, options=dict(
            domain=dict(type='list', required=False, elements='dict', options=dict(
                id=dict(type='str', required=False),
                access=dict(type='int', required=False),
                untagged=dict(type='int', required=False),
                stp=dict(type='dict', required=False, options=dict(
                    admin_edge=dict(type='str', required=False, choices=['on', 'off']),
                    auto_edge=dict(type='str', required=False, choices=['on', 'off']),
                    bpdu_guard=dict(type='str', required=False, choices=['on', 'off'])
                )),
                vlan=dict(type='list', required=False, elements='dict', options=dict(
                    id=dict(type='str', required=False)
                ))
            ))
        )),
        router=dict(type='dict', required=False, options=dict(
            ospf=dict(type='dict', required=False, options=dict(
                enable=dict(type='str', required=False, choices=['on', 'off'], default='off'),
                area=dict(type='str', required=False),
                network_type=dict(type='str', required=False, choices=['broadcast', 'non-broadcast', 'point-to-point', 'point-to-multipoint'],
                                  default='broadcast'),
                passive=dict(type='str', required=False, choices=['on', 'off']),
                timers=dict(type='dict', required=False, options=dict(
                    dead_interval=dict(type='str', required=False),
                    hello_interval=dict(type='int', required=False),
                    hello_multiplier=dict(type='int', required=False)
                ))
            )),
            pim=dict(type='dict', required=False, options=dict(
                enable=dict(type='str', required=False, choices=['on', 'off'], default='off'),
                address_family=dict(type='dict', required=False, options=dict(
                    ipv4_unicast=dict(type='dict', required=False, options=dict(
                        use_source=dict(type='str', required=False)
                    ))
                ))
            ))
        )),
        link=dict(type='dict', required=False, options=dict(
            breakout=dict(type='list', required=False, elements='dict', options=dict(
                id=dict(type='str', required=False, choices=['1x', '2x', '4x', '8x', 'disabled', 'loopback']),
                lanes_per_port=dict(type='str', required=False, choices=['1', '2', '4', '8'])
            )),
            mtu=dict(type='int', required=False),
            state=dict(type='list', required=False, elements='dict', options=dict(
                id=dict(type='str', required=False)
            ))
        )),
        ip=dict(type='dict', required=False, options=dict(
            address=dict(type='list', required=False, elements='dict', options=dict(
                id=dict(type='str', required=False)
            )),
            gateway=dict(type='list', required=False, elements='dict', options=dict(
                id=dict(type='str', required=False)
            )),
            vrf=dict(type='str', required=False, default='default'),
            vrr=dict(type='dict', required=False, options=dict(
                enable=dict(type='str', required=False, choices=['on', 'off'], default='off'),
                address=dict(type='list', required=False, elements='dict', options=dict(
                    id=dict(type='str', required=False)
                )),
                mac_address=dict(type='str', required=False),
                state=dict(type='list', required=False, elements='dict', options=dict(
                    id=dict(type='str', required=False)
                ))
            )),
            igmp=dict(type='dict', required=False, options=dict(
                enable=dict(type='str', required=False, choices=['on', 'off'], default='off')
            ))
        )),
        evpn=dict(type='dict', required=False, options=dict(
            multihoming=dict(type='dict', required=False, options=dict(
                uplink=dict(type='str', required=False, choices=['on', 'off'], default='off'),
                segment=dict(type='dict', required=False, options=dict(
                    enable=dict(type='str', required=False, choices=['on', 'off'], default='off'),
                    local_id=dict(type='int', required=False),
                    identifier=dict(type='str', required=False),
                    mac_address=dict(type='str', required=False, default='auto'),
                    df_preference=dict(type='int', required=False)
                ))
            ))
        )),
        tunnel=dict(type='dict', required=False, options=dict(
            source_ip=dict(type='str', required=False),
            dest_ip=dict(type='str', required=False),
            ttl=dict(type='int', required=False, default=64),
            mode=dict(type='str', required=False, default='gre'),
            interface=dict(type='str', required=False)
        )),
        base_interface=dict(type='str', required=False),
        vlan=dict(type='int', required=False)
    )

    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        force=dict(type='bool', required=False, default=False),
        wait=dict(type="int", required=False, default=0),
        state=dict(type='str', required=True, choices=["gathered", "deleted", "merged"]),
        revid=dict(type='str', required=False),
        interfaceid=dict(type='str', required=False),
        data=dict(type='list', required=False, elements='dict', options=interface_spec),
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

    path = "interface"
    if module.params["interfaceid"] is not None:
        path = path + "/" + module.params["interfaceid"]
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
