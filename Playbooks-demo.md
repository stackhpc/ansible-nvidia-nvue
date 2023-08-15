<!-- AIR:tour -->

# Cumulus Linux Automation Workshop

## NVUE API
NVUE is an object-oriented, schema driven model of a complete Cumulus Linux system (hardware and software) providing a robust API that allows for multiple interfaces to both view (show) and configure (set and unset) any element within a system running the NVUE software.

The NVUE object model definition uses the [OpenAPI specification(OAS)]("https://github.com/OAI/OpenAPI-Specification"). Like other systems that use OpenAPI, the NVUE OAS schema defines the endpoints (paths) exposed as RESTful APIs. With these REST APIs, you can perform various create, retrieve, update, delete, and eXecute (CRUDX) operations. The OAS schema also describes the API inputs and outputs (data models).

You can use the NVUE object model in the following ways:
- With the NVUE CLI, where you configure, monitor, and manage the Cumulus Linux network elements. The CLI commands translate to their equivalent REST APIs, which Cumulus Linux then runs on the NVUE object model.
- With the NVUE REST API, where you run the GET, PATCH, DELETE, and other REST APIs on the NVUE object model endpoints to configure, monitor, and manage the switch. Because of the large user community and maturity of OAS, you can work with several popular tools and libraries to create client-side bindings to use the NVUE REST API. You can view the NVUE REST API documentation using Swagger [here]("https://docs.nvidia.com/networking-ethernet-software/cumulus-linux-55/api/index.html").

## NVUE Ansible Modules
[The NVIDIA NVUE Collection]("https://galaxy.ansible.com/nvidia/nvue") includes Ansible modules to help you interact with NVIDIA devices managed by NVUE. The modules are developed and validated using Ansible 2.11 and Python 3.6, and are supported on Cumulus Linux 5.x.
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
 * Setting up system, interface, and bridge configurations
 * Setting up MLAG L2 server redundancy
 * BGP underlay fabric

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
 - Password: ***cumulus*** 

<!-- AIR:page -->

## Workshop

### Setup and Installation

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
*In case you are on other branch, use the `git checkout` command to move the `cumulus-linux-automation-workshop` branch*
```bash
ubuntu@oob-mgmt-server:~/workshop$ git checkout cumulus-linux-automation-workshop
```
4. Install the NVIDIA NVUE collection with the Ansible Galaxy CLI:
```bash
ubuntu@oob-mgmt-server:~/workshop$ ansible-galaxy collection install nvidia.nvue
```
5. Verify the installation:
```bash
ubuntu@oob-mgmt-server:~/workshop$ ansible-galaxy collection list | grep nvidia.nvue
nvidia.nvue                   1.0.1
```
6. Verify connectivity to the switches using the `ping` module:
```bash
ubuntu@oob-mgmt-server:~/workshop$ ansible switches -m ping -i hosts
leaf01 | SUCCESS => {
    "ansible_facts": {
        "discovered_interpreter_python": "/usr/bin/python3.7"
    },
    "changed": false,
    "ping": "pong"
}
leaf02 | SUCCESS => {
    "ansible_facts": {
        "discovered_interpreter_python": "/usr/bin/python3.7"
    },
    "changed": false,
    "ping": "pong"
}
spine01 | SUCCESS => {
    "ansible_facts": {
        "discovered_interpreter_python": "/usr/bin/python3.7"
    },
    "changed": false,
    "ping": "pong"
}
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
ubuntu@oob-mgmt-server:~/workshop$ ansible-playbook playbooks/enable-nvue-api.yml -i hosts

PLAY [Enable REST API on all the switches] *************************************

TASK [Gathering Facts] *********************************************************
ok: [leaf01]
ok: [spine01]
ok: [leaf02]

TASK [Create a link to the NVUE Config file] ***********************************
ok: [leaf01]
ok: [leaf02]
ok: [spine01]

TASK [Add the listening port] **************************************************
ok: [spine01]
ok: [leaf02]
ok: [leaf01]

TASK [Flush handlers] **********************************************************

TASK [Flush handlers] **********************************************************

TASK [Flush handlers] **********************************************************

TASK [Test API Connectivity] ***************************************************
ok: [leaf02]
ok: [leaf01]
ok: [spine01]

TASK [debug] *******************************************************************
ok: [leaf01] =>
  apioutput:
    changed: false
    connection: close
    content_length: '521'
    content_type: application/json
    cookies: {}
    cookies_string: ''
    date: Mon, 14 Aug 2023 23:56:40 GMT
    elapsed: 0
    failed: false
    json:
      '1':
        message: Automatic config translation while upgrading to Cumulus Linux 5.5.1
        state: applied
        transition:
          issue: {}
          progress: ''
      applied:
        state: saved
        transition:
          issue: {}
          progress: ''
      empty:
        state: inactive
        transition:
          issue: {}
          progress: ''
      startup:
        state: inactive
        transition:
          issue: {}
          progress: ''
    msg: OK (521 bytes)
    redirected: false
    server: nginx
    status: 200
    strict_transport_security: max-age=31536000; includeSubDomains
    url: https://127.0.0.1:8765/nvue_v1/revision
ok: [leaf02] =>
  apioutput:
    changed: false
    connection: close
    content_length: '413'
    content_type: application/json
    cookies: {}
    cookies_string: ''
    date: Mon, 14 Aug 2023 23:56:40 GMT
    elapsed: 0
    failed: false
    json:
      '1':
        message: Automatic config translation while upgrading to Cumulus Linux 5.5.1
        state: applied
        transition:
          issue: {}
          progress: ''
      empty:
        state: inactive
        transition:
          issue: {}
          progress: ''
      startup:
        state: inactive
        transition:
          issue: {}
          progress: ''
    msg: OK (413 bytes)
    redirected: false
    server: nginx
    status: 200
    strict_transport_security: max-age=31536000; includeSubDomains
    url: https://127.0.0.1:8765/nvue_v1/revision
ok: [spine01] =>
  apioutput:
    changed: false
    connection: close
    content_length: '413'
    content_type: application/json
    cookies: {}
    cookies_string: ''
    date: Mon, 14 Aug 2023 23:56:40 GMT
    elapsed: 0
    failed: false
    json:
      '1':
        message: Automatic config translation while upgrading to Cumulus Linux 5.5.1
        state: applied
        transition:
          issue: {}
          progress: ''
      empty:
        state: inactive
        transition:
          issue: {}
          progress: ''
      startup:
        state: inactive
        transition:
          issue: {}
          progress: ''
    msg: OK (413 bytes)
    redirected: false
    server: nginx
    status: 200
    strict_transport_security: max-age=31536000; includeSubDomains
    url: https://127.0.0.1:8765/nvue_v1/revision

PLAY RECAP *********************************************************************
leaf01                     : ok=5    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
leaf02                     : ok=5    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
spine01                    : ok=5    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
```

