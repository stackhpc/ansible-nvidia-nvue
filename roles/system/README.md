nvidia.nvue.system
=========

Role to setup system configuration.

Requirements
------------

The role uses the `system` module from this collection.

Role Variables
--------------

The role uses the following variables:
  - Revision ID - Revision to push all the API requests to.
  - Hostname - Hostname of the switch.
These can be set in host_vars/group_vars.

Example Playbook
----------------

[Example playbook to setup system configuration on switches](https://gitlab.com/nvidia-networking/systems-engineering/nvue/-/blob/main/examples/playbooks/roles/system-role.yml) 

License
-------

GNU General Public License v3.0 or later.

See [LICENSE](./LICENSE) to see the full text.
