# Demo setup files

The files in this folder will help you setup your environment in air.nvidia.com to test the new **REST API** modules.

Please note that this is for internal use only!

# Files

- topology.dot : Use this to create Build Your Own Simulation on NVAir.
	- Remember to enable ZTP and uncomment the SSH sections to get the setup ready. The final ZTP script will look as below:
		> #!/bin/bash <br>
		\# Created by Topology-Converter v4.7.1 <br>
		\#    Template Revision: v4.7.1 <br>
		function error() { <br>
  		echo -e "e[0;33mERROR: The Zero Touch Provisioning script failed while running the command $BASH_COMMAND at line $BASH_LINENO.e[0m" >&2 <br>
		} <br>
		trap error ERR <br><br>
		SSH_URL="http://192.168.200.1/authorized_keys" <br>
		\# Uncomment to setup SSH key authentication for Ansible <br>
		mkdir -p /home/cumulus/.ssh <br>
		wget -O /home/cumulus/.ssh/authorized_keys $SSH_URL <br><br>
		\# Uncomment to unexpire and change the default cumulus user password <br>
		passwd -x 99999 cumulus <br>
		echo 'cumulus:CumulusLinux!' | chpasswd <br><br>
		\# Uncomment to make user cumulus passwordless sudo <br>
		echo "cumulus ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/10_cumulus <br><br>
		\# Uncomment to enable all debian sources & netq apps3 repo <br>
		\# sed -i 's/#deb/deb/g' /etc/apt/sources.list <br>
		\# wget -O pubkey https://apps3.cumulusnetworks.com/setup/cumulus-apps-deb.pubkey <br>
		\# apt-key add pubkey <br>
		\# rm pubkey <br><br>
		\# Uncomment to allow NTP to make large steps at service restart<br>
		echo "tinker panic 0" >> /etc/ntp.conf <br>
		systemctl enable ntp@mgmt <br><br>
		exit 0 <br>
		\#CUMULUS-AUTOPROVISIONING

- setup.sh: Use the script to prepare and setup your system with the new collections
	- The script updates the Ansible version to 2.11, prepares the directory structure to install the new collection, and installs the new collection from the development branch of the gitlab code.
	- Run the following commands to download the script onto your oob-mgmt-server and run it
		>`$ wget https://gitlab.com/nvidia-networking/systems-engineering/nvue/-/raw/develop/examples/nvair-demo/setup.sh` <br>
		`$ chmod +x setup.sh` <br>
		`$ ./setup.sh`

# Post installation steps

## Verify the installation

 - Run `ansible --version` to verify updated Ansible version
	 > ansible [core 2.11.12] <br>
  config file = /etc/ansible/ansible.cfg<br>
  configured module search path = ['/home/ubuntu/.ansible/plugins/modules', '/usr/share/ansible/plugins/modules'] <br>
  ansible python module location = /home/ubuntu/.local/lib/python3.6/site-packages/ansible <br>
  ansible collection location = /home/ubuntu/.ansible/collections:/usr/share/ansible/collections <br>
  executable location = /home/ubuntu/.local/bin/ansible <br>
  python version = 3.6.9 (default, Jun 29 2022, 11:45:57) [GCC 8.4.0] <br>
  jinja version = 2.10 <br>
  libyaml = True <br>
  - Run `ansible-galaxy collection list` to verify if the NVUE collection is installed
	  > \# /home/ubuntu/.ansible/collections/ansible_collections <br>
Collection  Version <br>
\----------- ------- <br>
**nvidia.nvue 1.1.0** <br>
\
\# /home/ubuntu/.local/lib/python3.6/site-packages/ansible_collections <br>
Collection                    Version <br>
\---------------------------- ------- <br>
amazon.aws                    1.5.1 <br>
ansible.netcommon             2.5.0 <br>
ansible.posix                 1.3.0 <br>
ansible.utils                 2.4.3 <br>
ansible.windows               1.8.0 <br>
arista.eos                    2.2.0 <br>
awx.awx                       19.4.0 <br>
azure.azcollection            1.10.0 <br>
check_point.mgmt              2.2.0 <br>
chocolatey.chocolatey         1.1.0 <br>
......

 - Change into the playbooks directory:
 `$ cd .ansible/collections/ansible_collections/nvidia/nvue/examples/playbooks/`

## Enable NVUE API on all of the switches

Since the NVUE REST API is not enabled by default, use the **enable-api.yml** under the examples/playbooks directory to enable it on all of the switches. The **hosts** file under the examples directory has the switch information. <br>
`ansible-playbook enable-api.yml -i ../hosts`

## Execute the other playbooks
In order to increase verbosity and see the outputs from the tasks veing run as part of the playbooks, add `-v` while running the `ansible-playbook` command.
- static-vxlan-leaf01.yaml
	> This sets up single VXLAN device configuration on `leaf01` <br>
		-   Sets the loopback address on each leaf <br>
		-   Creates a single VXLAN device (`vxlan48`), and maps `vlan 10` to `VNI 10` and `vlan 20` to `VNI 20` <br>
		-   Enables bridge learning on the single VXLAN device <br>
		-   Adds the VXLAN device to the default bridge `br_default` <br>
		-   Configures the local tunnel IP address to be the loopback address of the switch <br>
		-   Creates the static VXLAN tunnels by specifying the loopback addresses of the other leafs
- evpn-symmetric-leaf01.yaml
	> This sets up EVPN symmetric route configuration on `leaf01` <br>
		-  MLAG is configured between leaf01 and leaf02, leaf03 and leaf04, and border01 and border02 <br>
		-   BGP unnumbered is in the underlay (configured on all leafs and spines) <br>
		-   VRF BLUE and VRF RED are configured on the leafs for traffic flow between tenants for traffic isolation <br>
- evpn-multihoming-leaf01.yaml 
	> This sets up EVPN multihoming with head end replication using single VXLAN devices on `leaf01`
- fetch-objects-leaf01.yaml
	> This fetches current running configuration of various objects like `interface`, `bridge`, etc from `leaf01`


# Feedback
Please feel free to reach out to Krishna Vasudevan (kvasudevan@nvidia.com) for any feedback or queries.
