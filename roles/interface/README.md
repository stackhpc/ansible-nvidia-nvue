nvidia.nvue.interface
=========

Role to setup interfaces configuration. It brings up interfaces and sets the `loopback` and `eth0` interfaces.

Requirements
------------

The role uses the `interface` module from this collection.

Role Variables
--------------

The role uses the following variables:
  - Revision ID - Revision to push all the API requests to.
  - Interface ID - Interfaces to bring up.
  - eth0 IP - IP address to be assigned to eth0 interface.
  - lo IP - IP address to be assigned to the loopback interface.
These can be set in host_vars/group_vars.

Example Playbook
----------------

[Example playbook to setup BGP configuration on leaf switches](https://gitlab.com/nvidia-networking/systems-engineering/nvue/-/tree/main/examples/playbooks/roles/bgp-role-leaf.yml) 

License
-------

GNU General Public License v3.0 or later.

See [LICENSE](./LICENSE) to see the full text.
