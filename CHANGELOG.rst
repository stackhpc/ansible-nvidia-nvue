=========================
nvidia.nvue Release Notes
=========================

.. contents:: Topics

v1.2.0
======

Release Summary
---------------

Release with new modules and updated examples.

Major Changes
-------------

- New Module: nvidia.nvue.qos

Minor Changes
-------------
- Support for route filter functionality
- Updates to the command module to implement the diff functionality

Bugfixes
--------
- Updates removing config
- null values getting populated if full sub dictionary items were not passed in the playbook.

v1.1.0
======

Release Summary
---------------

Release with new modules and roles.

Major Changes
-------------

- New Module: nvidia.nvue.acl
- New roles: nvidia.nvue.system, nvidia.nvue.bgp, nvidia.nvue.mlag

Minor Changes
-------------
- Updates to api and command modules
- Added update-source field to vrf module (`Update-source in BGP configuration<https://docs.nvidia.com/networking-ethernet-software/cumulus-linux-55/Layer-3/Border-Gateway-Protocol-BGP/Optional-BGP-Configuration/#update-source>`)

Bugfixes
--------
- autonomous_system field type in nvidia.nvue.vrf module

v1.0.1
======

Release Summary
---------------

Additional of object-specific modules.

Major Changes
-------------

- nvidia.nvue.bridge
- nvidia.nvue.config
- nvidia.nvue.evpn
- nvidia.nvue.interface
- nvidia.nvue.mlag
- nvidia.nvue.router
- nvidia.nvue.service
- nvidia.nvue.system
- nvidia.nvue.vrf
- nvidia.nvue.vxlan

Minor Changes
-------------


Bugfixes
--------



v1.0.0
======

Release Summary
---------------

Initial release.

Major Changes
-------------

- nvidia.nvue.command
- nvidia.nvue.api

Minor Changes
-------------

- remove `debug.yml` playbook

Bugfixes
--------