<!-- AIR:page -->

### Running your first NVUE API Call

You can use any tool that can run API calls. In this workshop, the sample implementation uses curl. First, SSH into leaf01 followed by running the curl call:
```bash
ubuntu@oob-mgmt-server:~/workshop$ ssh cumulus@leaf01
Linux leaf01 5.10.0-cl-1-amd64 #1 SMP Debian 5.10.162-1+cl5.5.1u6 (2023-05-19) x86_64

Welcome to NVIDIA Cumulus VX (TM)

NVIDIA Cumulus VX (TM) is a community supported virtual appliance designed
for experiencing, testing and prototyping NVIDIA Cumulus' latest technology.
For any questions or technical support, visit our community site at:
https://www.nvidia.com/en-us/support

The registered trademark Linux (R) is used pursuant to a sublicense from LMI,
the exclusive licensee of Linus Torvalds, owner of the mark on a world-wide
basis.
Last login: Mon Aug 14 23:56:40 2023 from 192.168.200.1
cumulus@leaf01:mgmt:~$ curl -k -u cumulus:cumulus 'https://127.0.0.1:8765/nvue_v1/?rev=applied'
{
  "acl": {},
  "bridge": {
    "domain": {
      "br_default": {
        "ageing": 1800,
        "encap": "802.1Q",
        "mac-address": "auto",
        "multicast": {
          "snooping": {
            "enable": "on",
            "querier": {
              "enable": "off"
            }
          }
        },
        "stp": {
          "priority": 32768,
          "state": {
            "up": {}
          }
        },
        "type": "vlan-aware",
        "untagged": 1,
        "vlan": {
          "1": {
            "multicast": {
              "snooping": {
                "querier": {
                  "source-ip": "0.0.0.0"
                }
              }
            },
            "ptp": {
              "enable": "off"
            },
            "vni": {}
          }
        },
        "vlan-vni-offset": 0
      }
    }
  },
  "evpn": {
    "enable": "off"
  },
  "header": {
    "model": "VX",
    "nvue-api-version": "nvue_v1",
    "rev-id": 1.0,
    "version": "Cumulus Linux 5.5.1"
  },
  "interface": {
    "eth0": {
      "acl": {},
      "ip": {
        "address": {
          "dhcp": {}
        },
        "gateway": {},
        "ipv4": {
          "forward": "off"
        },
        "ipv6": {
          "enable": "on",
          "forward": "off"
        },
        "vrf": "mgmt"
      },
      "link": {
        "auto-negotiate": "on",
        "duplex": "full",
        "fec": "auto",
        "mtu": 9216,
        "speed": "auto",
        "state": {
          "up": {}
        }
      },
      "type": "eth"
    },
    "lo": {
      "ip": {
        "address": {},
        "igmp": {
          "enable": "off"
        },
        "ipv4": {
          "forward": "on"
        },
        "ipv6": {
          "enable": "on",
          "forward": "on"
        },
        "vrf": "default"
      },
      "router": {
        "adaptive-routing": {
          "enable": "off"
        },
        "ospf": {
          "enable": "off"
        },
        "ospf6": {
          "enable": "off"
        },
        "pim": {
          "enable": "off"
        }
      },
      "type": "loopback"
    }
  },
  "mlag": {
    "enable": "off"
  },
  "nve": {
    "vxlan": {
      "enable": "off"
    }
  },
  "qos": {
    "advance-buffer-config": {
      "default-global": {
        "egress-lossy-buffer": {
          "multicast-switch-priority": {
            "0": {
              "service-pool": "0"
            },
            "1": {
              "service-pool": "0"
            },
            "2": {
              "service-pool": "0"
            },
            "3": {
              "service-pool": "0"
            },
            "4": {
              "service-pool": "0"
            },
            "5": {
              "service-pool": "0"
            },
            "6": {
              "service-pool": "0"
            },
            "7": {
              "service-pool": "0"
            }
          },
          "traffic-class": {
            "0": {
              "service-pool": "0"
            },
            "1": {
              "service-pool": "0"
            },
            "2": {
              "service-pool": "0"
            },
            "3": {
              "service-pool": "0"
            },
            "4": {
              "service-pool": "0"
            },
            "5": {
              "service-pool": "0"
            },
            "6": {
              "service-pool": "0"
            },
            "7": {
              "service-pool": "0"
            }
          }
        },
        "egress-pool": {
          "0": {
            "memory-percent": 100,
            "mode": "dynamic"
          }
        },
        "ingress-lossy-buffer": {
          "priority-group": {
            "bulk": {
              "service-pool": "0",
              "switch-priority": {
                "0": {},
                "1": {},
                "2": {},
                "3": {},
                "4": {},
                "5": {},
                "6": {},
                "7": {}
              }
            }
          }
        },
        "ingress-pool": {
          "0": {
            "memory-percent": 100,
            "mode": "dynamic"
          }
        }
      }
    },
    "congestion-control": {
      "default-global": {
        "traffic-class": {
          "0": {
            "ecn": "enable",
            "max-threshold": 1500000,
            "min-threshold": 150000,
            "probability": 100,
            "red": "disable"
          }
        }
      }
    },
    "egress-queue-mapping": {
      "default-global": {
        "switch-priority": {
          "0": {
            "traffic-class": 0
          },
          "1": {
            "traffic-class": 1
          },
          "2": {
            "traffic-class": 2
          },
          "3": {
            "traffic-class": 3
          },
          "4": {
            "traffic-class": 4
          },
          "5": {
            "traffic-class": 5
          },
          "6": {
            "traffic-class": 6
          },
          "7": {
            "traffic-class": 7
          }
        }
      }
    },
    "egress-scheduler": {
      "default-global": {
        "traffic-class": {
          "0": {
            "bw-percent": 12,
            "mode": "dwrr"
          },
          "1": {
            "bw-percent": 13,
            "mode": "dwrr"
          },
          "2": {
            "bw-percent": 12,
            "mode": "dwrr"
          },
          "3": {
            "bw-percent": 13,
            "mode": "dwrr"
          },
          "4": {
            "bw-percent": 12,
            "mode": "dwrr"
          },
          "5": {
            "bw-percent": 13,
            "mode": "dwrr"
          },
          "6": {
            "bw-percent": 12,
            "mode": "dwrr"
          },
          "7": {
            "bw-percent": 13,
            "mode": "dwrr"
          }
        }
      }
    },
    "egress-shaper": {},
    "link-pause": {},
    "mapping": {
      "default-global": {
        "pcp": {
          "0": {
            "switch-priority": 0
          },
          "1": {
            "switch-priority": 1
          },
          "2": {
            "switch-priority": 2
          },
          "3": {
            "switch-priority": 3
          },
          "4": {
            "switch-priority": 4
          },
          "5": {
            "switch-priority": 5
          },
          "6": {
            "switch-priority": 6
          },
          "7": {
            "switch-priority": 7
          }
        },
        "port-default-sp": 0,
        "trust": "l2"
      }
    },
    "pfc": {},
    "remark": {
      "default-global": {}
    },
    "roce": {
      "enable": "off"
    },
    "traffic-pool": {
      "default-lossy": {
        "memory-percent": 100,
        "switch-priority": {
          "0": {},
          "1": {},
          "2": {},
          "3": {},
          "4": {},
          "5": {},
          "6": {},
          "7": {}
        }
      }
    }
  },
  "router": {
    "adaptive-routing": {
      "enable": "off"
    },
    "bgp": {
      "enable": "off"
    },
    "igmp": {
      "enable": "off"
    },
    "nexthop": {
      "group": {}
    },
    "ospf": {
      "enable": "off"
    },
    "ospf6": {
      "enable": "off"
    },
    "pbr": {
      "enable": "off"
    },
    "pim": {
      "enable": "off"
    },
    "policy": {
      "as-path-list": {},
      "community-list": {},
      "ext-community-list": {},
      "large-community-list": {},
      "prefix-list": {},
      "route-map": {}
    },
    "ptm": {
      "enable": "off"
    },
    "vrr": {
      "enable": "off"
    },
    "vrrp": {
      "enable": "off"
    }
  },
  "service": {
    "dhcp-relay": {},
    "dhcp-relay6": {},
    "dhcp-server": {},
    "dhcp-server6": {},
    "dns": {},
    "lldp": {
      "dot1-tlv": "off",
      "lldp-med-inventory-tlv": "off",
      "mode": "default",
      "tx-hold-multiplier": 4,
      "tx-interval": 30
    },
    "ntp": {},
    "ptp": {
      "1": {
        "acceptable-master": {},
        "domain": 0,
        "enable": "off",
        "ip-dscp": 46,
        "logging-level": "info",
        "monitor": {
          "max-offset-threshold": 50,
          "max-timestamp-entries": 100,
          "max-violation-log-entries": 4,
          "max-violation-log-sets": 2,
          "min-offset-threshold": -50,
          "path-delay-threshold": 200,
          "violation-log-interval": 1
        },
        "priority1": 128,
        "priority2": 128,
        "profile": {
          "default-1588": {
            "announce-interval": 1,
            "announce-timeout": 3,
            "delay-mechanism": "end-to-end",
            "delay-req-interval": 0,
            "domain": 0,
            "priority1": 128,
            "priority2": 128,
            "profile-type": "ieee-1588",
            "sync-interval": 0,
            "transport": "ipv4"
          },
          "default-itu-8275-1": {
            "announce-interval": -3,
            "announce-timeout": 3,
            "delay-mechanism": "end-to-end",
            "delay-req-interval": -4,
            "domain": 24,
            "local-priority": 128,
            "priority1": 128,
            "priority2": 128,
            "profile-type": "itu-g-8275-1",
            "sync-interval": -4,
            "transport": "802.3"
          },
          "default-itu-8275-2": {
            "announce-interval": 0,
            "announce-timeout": 3,
            "delay-mechanism": "end-to-end",
            "delay-req-interval": -6,
            "domain": 44,
            "local-priority": 128,
            "priority1": 128,
            "priority2": 128,
            "profile-type": "itu-g-8275-2",
            "sync-interval": -6,
            "transport": "ipv4"
          }
        },
        "unicast-master": {}
      }
    },
    "snmp-server": {
      "enable": "off"
    },
    "synce": {
      "enable": "off"
    },
    "syslog": {}
  },
  "system": {
    "aaa": {
      "authentication-order": {},
      "tacacs": {
        "enable": "off"
      },
      "user": {}
    },
    "acl": {
      "mode": "atomic"
    },
    "config": {
      "apply": {
        "ignore": {},
        "overwrite": "all"
      },
      "auto-save": {
        "enable": "off"
      },
      "snippet": {}
    },
    "control-plane": {
      "acl": {},
      "policer": {},
      "trap": {}
    },
    "counter": {
      "polling-interval": {
        "logical-interface": 5,
        "physical-interface": 2
      }
    },
    "forwarding": {
      "ecmp-hash": {
        "destination-ip": "on",
        "destination-port": "on",
        "gtp-teid": "off",
        "ingress-interface": "off",
        "inner-destination-ip": "off",
        "inner-destination-port": "off",
        "inner-ip-protocol": "off",
        "inner-ipv6-label": "off",
        "inner-source-ip": "off",
        "inner-source-port": "off",
        "ip-protocol": "on",
        "ipv6-label": "on",
        "source-ip": "on",
        "source-port": "on"
      },
      "host-route-preference": "route",
      "lag-hash": {
        "destination-ip": "on",
        "destination-mac": "on",
        "destination-port": "on",
        "ether-type": "on",
        "gtp-teid": "off",
        "ip-protocol": "on",
        "source-ip": "on",
        "source-mac": "on",
        "source-port": "on",
        "vlan": "on"
      },
      "programming": {
        "log-level": "info"
      }
    },
    "global": {
      "anycast-id": "none",
      "anycast-mac": "none",
      "fabric-id": 1,
      "fabric-mac": "none",
      "l3svd": {
        "enable": "off"
      },
      "reserved": {
        "routing-table": {
          "pbr": {
            "begin": 10000,
            "end": 4294966272
          }
        },
        "vlan": {
          "internal": {
            "range": "3725-3999"
          },
          "l3-vni-vlan": {
            "begin": 4000,
            "end": 4064
          }
        }
      },
      "system-mac": "auto"
    },
    "hostname": "cumulus",
    "port-mirror": {
      "session": {}
    },
    "reboot": {
      "mode": "cold"
    },
    "wjh": {
      "enable": "off"
    }
  },
  "vrf": {
    "default": {
      "evpn": {
        "enable": "off"
      },
      "loopback": {
        "ip": {
          "address": {
            "127.0.0.1/8": {},
            "::1/128": {}
          }
        }
      },
      "ptp": {
        "enable": "on"
      },
      "router": {
        "bgp": {
          "enable": "off"
        },
        "nexthop-tracking": {},
        "ospf": {
          "enable": "off"
        },
        "ospf6": {
          "enable": "off"
        },
        "pim": {
          "enable": "off"
        },
        "rib": {},
        "static": {}
      },
      "table": "auto"
    },
    "mgmt": {
      "evpn": {
        "enable": "off"
      },
      "loopback": {
        "ip": {
          "address": {
            "127.0.0.1/8": {},
            "::1/128": {}
          }
        }
      },
      "ptp": {
        "enable": "on"
      },
      "router": {
        "bgp": {
          "enable": "off"
        },
        "nexthop-tracking": {},
        "ospf": {
          "enable": "off"
        },
        "ospf6": {
          "enable": "off"
        },
        "rib": {},
        "static": {}
      },
      "table": "auto"
    }
  }
}
cumulus@leaf01:mgmt:~$ exit
logout
Connection to leaf01 closed.
ubuntu@oob-mgmt-server:~/workshop$
```
<!-- AIR:page -->

