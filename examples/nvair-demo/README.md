# Demo setup files

The files in this folder will help you setup your environment in air.nvidia.com to test the new **REST API** modules.

# Files

- topology.dot : Use this to create Build Your Own Simulation on NVAir.
	> Remember to enable ZTP and uncomment the SSH sections to get the setup ready
- setup.sh: Use the script to prepare and setup your system with the new collections
	> The script updates the Ansible version to 2.11, prepares the directory structure to install the new collection, and installs the new collection from the development branch of the gitlab code.

# Post installation steps

## Verify the installation

 - Run `ansible --version` to verify updated Ansible version
	 > ansible [core 2.11.12]
  config file = /etc/ansible/ansible.cfg
  configured module search path = ['/home/ubuntu/.ansible/plugins/modules', '/usr/share/ansible/plugins/modules']
  ansible python module location = /home/ubuntu/.local/lib/python3.6/site-packages/ansible
  ansible collection location = /home/ubuntu/.ansible/collections:/usr/share/ansible/collections
  executable location = /home/ubuntu/.local/bin/ansible
  python version = 3.6.9 (default, Jun 29 2022, 11:45:57) [GCC 8.4.0]
  jinja version = 2.10
  libyaml = True
  - Run `ansible-galaxy collection list` to verify if the NVUE collection is installed
	  > \# /home/ubuntu/.ansible/collections/ansible_collections
Collection  Version
\----------- -------
**nvidia.nvue** 1.0.0
\
\# /home/ubuntu/.local/lib/python3.6/site-packages/ansible_collections
Collection                    Version
\---------------------------- -------
amazon.aws                    1.5.1
ansible.netcommon             2.5.0
ansible.posix                 1.3.0
ansible.utils                 2.4.3
ansible.windows               1.8.0
arista.eos                    2.2.0
awx.awx                       19.4.0
azure.azcollection            1.10.0
check_point.mgmt              2.2.0
chocolatey.chocolatey         1.1.0


## Enable NVUE API on all of the switches

Since the NVUE REST API is not enabled by default, use the **enable-api.yml** under the examples/playbooks directory to enable it on all of the switches. The **hosts** file under the examples directory has the switch information.
`ansible-playbook enable-api.yml -i ../hosts`

## Execute the other playbooks
In order to increase verbosity and see the outputs from the tasks veing run as part of the playbooks, add `-v` while running the `ansible-playbook` command.
- static-vxlan-leaf01.yaml
	> This sets up single VXLAN device configuration on `leaf01`
		-   Sets the loopback address on each leaf
		-   Creates a single VXLAN device (`vxlan48`), and maps `vlan 10` to `VNI 10` and `vlan 20` to `VNI 20`
		-   Enables bridge learning on the single VXLAN device
		-   Adds the VXLAN device to the default bridge `br_default`
		-   Configures the local tunnel IP address to be the loopback address of the switch
		-   Creates the static VXLAN tunnels by specifying the loopback addresses of the other leafs
- evpn-symmetric-leaf01.yaml
	> This sets up EVPN symmetric route configuration on `leaf01`
		-  MLAG is configured between leaf01 and leaf02, leaf03 and leaf04, and border01 and border02
		-   BGP unnumbered is in the underlay (configured on all leafs and spines)
		-   VRF BLUE and VRF RED are configured on the leafs for traffic flow between tenants for traffic isolation
- evpn-multihoming-leaf01.yaml
	> This sets up EVPN multihoming with head end replication using single VXLAN devices on `leaf01`
- fetch-objects-leaf01.yaml
	> This fetches current running configuration of various objects like `interface`, `bridge`, etc from `leaf01`


# Feedback
Please feel free to reach out to Krishna Vasudevan (kvasudevan@nvidia.com) for any feedback or queries.
