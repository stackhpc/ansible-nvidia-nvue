nvidia.nvue.bgp
=========

Role to setup BGP configuration.

Requirements
------------

The role uses the `router` and `vrf` modules from this collection.

Role Variables
--------------

The role uses the following variables:
  - Revision ID - Revision to push all the API requests to.
  - Autonomous System Number - ASN for all VRFs, if a single AS is in use. If "none", then ASN must be set for every VRF. This is the default.
  - Router ID - BGP router-id for all VRFs, if a common one is used. If "none", then router-id must be set for every VRF. This is the default.
  - Loopback IP - An IPv4 static network.
  - Neighbour ID - Peers.
These can be set in host_vars/group_vars.

Example Playbook
----------------

[Example playbook to setup BGP configuration on leaf switches](https://gitlab.com/nvidia-networking/systems-engineering/nvue/-/tree/main/examples/playbooks/roles/bgp-role-leaf.yml) 

License
-------

GNU General Public License v3.0 or later.

See [LICENSE](./LICENSE) to see the full text.