## Sample playbooks
1. The `gather-config.yml` uses the high-level `api` module to fetch the root configuration and the object-level `interface` module to fetch interface configuration.
```bash
ubuntu@oob-mgmt-server:~/workshop$ ansible-playbook playbooks/gather-config.yml -i hosts
PLAY [NVUE API] ****************************************************************

TASK [Get the current config] **************************************************
ok: [leaf01]

TASK [Print current config] ****************************************************
ok: [leaf01] =>
  msg:
    changed: false
    failed: false
    message:
      acl: {}
      bridge:
        domain:
          br_default:
            ageing: 1800
            encap: 802.1Q
            mac-address: auto
            multicast:
              snooping:
                enable: 'on'
                querier:
                  enable: 'off'
            stp:
              priority: 32768
              state:
                up: {}
            type: vlan-aware
            untagged: 1
            vlan:
              '1':
                multicast:
                  snooping:
                    querier:
                      source-ip: 0.0.0.0
                ptp:
                  enable: 'off'
                vni: {}
            vlan-vni-offset: 0
      evpn:
        enable: 'off'
      header:
        model: VX
        nvue-api-version: nvue_v1
        rev-id: 1.0
        version: Cumulus Linux 5.5.1
      interface:
        eth0:
          acl: {}
          ip:
            address:
              dhcp: {}
            gateway: {}
            ipv4:
              forward: 'off'
            ipv6:
              enable: 'on'
              forward: 'off'
            vrf: mgmt
          link:
            auto-negotiate: 'on'
            duplex: full
            fec: auto
            mtu: 9216
            speed: auto
            state:
              up: {}
          type: eth
        lo:
          ip:
            address: {}
            igmp:
              enable: 'off'
            ipv4:
              forward: 'on'
            ipv6:
              enable: 'on'
              forward: 'on'
            vrf: default
          router:
            adaptive-routing:
              enable: 'off'
            ospf:
              enable: 'off'
            ospf6:
              enable: 'off'
            pim:
              enable: 'off'
          type: loopback
      mlag:
        enable: 'off'
      nve:
        vxlan:
          enable: 'off'
      qos:
        advance-buffer-config:
          default-global:
            egress-lossy-buffer:
              multicast-switch-priority:
                '0':
                  service-pool: '0'
                '1':
                  service-pool: '0'
                '2':
                  service-pool: '0'
                '3':
                  service-pool: '0'
                '4':
                  service-pool: '0'
                '5':
                  service-pool: '0'
                '6':
                  service-pool: '0'
                '7':
                  service-pool: '0'
              traffic-class:
                '0':
                  service-pool: '0'
                '1':
                  service-pool: '0'
                '2':
                  service-pool: '0'
                '3':
                  service-pool: '0'
                '4':
                  service-pool: '0'
                '5':
                  service-pool: '0'
                '6':
                  service-pool: '0'
                '7':
                  service-pool: '0'
            egress-pool:
              '0':
                memory-percent: 100
                mode: dynamic
            ingress-lossy-buffer:
              priority-group:
                bulk:
                  service-pool: '0'
                  switch-priority:
                    '0': {}
                    '1': {}
                    '2': {}
                    '3': {}
                    '4': {}
                    '5': {}
                    '6': {}
                    '7': {}
            ingress-pool:
              '0':
                memory-percent: 100
                mode: dynamic
        congestion-control:
          default-global:
            traffic-class:
              '0':
                ecn: enable
                max-threshold: 1500000
                min-threshold: 150000
                probability: 100
                red: disable
        egress-queue-mapping:
          default-global:
            switch-priority:
              '0':
                traffic-class: 0
              '1':
                traffic-class: 1
              '2':
                traffic-class: 2
              '3':
                traffic-class: 3
              '4':
                traffic-class: 4
              '5':
                traffic-class: 5
              '6':
                traffic-class: 6
              '7':
                traffic-class: 7
        egress-scheduler:
          default-global:
            traffic-class:
              '0':
                bw-percent: 12
                mode: dwrr
              '1':
                bw-percent: 13
                mode: dwrr
              '2':
                bw-percent: 12
                mode: dwrr
              '3':
                bw-percent: 13
                mode: dwrr
              '4':
                bw-percent: 12
                mode: dwrr
              '5':
                bw-percent: 13
                mode: dwrr
              '6':
                bw-percent: 12
                mode: dwrr
              '7':
                bw-percent: 13
                mode: dwrr
        egress-shaper: {}
        link-pause: {}
        mapping:
          default-global:
            pcp:
              '0':
                switch-priority: 0
              '1':
                switch-priority: 1
              '2':
                switch-priority: 2
              '3':
                switch-priority: 3
              '4':
                switch-priority: 4
              '5':
                switch-priority: 5
              '6':
                switch-priority: 6
              '7':
                switch-priority: 7
            port-default-sp: 0
            trust: l2
        pfc: {}
        remark:
          default-global: {}
        roce:
          enable: 'off'
        traffic-pool:
          default-lossy:
            memory-percent: 100
            switch-priority:
              '0': {}
              '1': {}
              '2': {}
              '3': {}
              '4': {}
              '5': {}
              '6': {}
              '7': {}
      router:
        adaptive-routing:
          enable: 'off'
        bgp:
          enable: 'off'
        igmp:
          enable: 'off'
        nexthop:
          group: {}
        ospf:
          enable: 'off'
        ospf6:
          enable: 'off'
        pbr:
          enable: 'off'
        pim:
          enable: 'off'
        policy:
          as-path-list: {}
          community-list: {}
          ext-community-list: {}
          large-community-list: {}
          prefix-list: {}
          route-map: {}
        ptm:
          enable: 'off'
        vrr:
          enable: 'off'
        vrrp:
          enable: 'off'
      service:
        dhcp-relay: {}
        dhcp-relay6: {}
        dhcp-server: {}
        dhcp-server6: {}
        dns: {}
        lldp:
          dot1-tlv: 'off'
          lldp-med-inventory-tlv: 'off'
          mode: default
          tx-hold-multiplier: 4
          tx-interval: 30
        ntp: {}
        ptp:
          '1':
            acceptable-master: {}
            domain: 0
            enable: 'off'
            ip-dscp: 46
            logging-level: info
            monitor:
              max-offset-threshold: 50
              max-timestamp-entries: 100
              max-violation-log-entries: 4
              max-violation-log-sets: 2
              min-offset-threshold: -50
              path-delay-threshold: 200
              violation-log-interval: 1
            priority1: 128
            priority2: 128
            profile:
              default-1588:
                announce-interval: 1
                announce-timeout: 3
                delay-mechanism: end-to-end
                delay-req-interval: 0
                domain: 0
                priority1: 128
                priority2: 128
                profile-type: ieee-1588
                sync-interval: 0
                transport: ipv4
              default-itu-8275-1:
                announce-interval: -3
                announce-timeout: 3
                delay-mechanism: end-to-end
                delay-req-interval: -4
                domain: 24
                local-priority: 128
                priority1: 128
                priority2: 128
                profile-type: itu-g-8275-1
                sync-interval: -4
                transport: '802.3'
              default-itu-8275-2:
                announce-interval: 0
                announce-timeout: 3
                delay-mechanism: end-to-end
                delay-req-interval: -6
                domain: 44
                local-priority: 128
                priority1: 128
                priority2: 128
                profile-type: itu-g-8275-2
                sync-interval: -6
                transport: ipv4
            unicast-master: {}
        snmp-server:
          enable: 'off'
        synce:
          enable: 'off'
        syslog: {}
      system:
        aaa:
          authentication-order: {}
          tacacs:
            enable: 'off'
          user: {}
        acl:
          mode: atomic
        config:
          apply:
            ignore: {}
            overwrite: all
          auto-save:
            enable: 'off'
          snippet: {}
        control-plane:
          acl: {}
          policer: {}
          trap: {}
        counter:
          polling-interval:
            logical-interface: 5
            physical-interface: 2
        forwarding:
          ecmp-hash:
            destination-ip: 'on'
            destination-port: 'on'
            gtp-teid: 'off'
            ingress-interface: 'off'
            inner-destination-ip: 'off'
            inner-destination-port: 'off'
            inner-ip-protocol: 'off'
            inner-ipv6-label: 'off'
            inner-source-ip: 'off'
            inner-source-port: 'off'
            ip-protocol: 'on'
            ipv6-label: 'on'
            source-ip: 'on'
            source-port: 'on'
          host-route-preference: route
          lag-hash:
            destination-ip: 'on'
            destination-mac: 'on'
            destination-port: 'on'
            ether-type: 'on'
            gtp-teid: 'off'
            ip-protocol: 'on'
            source-ip: 'on'
            source-mac: 'on'
            source-port: 'on'
            vlan: 'on'
          programming:
            log-level: info
        global:
          anycast-id: none
          anycast-mac: none
          fabric-id: 1
          fabric-mac: none
          l3svd:
            enable: 'off'
          reserved:
            routing-table:
              pbr:
                begin: 10000
                end: 4294966272
            vlan:
              internal:
                range: 3725-3999
              l3-vni-vlan:
                begin: 4000
                end: 4064
          system-mac: auto
        hostname: cumulus
        port-mirror:
          session: {}
        reboot:
          mode: cold
        wjh:
          enable: 'off'
      vrf:
        default:
          evpn:
            enable: 'off'
          loopback:
            ip:
              address:
                127.0.0.1/8: {}
                ::1/128: {}
          ptp:
            enable: 'on'
          router:
            bgp:
              enable: 'off'
            nexthop-tracking: {}
            ospf:
              enable: 'off'
            ospf6:
              enable: 'off'
            pim:
              enable: 'off'
            rib: {}
            static: {}
          table: auto
        mgmt:
          evpn:
            enable: 'off'
          loopback:
            ip:
              address:
                127.0.0.1/8: {}
                ::1/128: {}
          ptp:
            enable: 'on'
          router:
            bgp:
              enable: 'off'
            nexthop-tracking: {}
            ospf:
              enable: 'off'
            ospf6:
              enable: 'off'
            rib: {}
            static: {}
          table: auto

TASK [Get the current interface config] ****************************************
ok: [leaf01]

TASK [Print current interface] *************************************************
ok: [leaf01] =>
  msg:
    changed: false
    failed: false
    message:
      eth0:
        acl: {}
        ip:
          address:
            dhcp: {}
          gateway: {}
          ipv4:
            forward: 'off'
          ipv6:
            enable: 'on'
            forward: 'off'
          vrf: mgmt
        link:
          auto-negotiate: 'on'
          duplex: full
          fec: auto
          mtu: 9216
          speed: auto
          state:
            up: {}
        type: eth
      lo:
        ip:
          address: {}
          igmp:
            enable: 'off'
          ipv4:
            forward: 'on'
          ipv6:
            enable: 'on'
            forward: 'on'
          vrf: default
        router:
          adaptive-routing:
            enable: 'off'
          ospf:
            enable: 'off'
          ospf6:
            enable: 'off'
          pim:
            enable: 'off'
        type: loopback

PLAY RECAP *********************************************************************
leaf01                     : ok=4    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
```
2. The `api.yml` uses the high-level `api` module to setup a pre-login message on `leaf01`.
```bash
ubuntu@oob-mgmt-server:~/workshop$ ansible-playbook -v playbooks/api.yml -i hosts
```
3. The `interface.yml` uses the object-level `interface` module to setup interfaces on `leaf01`.
```bash
ubuntu@oob-mgmt-server:~/workshop$ ansible-playbook -v playbooks/interface.yml -i hosts
```
4. The `bridge.yml` uses the object-level `bridge` module to setup bridge domain `br_default` on `leaf01`.
```bash
ubuntu@oob-mgmt-server:~/workshop$ ansible-playbook -v playbooks/bridge.yml -i hosts
```
<!-- AIR:page -->

