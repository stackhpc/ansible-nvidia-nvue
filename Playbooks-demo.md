<!-- AIR:tour -->

# Cumulus Linux Automation Workshop

## NVUE API
NVUE is an object-oriented, schema driven model of a complete Cumulus Linux system (hardware and software) providing a robust API that allows for multiple interfaces to both view (show) and configure (set and unset) any element within a system running the NVUE software.

The NVUE object model definition uses the {{<exlink url="https://github.com/OAI/OpenAPI-Specification" text="OpenAPI specification (OAS)">}}. Like other systems that use OpenAPI, the NVUE OAS schema defines the endpoints (paths) exposed as RESTful APIs. With these REST APIs, you can perform various create, retrieve, update, delete, and eXecute (CRUDX) operations. The OAS schema also describes the API inputs and outputs (data models).

You can use the NVUE object model in the following ways:
- With the NVUE CLI, where you configure, monitor, and manage the Cumulus Linux network elements. The CLI commands translate to their equivalent REST APIs, which Cumulus Linux then runs on the NVUE object model.
- With the NVUE REST API, where you run the GET, PATCH, DELETE, and other REST APIs on the NVUE object model endpoints to configure, monitor, and manage the switch. Because of the large user community and maturity of OAS, you can work with several popular tools and libraries to create client-side bindings to use the NVUE REST API. You can view the NVUE REST API documentation using Swagger {{<exlink url="https://docs.nvidia.com/networking-ethernet-software/cumulus-linux-55/api/index.html" text="here">}}.

## NVUE ANsible Modules
{{<exlink url="https://galaxy.ansible.com/nvidia/nvue" text="The NVIDIA NVUE Collection">}} includes Ansible modules to help you interact with NVIDIA devices managed by NVUE. The modules are developed and validated using Ansible 2.11 and Python 3.6, and are supported on Cumulus Linux 5.x.
The collection includes high-level wrapper modules and object specific modules as listed below:

**High-level modules**
 - nvidia.nvue.command - A wrapper around the NVUE command line tool with added templating and automated dialog prompting.
 - nvidia.nvue.api – A wrapper around the NVUE REST API to send and retrieve NVUE configuration.

**Object specific modules**
 - nvidia.nvue.bridge - Bridge configuration with the REST API.
 - nvidia.nvue.config – Revisions with the REST API
 - nvidia.nvue.evpn - EVPN configuration with the REST API.
 - nvidia.nvue.interface - Interface configuration with the REST API.
 - nvidia.nvue.mlag - MLAG configuration with the REST API.
 - nvidia.nvue.router - Router configuration with the REST API.
 - nvidia.nvue.service - Service configuration with the REST API.
 - nvidia.nvue.system – System configuration with the REST API.
 - nvidia.nvue.vrf - VRF configuration with the REST API.
 - nvidia.nvue.vxlan - VXLAN configuration with the REST API.

For REST API endpoints that are not covered by the object-specific modules or for sub-paths within the object specific modules (for example, `/interface/<id>/qos/roce/counters`), you can leverage the `nvidia.nvue.api` module and specify the endpoint in the `path` parameter.

## Features and Services

This workshop includes demos of the following features:

 * Working with NVUE API
 * Using the Ansible modules - both high level and low level to fetch information
 * Setting up system and interface configurations
 * Static VXLAN
 * Setting up MLAG L2 server redundancy
 * BGP underlay fabric
 * Sample EVPN symmetric configuration

<!-- AIR:page -->

## Demo Topology Information 

### Devices

The workshop uses a simple topology consisting of 3 switches running Cumulus Linux 5.5.1, and 1 Ubuntu server. This can be extended to more complex scenarios.

| __Leaf__ | __Spine__ | __Server__ | 
| -------- | --------- | ---------- | 
| leaf01   | spine01   | server01   | 
| leaf02   |           |            |

<!-- AIR:page -->

### IPAM

#### Hosts

| __Hostname__| __Interface__ | __VRF__ | __VLAN__ | __IP Address__    |
| ---------   | ------------- | ------- | -------- | ----------------- |
| server01    | eth0          | mgmt.   |          | 192.168.200.5/24  |

#### Switches

