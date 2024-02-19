nvidia.nvue.mlag
=========

Role to setup MLAG configuration.

Requirements
------------

The role uses the `bridge`, `interface`,  and `mlag` modules from this collection.

Role Variables
--------------

The role uses the following variables:
  - Revision ID - Revision to push all the API requests to.
  - Interface ID - Name of interface (for VLAN interfaces).
  - Interface IP address - IP address to be assigned to the interface (for VLAN interfaces).
  - VLAN - VLAN ID of the interface (for VLAN interfaces).
  - MLAG ID - MLAG configuration (for Bond interfaces).
  - Member - Set of bond members (for Bond interfaces).
  - Bridge Domain - Bridge domains on this interface (for Bond interfaces).
  - MLAG MAC - MAC Address.
  - MLAG backup - Alternative ip address or interface for peer to reach us.
These can be set in host_vars/group_vars.

Example Playbook
----------------

[Example playbook to setup MLAG configuration on leaf switches](https://gitlab.com/nvidia-networking/systems-engineering/nvue/-/blob/main/examples/playbooks/roles/mlag-role-leaf.yml) 

License
-------

GNU General Public License v3.0 or later.

See [LICENSE](./LICENSE) to see the full text.