### BGP and MLAG
1. Clear the configuration on the switches to avoid any MLAG configuration inconsistencies:
```bash
ubuntu@oob-mgmt-server:~/workshop$ ansible-playbook -v playbooks/clean-switches.yml -i hosts
```
2. To setup MLAG between the 2 leaf switches, you can use the playbooks in the `playbooks/MLAG/` directory:
```bash
ubuntu@oob-mgmt-server:~/workshop$ ansible-playbook -v playbooks/MLAG/mlag-leaf01.yml -i hosts
ubuntu@oob-mgmt-server:~/workshop$ ansible-playbook -v playbooks/MLAG/mlag-leaf02.yml -i hosts
ubuntu@oob-mgmt-server:~/workshop$ ansible-playbook -v playbooks/MLAG/mlag-spine01.yml -i hosts
```
3. Verify MLAG operational state:
```bash
cumulus@leaf01:mgmt:~$ nv show mlag
                operational                applied
--------------  -------------------------  -----------------
enable          on                         on
debug           off                        off
init-delay      100                        100
mac-address     44:38:39:be:ef:aa          44:38:39:BE:EF:AA
peer-ip         fe80::4ab0:2dff:fe3a:abc3  linklocal
priority        1000                       1000
[backup]        10.10.10.2                 10.10.10.2
backup-active   False
backup-reason
local-id        48:b0:2d:b1:bd:bd
local-role      secondary
peer-alive      True
peer-id         48:b0:2d:3a:ab:c3
peer-interface  peerlink.4094
peer-priority   1000
peer-role       primary
```

