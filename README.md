# NVIDIA NVUE Collection


[![CI](https://gitlab.com/nvidia-networking/systems-engineering/nvue/badges/main/pipeline.svg)](https://gitlab.com/nvidia-networking/systems-engineering/nvue/-/pipelines?scope=branches)

The NVIDIA NVUE Collection includes Ansible modules to help you interact with NVIDIA devices managed by NVUE. Currently, it includes the following modules:

| Module | Description |
| ------ | ----------  |
| nvidia.nvue.command | A wrapper around `nv` command line tool with added templating and automated dialog prompting. | 
| nvidia.nvue.api | Send and retrieve NVUE configuration via REST API. | 
| nvidia.nvue.bridge | Bridge configuration via REST API. | 
| nvidia.nvue.config | Revisions via REST API. | 
| nvidia.nvue.evpn | EVPN configuration via REST API. | 
| nvidia.nvue.interface | Interface configuration via REST API. | 
| nvidia.nvue.mlag | MLAG configuration via REST API. | 
| nvidia.nvue.router | Router configuration via REST API. | 
| nvidia.nvue.service | Service configuration via REST API. | 
| nvidia.nvue.system | System configuration via REST API. | 
| nvidia.nvue.vrf | VRF configuration via REST API. | 
| nvidia.nvue.vxlan | VXLAN configuration via REST API. | 

## Ansible version compatibility

Tested with the Ansible Core 2.12 and 2.13

## Python version compatibility

Supports Python 3.8 and higher.

## Installing this collection

### Installing from Ansible Galaxy - Once certification is complete

You can install the NVIDIA NVUE collection with the Ansible Galaxy CLI:

```
ansible-galaxy collection install nvidia.nvue
```

You can also include it in a requirements.yml file and install it with `ansible-galaxy collection install -r requirements.yml`, using the format:

```
---
collections:
  - name: nvidia.nvue
```

### Installing from git

You can install the NVIDIA NVUE collection using the git URL:

```
ansible-galaxy collection install git+https://gitlab.com/nvidia-networking/systems-engineering/nvue.git
```

## Using this collection

You can call modules by their Fully Qualified Collection Name (FQCN), such as `nvidia.nvue.command` or `nvidia.nvue.api`:


```
- name: Set prefix lists
  nvidia.nvue.command: 
    template: |
      {% for rule in rules %}
      set router policy prefix-list PL rule {{ rule.id }} match {{ rule.match }}
      set router policy prefix-list PL rule {{ rule.id }} action {{ rule.action }}
      {% endfor %}
    apply: true
    assume_yes: true
  vars:
    rules:
    - id: 10
      match: 1.1.1.1/32
      action: permit
    - id: 20
      match: 8.8.8.8/32
      action: deny
```

## Examples

For additional usage examples please refer to the `./examples` directory. You can find playbooks that shows some of the common ways of interacting with the collection modules:

| Module | Playbook | 
| ------ | ---------|
| nvidia.nvue.command | [command.yml](./examples/playbooks/command.yml) | 
| nvidia.nvue.api | [api.yml](./examples/playbooks/api.yml) | 
| nvidia.nvue.bridge | [test-bridge.yaml](./examples/playbooks/test-bridge.yaml) | 
| nvidia.nvue.interface | [test-interface.yaml](./examples/playbooks/test-interface.yaml) | 
| nvidia.nvue.config | [test-revision.yaml](./examples/playbooks/test-revision.yaml) | 

## Licensing

GNU General Public License v3.0 or later.

See [LICENSE](./LICENSE) to see the full text.