| __Hostname__| __Interface__ | __VRF__ | __VLAN__ | __IP Address__    |
| ---------   | ------------- | ------- | -------- | ----------------- |
| leaf01      | eth0          | mgmt.   |          | 192.168.200.2/24  |
|             | lo            | default |          | 10.10.10.1/32     |
| leaf02      | eth0          | mgmt.   |          | 192.168.200.3/24  |
|             | lo            | default |          | 10.10.10.2/32     |
| spine01     | eth0          | mgmt.   |          | 192.168.200.4/24  |
|             | lo            | default |          | 10.10.10.101/32   |

### Physical Connectivity

__Hostname__| __Local Port__ | __Remote Port__ | __Remote Device__ |
----------- | -------------- | --------------- | ----------------- |
| leaf01    | swp1           | eth1(uplink)    | server01          |
|           | swp49          | swp49           | leaf02            |
|           | swp50          | swp50           | leaf02            |
|           | swp51          | swp1            | spine01           |
| leaf02    | swp1           | eth2(uplink)    | server01          |
|           | swp49          | swp49           | leaf01            |
|           | swp50          | swp50           | leaf01            |
|           | swp51          | swp2            | spine01           |
<!-- AIR:page -->

## Demo Environment Access

All environment devices access are done via the jump server - `oob-mgmt-server`.

Use the default access credentials to login the `oob-mgmt-server`:
 - Username: ***ubuntu***
 - Password: ***nvidia***

***Note:*** *Once you first login, you must change the default password.*

You can use the web intergrated console or create an SSH service to access the `oob-mgmt-server` using any SSH client.  
For more information and step-by-step instructions, check out NVIDIA Air [Quick Start](https://docs.nvidia.com/networking-ethernet-software/guides/nvidia-air/Quick-Start/) guide.

Once you login the `oob-mgmt-server`, you can access any device in the topology using its hostname.

Login to the servers and firewalls using just the hostname - `ssh <hostname>` (all have the same username - `ubuntu`, which is identical to the `oob-mgmt-server` username).

Default server credentials are:  
 - Username: ***ubuntu***
 - Password: ***nvidia*** 

```bash
ubuntu@oob-mgmt-server:~$ ssh server01
```
Login to the switches using `cumulus` username - `ssh cumulus@<hostname>`. To ease the access, `cumulus` username was set to passwordless authentication from `oob-mgmt-server`. 

```bash
ubuntu@oob-mgmt-server:~$ ssh cumulus@leaf01
```
When logging in from other environment devices, use `ssh cumulus@<ip-address>`.

Default switch credentials are:  
 - Username: ***cumulus***
 - Password: ***CumulusLinux!*** 

<!-- AIR:page -->

## Workshop

### Setup


1. Login to the `oob-mgmt-server`
2. Enter to the `workshop` folder:
```bash
ubuntu@oob-mgmt-server:~$ cd workshop
```
3. Make sure you are on the `cumulus-linux-automation-workshop` branch:
```bash
ubuntu@oob-mgmt-server:~/workshop$ git status | grep cumulus-linux-automation-workshop
On branch cumulus-linux-automation-workshop
Your branch is up to date with 'origin/cumulus-linux-automation-workshop'.
```
*In case you or on other branch, use the `git checkout` command to move the `cumulus-linux-automation-workshop` branch*
```bash
ubuntu@oob-mgmt-server:~/workshop$ git checkout cumulus-linux-automation-workshop
```

### Setting up NVUE API Access

As of the time of this workshop, NVUE REST API is disabled by default. If you want to use any of the object specific modules or the `api` module, you need to enable the NVUE REST API with the following commands on the switch:

```bash
cumulus@switch:~$ sudo ln -s /etc/nginx/sites-{available,enabled}/nvue.conf 
cumulus@switch:~$ sudo sed -i 's/listen localhost:8765 ssl;/listen \[::\]:8765 ipv6only=off ssl;/g' /etc/nginx/sites-available/nvue.conf 
cumulus@switch:~$ sudo systemctl restart nginx
```

You can find a sample playbook that enables the NVUE REST API across all of the switches under `playbooks`.
 
```bash
cumulus@oob-management:~$ ansible-playbook playbooks/enable-nvue-api.yml -i hosts   
```
<!-- AIR:tour -->
