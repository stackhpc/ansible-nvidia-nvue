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
        description: Defines the action to be taken.
        required: true
        type: str
        choices:
            - gathered
            - new
            - apply
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
    revid:
        description: The default is to query the operational state. However, this parameter can be used to query desired state on configuration branches,
                     such as startup and applied. This could be a branch name, tag name or specific commit.
        required: false
        type: str

author:
    - Nvidia NBU Team (@nvidia-nbu)
    - Krishna Vasudevan (@krisvasudevan)
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

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.connection import Connection


def main():
    # define supported filters for the endpoint
    filter_spec = dict(
        omit=dict(type='list', elements='str', required=False),
        include=dict(type='list', elements='str', required=False)
    )

    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        force=dict(type='bool', required=False, default=False),
        wait=dict(type="int", required=False, default=0),
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

    path = "revision"
    if module.params["state"] == "gathered":
        operation = "get"
        if module.params["revid"] is not None:
            path = path + "/" + module.params["revid"]
    else:
        operation = module.params["state"]
    force = module.params["force"]
    wait = module.params["wait"]
    revid = module.params["revid"]

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
    response = connection.send_request("", path, operation, force=force, wait=wait, revid=revid)
    if operation == "set" and response:
        result["changed"] = True
    result["revid"] = response

    module.exit_json(**result)


if __name__ == '__main__':
    main()
