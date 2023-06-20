#!/usr/bin/python

# Copyright: (c) 2022 NVIDIA
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
import json
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.connection import Connection
from ansible.module_utils.six import string_types

__metaclass__ = type

DOCUMENTATION = r'''
---
module: system

short_description: This is the Cumulus Linux system module

version_added: "1.0.0"

description: This is a Cumulus Linux module to interact with the system-wide properties.

options:
    filters:
        description: Filters used while fetching information about the system
        type: dict
        elements: dict
        suboptions:
            rev:
                description: The default is to query the operational state. However, this parameter can be used to query desired state on configuration
                             branches, such as startup and applied. This could be a branch name, tag name or specific commit.
                required: false
                type: str
            omit:
                description: Drop any JSON properties matched by an omit pattern from the response.
                required: false
                type: list
            include:
                description: Only include JSON properties matched by an include pattern in the response.
                required: false
                type: list
    data:
        description: Provided configuration
        type: dict
        elements: dict
        suboptions:
            hostname:
                description: Static hostname for the switch.
                required: false
                type: str
                default: cumulus
            timezone:
                description: System Time Zone.
                required: false
                type: str
            message:
                description: System pre-login and post-login messages.
                required: false
                type: dict
                elements: dict
                suboptions:
                    pre_login:
                        description: Configure pre-login banner.
                        required: false
                        type: str
                    post_login:
                        description: Configure post-login message of the day.
                        required: false
                        type: str
    state:
        description: Defines the action to be taken
        required: true
        type: str
        choices:
            - gathered
            - deleted
            - merged
    force:
        description: When true, replies "yes" to NVUE prompts.
        required: false
        default: false
        type: bool
    wait:
        description: How long to poll for "merged/deleted" operation results.
        required: false
        default: 0
        type: int

author:
    - Krishna Vasudevan
'''

EXAMPLES = r'''
# Pass in a message
- name: Display the system configuration
  nvidia.nvue.system:
    state: gathered
'''

RETURN = r'''
# These are examples of possible return values, and in general should use other names for return values.

'''


def main():
    # define supported filters for the endpoint
    # since router object doesn't support querying the operational state, we will default to applied state
    filter_spec = dict(
        rev=dict(type='str', required=False, default='applied'),
        omit=dict(type='list', required=False),
        include=dict(type='list', required=False)
    )

    # define the system spec - used for creation/modification
    system_spec = dict(
        hostname=dict(type='str', required=False, default='cumulus'),
        timezone=dict(type='str', required=False),
        message=dict(type='dict', required=False, options=dict(
            pre_login=dict(type='str', required=False),
            post_login=dict(type='str', required=False)
        ))
    )

    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        force=dict(type='bool', required=False, default=False),
        wait=dict(type="int", required=False, default=0),
        revid=dict(type='str', required=False),
        state=dict(type='str', required=True, choices=["gathered", "deleted", "merged"]),
        data=dict(type='dict', required=False, options=system_spec),
        filters=dict(type='dict', required=False, options=filter_spec)
    )

    required_if = [
        ["operation", "merged", ["data"]],
    ]
    # the AnsibleModule object will be our abstraction working with Ansible
    # this includes instantiation, a couple of common attr would be the
    # args/params passed to the execution, as well as if the module
    # supports check mode
    module = AnsibleModule(
        argument_spec=module_args,
        required_if=required_if,
        supports_check_mode=True
    )

    path = "system"
    if module.params["state"] == "gathered":
        operation = "get"
    else:
        operation = "set"
    data = module.params["data"]
    force = module.params["force"]
    wait = module.params["wait"]
    revid = module.params["revid"]

    if isinstance(data, string_types):
        data = json.loads(data)

    warnings = list()
    result = {"changed": False, "warnings": warnings}

    running = None
    commit = not module.check_mode

    # if the user is working with this module in only check mode we do not
    # want to make any changes to the environment, just return the current
    # state with no modifications
    if module.check_mode:
        module.exit_json(**result)

    connection = Connection(module._socket_path)
    response = connection.send_request(data, path, operation, force=force, wait=wait, revid=revid)
    if operation == "set" and response:
        result["changed"] = True
    result["message"] = response

    module.exit_json(**result)


if __name__ == '__main__':
    main()