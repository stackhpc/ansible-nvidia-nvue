# NVIDIA Cumulus Linux Automation Workshop using NVUE and Ansible

This branch contains NVUE and Ansible automation to configure different demo scenarios using [NVUE](https://docs.nvidia.com/networking-ethernet-software/cumulus-linux/System-Configuration/NVIDIA-User-Experience-NVUE/) on Cumulus Linux 5.5.

[![License](https://img.shields.io/badge/License-Apache%202.0-83389B.svg)](https://opensource.org/licenses/Apache-2.0)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](http://makeapullrequest.com)
[![Slack Status](https://img.shields.io/badge/Slack-2800+-F1446F)](https://slack.cumulusnetworks.com)
[![Code of Conduct](https://img.shields.io/badge/Contributing-Code%20of%20Conduct-1EB5BD)](https://docs.cumulusnetworks.com/contributor-guide/#contributor-covenant-code-of-conduct)

<img src="https://www.ansible.com/hubfs/2016_Images/Assets/Ansible-Mark-Large-RGB-BlackOutline.png" height="150" title="Ansible" /> 
<img src="https://www.nvidia.com/content/dam/en-zz/Solutions/about-nvidia/logo-and-brand/01-nvidia-logo-vert-500x200-2c50-d@2x.png" height="150" title="NVIDIA" />

This repository contains examples that will help you understand the [Ansible NVUE modules](https://galaxy.ansible.com/nvidia/nvue) and use it to configure various scenarios. 

## How to Use

Install the Ansible NVUE module using:
```
ubuntu@oob-management:~ $ ansible-galaxy install nvidia.nvue
```
Clone this repository to access the examples, and run the playbooks in the `playbooks/` directory with the `ansible-playbook` command and specify the inventory `hosts` file using the `-i` flag:
```bash
ubuntu@server:~$ git clone https://gitlab.com/nvidia-networking/systems-engineering/nvue.git
ubuntu@server:~$ cd nvue/
ubuntu@server:~/cumulus_ansible_modules$ git checkout cumulus-linux-58-automation-workshop
ubuntu@server:~/cumulus_ansible_modules-nvue$ ansible-playbook playbooks/api.yml -i hosts
```

## Requirements

* NVIDIA Cumulus Linux Version

```bash
cumulus@leaf01:mgmt:~$ nv show system
             operational          applied
-----------  -------------------  -------
hostname     leaf01               cumulus
build        Cumulus Linux 5.8.0
uptime       14:53:42
timezone     Etc/UTC
maintenance
  mode       disabled
  ports      enabled
  ```

* Ansible Version
```bash
ubuntu@oob-mgmt-server:~$ ansible --version
ansible [core 2.16.4]
  config file = /etc/ansible/ansible.cfg
  configured module search path = ['/home/ubuntu/.ansible/plugins/modules', '/usr/share/ansible/plugins/modules']
  ansible python module location = /usr/lib/python3/dist-packages/ansible
  ansible collection location = /home/ubuntu/.ansible/collections:/usr/share/ansible/collections
  executable location = /usr/bin/ansible
  python version = 3.10.12 (main, Nov 20 2023, 15:14:05) [GCC 11.4.0] (/usr/bin/python3)
  jinja version = 3.0.3
  libyaml = True
  ```
* Ubuntu Version
```bash
ubuntu@oob-mgmt-server:~$ cat /etc/lsb-release
DISTRIB_ID=Ubuntu
DISTRIB_RELEASE=22.04
DISTRIB_CODENAME=jammy
DISTRIB_DESCRIPTION="Ubuntu 22.04.3 LTS"
  ```