Verify MLAG interfaces state:
```bash
cumulus@leaf01:mgmt:~$ net show clag
The peer is alive
     Our Priority, ID, and Role: 1000 48:b0:2d:b1:bd:bd secondary
    Peer Priority, ID, and Role: 1000 48:b0:2d:3a:ab:c3 primary
          Peer Interface and IP: peerlink.4094 fe80::4ab0:2dff:fe3a:abc3 (linklocal)
                      Backup IP: 10.10.10.2 (inactive)
                     System MAC: 44:38:39:be:ef:aa

Global Inconsistencies
Consistency Params            Conflicts
----------------------        ------------------
        peerlink-vlans        allowed vlans on peerlink mismatch between clag peers

CLAG Interfaces
Our Interface      Peer Interface     CLAG Id   Conflicts              Proto-Down Reason
----------------   ----------------   -------   --------------------   -----------------
           bond1   -                  1         vlan mismatch on       -
                                                clag interface
                                                between clag
                                                peers,some allowed
                                                vlans on clag
                                                interface are not
                                                allowed on the
                                                peerlink
```
Verify that no configuration conflicts exist between the two MLAG peers:
```bash
cumulus@leaf01:mgmt:~$ nv show mlag consistency-checker global
Parameter         LocalValue        PeerValue          Conflict          Summary
---------------…  ---------------…  ----------------…  ---------------…  -------
anycast-ip        -                 -                  -
bridge-priority   32768             32768              -
bridge-stp        on                on                 -
bridge-type       vlan-aware        vlan-aware         -
clag-pkg-version  1.6.0-cl5.5.0u4   1.6.0-cl5.5.0u4    -
clag-protocol-v…  1.6.0             1.6.0              -
peer-ip           fe80::4ab0:2dff…  fe80::4ab0:2dff:…  -
peerlink-master   br_default        NOT-SYNCED         -
peerlink-mtu      9216              9216               -
peerlink-native…  1                 1                  -
peerlink-vlans    1, 10             1, 10              -
redirect2-enable  yes               yes                -
system-mac        44:38:39:be:ef:…  44:38:39:be:ef:aa  -
```
```bash
cumulus@leaf01:mgmt:~$ nv show interface --view=mlag-cc
Interface  Parameter        LocalValue       PeerValue         Conflict
---------  --------------…  --------------…  ---------------…  ----------------…
bond1      bridge-learning  yes              yes               -
           clag-id          1                1                 -
           lacp-actor-mac   44:38:39:be:ef…  44:38:39:be:ef:…  -
           lacp-partner-m…  00:00:00:00:00…  00:00:00:00:00:…  -
           master           br_default       NOT-SYNCED        -
           mtu              9216             9216              -
           native-vlan      1                1                 -
           vlan-id          1, 10            1, 10             -
```
On any MLAG configuration change, Cumulus Linux automatically validates the corresponding parameters on both MLAG peers and takes action based on the type of conflict it sees. For every conflict, the `/var/log/clagd.log` file records a log message. For more information about MLAG consistency-checker and other MLAG validations, check out the [MLAG Troubleshooting](https://docs.nvidia.com/networking-ethernet-software/cumulus-linux-55/Layer-2/Multi-Chassis-Link-Aggregation-MLAG/#troubleshooting) section in Cumulus Linux documentation.

4. To setup BGP, you can use the playbooks in the `playbooks/BGP/` directory:
```bash
cumulus@leaf01:mgmt:~$ exit
ubuntu@oob-mgmt-server:~/workshop$ ansible-playbook -v playbooks/BGP/bgp-leaf01.yml -i hosts
ubuntu@oob-mgmt-server:~/workshop$ ansible-playbook -v playbooks/BGP/bgp-leaf02.yml -i hosts
ubuntu@oob-mgmt-server:~/workshop$ ansible-playbook -v playbooks/BGP/bgp-spine01.yml -i hosts
```
5. Verify BGP peerings:
```bash
cumulus@leaf01:mgmt:~$ net show bgp summary
cumulus@leaf01:mgmt:~$ net show bgp summary
show bgp ipv4 unicast summary
=============================
BGP router identifier 10.10.10.1, local AS number 65101 vrf-id 0
BGP table version 4
RIB entries 7, using 1400 bytes of memory
Peers 2, using 46 KiB of memory

Neighbor        V         AS   MsgRcvd   MsgSent   TblVer  InQ OutQ  Up/Down State/PfxRcd   PfxSnt
spine01(swp51)  4      65199        12        13        0    0    0 00:00:17            2        4
swp52           4          0         0         0        0    0    0    never         Idle        0

Total number of neighbors 2


show bgp ipv6 unicast summary
=============================
% No BGP neighbors found


show bgp l2vpn evpn summary
===========================
% No BGP neighbors found
cumulus@leaf01:mgmt:~$ nv show vrf default router bgp neighbor

AS - Remote Autonomous System, Afi-Safi - Address family, GracefulRestart -
Graceful restart end of rib notification, PfxSent - Transmitted prefix counter,
PfxRcvd - Recieved prefix counter

Neighbor  AS     State        Uptime    ResetTime  ResetReason                   MsgRcvd  MsgSent  Afi-Safi      GracefulRestart  PfxSent  PfxRcvd
--------  -----  -----------  --------  ---------  ---------------------------…  -------  -------  ------------  ---------------  -------  -------
swp51     65199  established  00:04:06  300000     No AFI/SAFI activated for     89       90       ipv4-unicast  rx-eof-rib: on   4        2
                                                   peer
                                                                                                                 tx-eof-rib: on
                                                                                                   ipv6-unicast
                                                                                                   l2vpn-evpn
swp52            idle                   300000     Waiting for Peer IPv6 LLA     0        0        ipv4-unicast  rx-eof-rib: off
                                                                                                                 tx-eof-rib: off
                                                                                                   ipv6-unicast
                                                                                                   l2vpn-evpn

```
<!-- AIR:page -->
## Additional Resources
- [NVUE modules on Gtilab](https://gitlab.com/nvidia-networking/systems-engineering/nvue/-/tree/main/examples/playbooks)
- [NVUE modules on Galaxy](https://galaxy.ansible.com/nvidia/nvue)
- [NVUE modules on Automation Hub](https://console.redhat.com/ansible/automation-hub/repo/published/nvidia/nvue/)
- [Data Center Network Automation Quick Start Guide](https://docs.nvidia.com/networking-ethernet-software/guides/Data-Center-Network-Automation-Quick-Start-Guide/)
- [Production Ready Automation Guide](https://docs.nvidia.com/networking-ethernet-software/guides/production-ready-automation/)
- [Automating Data Center Networks with NVIDIA Cumulus Linux](https://developer.nvidia.com/blog/automating-data-center-networks-with-nvidia-cumulus-linux/)
<!-- AIR:tour -->
