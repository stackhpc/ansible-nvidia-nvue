#!/usr/bin/python

# Copyright: (c) 2022 NVIDIA
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = r'''
---
module: vrf

short_description: This is the Cumulus Linux vrf module

version_added: "1.0.0"

description: This is a Cumulus Linux module to interact with the vrf object.

options:
    filters:
        description: Filters used while fetching information about the system
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
                description: VRF ID.
                required: true
                type: str
            evpn:
                description: EVPN control plane config and info for VRF.
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
                    vlan:
                        description: VLAN ID
                        required: false
                        type: int
                    vni:
                        description: L3 VNI
                        type: list
                        elements: dict
                        suboptions:
                            id:
                                description: VNI.
                                required: false
                                type: str
            router:
                description: Router configuration on the VRF.
                required: false
                type: dict
                suboptions:
                    bgp:
                        description: BGP VRF configuration.
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
                            autonomous_system:
                                description: ASN for this VRF. If "auto", inherit from the global config. This is the default.
                                required: false
                                type: str
                            router_id:
                                description: BGP router-id for this VRF. If "auto", inherit from the global config. This is the default.
                                required: false
                                type: str
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
                                            enable:
                                                description: Turn the feature 'on' or 'off'.
                                                required: false
                                                type: str
                                                default: 'on'
                                                choices:
                                                    - 'on'
                                                    - 'off'
                                            network:
                                                description: IPv4 static networks.
                                                required: false
                                                type: list
                                                elements: dict
                                                suboptions:
                                                    id:
                                                        description: An IPv4 static network.
                                                        required: false
                                                        type: str
                                            route_export:
                                                description: Route export.
                                                required: false
                                                type: dict
                                                suboptions:
                                                    to_evpn:
                                                        description: Controls for exporting routes from this VRF for this address-family
                                                                     into EVPN (as type-5 routes).
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
                                            redistribute:
                                                description: Route redistribute.
                                                required: false
                                                type: dict
                                                suboptions:
                                                    connected:
                                                        description: Route redistribution of IPv4 connected routes.
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
                                                    static:
                                                        description: Route redistribution of IPv4 static routes.
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
                                    l2vpn_evpn:
                                        description: L2VPN EVPN address family.
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
                            neighbor:
                                description: Peers.
                                required: false
                                type: list
                                elements: dict
                                suboptions:
                                    id:
                                        description: Interface.
                                        required: false
                                        type: str
                                    enable:
                                        description: Turn the feature 'on' or 'off'.
                                        required: false
                                        type: str
                                        default: 'on'
                                        choices:
                                            - 'on'
                                            - 'off'
                                    peer_group:
                                        description: Optional peer-group to which the peer is attached to inherit the group's configuration.
                                        required: false
                                        type: str
                                    type:
                                        description: Type of peer.
                                        required: false
                                        type: str
                                        choices:
                                            - numbered
                                            - unnumbered
                                    remote_as:
                                        description: ASN for the BGP neighbor(s) using this configuration. If specified as 'external', it means an EBGP
                                                     configuration but the actual ASN is immaterial. If specified as 'internal', it means an IBGP configuration.
                                        required: false
                                        type: str
                                    address_family:
                                        description: Address family specific configuration.
                                        required: false
                                        type: dict
                                        suboptions:
                                            l2vpn_evpn:
                                                description: Peer L2VPN EVPN address family.
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
                            peer_group:
                                description: Peer groups.
                                required: false
                                type: list
                                elements: dict
                                suboptions:
                                    id:
                                        description: Peer group.
                                        required: false
                                        type: str
                                    remote_as:
                                        description: ASN for the BGP neighbor(s) using this configuration. If specified as 'external', it means an EBGP
                                                     configuration but the actual ASN is immaterial. If specified as 'internal', it means an IBGP configuration.
                                        required: false
                                        type: str
                                    address_family:
                                        description: Address family specific configuration.
                                        required: false
                                        type: dict
                                        suboptions:
                                            ipv4_unicast:
                                                description: Peer IPv4 unicast address family. Always on, unless disabled globaly.
                                                required: false
                                                type: dict
                                                suboptions:
                                                    enable:
                                                        description: Turn the feature 'on' or 'off'.
                                                        required: false
                                                        type: str
                                                        default: 'on'
                                                        choices:
                                                            - 'on'
                                                            - 'off'
                                            l2vpn_evpn:
                                                description: Peer L2VPN EVPN address family.
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
                            route_import:
                                description: Controls for importing of IPv4 and IPv6 routes from this VRF.
                                required: false
                                type: dict
                                suboptions:
                                    from_evpn:
                                        description: Controls for importing EVPN type-2 and type-5 routes into this VRF.
                                        required: false
                                        type: dict
                                        suboptions:
                                            route_target:
                                                description: List of the RTs to attach to host or prefix routes when importing them into VRF or "auto".
                                                             If "auto", the RT will be derived. This is the default..
                                                required: false
                                                type: list
                                                elements: dict
                                                suboptions:
                                                    id:
                                                        description: A route target identifier.
                                                        required: false
                                                        type: str
                    ospf:
                        description: OSPF VRF configuration.
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
                            router_id:
                                description: BGP router-id for this VRF. If "auto", inherit from the global config. This is the default.
                                required: false
                                type: str
                    pim:
                        description: PIM VRF configuration.
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
                            ecmp:
                                description: Choose all available ECMP paths for a particular RPF. If 'off', the first nexthop found will be used.
                                             This is the default.
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
                                    rebalance:
                                        description: Recalculate all multicast streams in the event of path going down.
                                                     If 'off', only the impacted streams by path going down recalculated. This is the default.
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
                                            rp:
                                                description: RP address and associated group range.
                                                required: false
                                                type: list
                                                elements: dict
                                                suboptions:
                                                    id:
                                                        description: RP.
                                                        required: false
                                                        type: str
                                                    prefix_list:
                                                        description: Prefix-list to specify multicast group range.
                                                        required: false
                                                        type: str
                                                    group_range:
                                                        description: Set of group range assocaited to RP.
                                                        required: false
                                                        type: list
                                                        elements: dict
                                                        suboptions:
                                                            id:
                                                                description: A group range.
                                                                required: false
                                                                type: str
                            msdp_mesh_group:
                                description: To connect multiple PIM-SM multicast domains using RPs.
                                required: false
                                type: list
                                elements: dict
                                suboptions:
                                    id:
                                        description: MSDP mesh-group.
                                        required: false
                                        type: str
                                    source_address:
                                        description: MSDP mesh-group source IP address.
                                        required: false
                                        type: str
                                    member_address:
                                        description: Set of member-address.
                                        required: false
                                        type: list
                                        elements: dict
                                        suboptions:
                                            id:
                                                description: A MSDP mesh member.
                                                required: false
                                                type: str
                    static:
                        description: Statis route info on the VRF.
                        required: false
                        type: list
                        elements: dict
                        suboptions:
                            id:
                                description: Route.
                                required: false
                                type: str
                            address_family:
                                description: Route address family.
                                required: false
                                type: str
                                default: ipv4-unicast
                            via:
                                description: Nexthops.
                                required: false
                                type: list
                                elements: dict
                                suboptions:
                                    id:
                                        description: A via.
                                        required: false
                                        type: str
                                    type:
                                        description: Type of via.
                                        required: false
                                        type: str
                                        choices:
                                            - interface
                                            - ipv4-address
                                            - ipv6-address
                                            - blackhole
                                            - reject
    revid:
        description: Revision ID to query/to apply config to.
        required: false
        type: str
    vrfid:
        description: Specific VRF to query/modify.
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
- name: List all the VRFs and their configuration
  nvidia.nvue.vrf:
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
    #  define the VRF spec - used for creation/modification
    vrf_spec = dict(
        id=dict(type='str', required=True),
        evpn=dict(type='dict', required=False, options=dict(
            enable=dict(type='str', required=False, choices=['on', 'off'], default='off'),
            vlan=dict(type='int', required=False),
            vni=dict(type='list', required=False, elements='dict', options=dict(
                id=dict(type='str', required=False))
            )
        )),
        router=dict(type='dict', required=False, options=dict(
            bgp=dict(type='dict', required=False, options=dict(
                enable=dict(type='str', required=False, choices=['on', 'off'], default='off'),
                autonomous_system=dict(type='str', required=False),
                router_id=dict(type='str', required=False),
                address_family=dict(type='dict', required=False, options=dict(
                    ipv4_unicast=dict(type='dict', required=False, options=dict(
                        enable=dict(type='str', required=False, choices=['on', 'off'], default='on'),
                        network=dict(type='list', required=False, elements='dict', options=dict(
                            id=dict(type='str', required=False)
                        )),
                        route_export=dict(type='dict', required=False, options=dict(
                            to_evpn=dict(type='dict', required=False, options=dict(
                                enable=dict(type='str', required=False, choices=['on', 'off'], default='off')
                            ))
                        )),
                        redistribute=dict(type='dict', required=False, options=dict(
                            connected=dict(type='dict', required=False, options=dict(
                                enable=dict(type='str', required=False, choices=['on', 'off'], default='off')
                            )),
                            static=dict(type='dict', required=False, options=dict(
                                enable=dict(type='str', required=False, choices=['on', 'off'], default='off')
                            ))
                        ))
                    )),
                    l2vpn_evpn=dict(type='dict', required=False, options=dict(
                        enable=dict(type='str', required=False, choices=['on', 'off'], default='off')
                    ))
                )),
                neighbor=dict(type='list', required=False, elements='dict', options=dict(
                    id=dict(type='str', required=False),
                    enable=dict(type='str', required=False, default='on', choices=['on', 'off']),
                    peer_group=dict(type='str', required=False),
                    type=dict(type='str', required=False, choices=['numbered', 'unnumbered']),
                    remote_as=dict(type='str', required=False),
                    address_family=dict(type='dict', required=False, options=dict(
                        l2vpn_evpn=dict(type='dict', required=False, options=dict(
                            enable=dict(type='str', required=False, choices=['on', 'off'], default='off')
                        ))
                    ))
                )),
                peer_group=dict(type='list', required=False, elements='dict', options=dict(
                    id=dict(type='str', required=False),
                    remote_as=dict(type='str', required=False),
                    address_family=dict(type='dict', required=False, options=dict(
                        ipv4_unicast=dict(type='dict', required=False, options=dict(
                            enable=dict(type='str', required=False, choices=['on', 'off'], default='on')
                        )),
                        l2vpn_evpn=dict(type='dict', required=False, options=dict(
                            enable=dict(type='str', required=False, choices=['on', 'off'], default='off')
                        ))
                    ))
                )),
                route_import=dict(type='dict', required=False, options=dict(
                    from_evpn=dict(type='dict', required=False, options=dict(
                        route_target=dict(type='list', required=False, elements='dict', options=dict(
                            id=dict(type='str', required=False)
                        ))
                    ))
                ))
            )),
            ospf=dict(type='dict', required=False, options=dict(
                enable=dict(type='str', required=False, choices=['on', 'off'], default='off'),
                router_id=dict(type='str', required=False)
            )),
            pim=dict(type='dict', required=False, options=dict(
                enable=dict(type='str', required=False, choices=['on', 'off'], default='off'),
                ecmp=dict(type='dict', required=False, options=dict(
                    enable=dict(type='str', required=False, choices=['on', 'off'], default='off'),
                    rebalance=dict(type='str', required=False, choices=['on', 'off'], default='off')
                )),
                address_family=dict(type='dict', required=False, options=dict(
                    ipv4_unicast=dict(type='dict', required=False, options=dict(
                        rp=dict(type='list', required=False, elements='dict', options=dict(
                            id=dict(type='str', required=False),
                            prefix_list=dict(type='str', required=False),
                            group_range=dict(type='list', required=False, elements='dict', options=dict(
                                id=dict(type='str', required=False)
                            ))
                        ))
                    ))
                )),
                msdp_mesh_group=dict(type='list', required=False, elements='dict', options=dict(
                    id=dict(type='str', required=False),
                    source_address=dict(type='str', required=False),
                    member_address=dict(type='list', required=False, elements='dict', options=dict(
                        id=dict(type='str', required=False)
                    ))
                ))
            )),
            static=dict(type='list', required=False, elements='dict', options=dict(
                id=dict(type='str', required=False),
                address_family=dict(type='str', required=False, default='ipv4-unicast'),
                via=dict(type='list', required=False, elements='dict', options=dict(
                    id=dict(type='str', required=False),
                    type=dict(type='str', required=False, choices=['interface', 'ipv4-address', 'ipv6-address', 'blackhole', 'reject'])
                ))
            ))
        )),
    )

    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        force=dict(type='bool', required=False, default=False),
        wait=dict(type="int", required=False, default=0),
        revid=dict(type='str', required=False),
        state=dict(type='str', required=True, choices=['gathered', 'deleted', 'merged']),
        vrfid=dict(type='str', required=False),
        data=dict(type='list', required=False, elements='dict', options=vrf_spec),
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

    path = "vrf"
    if module.params["vrfid"] is not None:
        path = path + "/" + module.params["vrfid"]
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
