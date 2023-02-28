#!/usr/bin/python

# Copyright: (c) 2022 NVIDIA
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: config

short_description: This is a Cumulus Linux revision module

version_added: "1.0.0"

description: This is a Cumulus Linux module to initialize/apply a revision.

options:
    filters:
        description: Filters used while fetching information about revision
        type: dict
        elements: dict
        suboptions:
            omit:
                description: Drop any JSON properties matched by an omit pattern from the response.
                required: false
                type: list
            include:
                description: Only include JSON properties matched by an include pattern in the response.
                required: false
                type: list
    state:
        description: Defines the action to be taken
        required: true
        type: string
        choices:
            - gathered
            - new
            - apply
    revid:
        description: The default is to query the operational state. However, this parameter can be used to query desired state on configuration branches,
                     such as startup and applied. This could be a branch name, tag name or specific commit.
        required: false
        type: str

author:
    - Krishna Vasudevan
'''

EXAMPLES = r'''
- name: Fetch all revisions
  nvidia.nvue.config:
    state: gathered
- name: Fetch specific revision
  nvidia.nvue.config:
    state: gathered
    revid: changeset/cumulus/2021-11-02_16.09.18_5Z1K
- name: Initialize a revision
  nvidia.nvue.config:
    state: new
- name: Apply a revision
  nvidia.nvue.config:
    state: apply
    revid: changeset/cumulus/2021-11-02_16.09.18_5Z1K
'''

RETURN = r'''

'''

import json
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.connection import Connection
from ansible.module_utils.six import string_types
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.utils import (
    dict_diff,
)


def main():
    # define paremeters to connect to the CL instance
    provider_spec = dict(
        cl_url=dict(type='str', required=True),
        cl_port=dict(type='str', required=True),
        cl_username=dict(type='str', required=True),
        cl_password=dict(type='str', required=True, no_log=True)
    )

    # define supported filters for the endpoint
    filter_spec = dict(
        omit=dict(type='list', required=False),
        include=dict(type='list', required=False)
    )

    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        provider=dict(type='dict', required=True, options=provider_spec),
        state=dict(type='str', required=True, choices=['new', 'apply', 'gathered']),
        revid=dict(type='str', required=False),
        filters=dict(type='dict', required=False, options=filter_spec)
    )

    required_if = [
        ('state', 'apply', ['revid'])
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

    # if the user is working with this module in only check mode we do not
    # want to make any changes to the environment, just return the current
    # state with no modifications
    if module.check_mode:
        module.exit_json(**result)

    path = "revision/"
    if module.params["state"] == "gathered":
        operation = "get"
        if module.params["revid"] is not None:
            path = path + module.params["revid"]
    else:
        operation = module.params["state"]
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

    connection = Connection(module._socket_path)
    response = connection.send_request(data, path, operation, force=force, wait=wait, revid=revid)
    if operation == "set" and response:
        result["changed"] = True
    result["message"] = response

    module.exit_json(**result)

    # if the user is working with this module in only check mode we do not
    # want to make any changes to the environment, just return the current
    # state with no modifications
    if module.check_mode:
        module.exit_json(**result)

    

    result = run(endpoint, module.params)

    # during the execution of the module, if there is an exception or a
    # conditional state that effectively causes a failure, run
    # AnsibleModule.fail_json() to pass in the message and the result
    if result["status_code"] != 200:
        module.fail_json(msg='Your request failed', **result)

    # in the event of a successful module execution, you will want to
    # simple AnsibleModule.exit_json(), passing the key/value results
    module.exit_json(**result)


if __name__ == '__main__':
    main()
