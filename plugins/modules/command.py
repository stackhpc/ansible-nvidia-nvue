#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2022, NVIDIA <nvidia.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

# Original design: https://github.com/ansible-collections/community.network/blob/main/plugins/modules/network/cumulus/nclu.py

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
author: Nvidia NBU Team (@nvidia-nbu)
module: command
short_description: Run NVUE commands on Nvidia Cumulus Linux
description: This is my longer description explaining my test module.
options:
    commands:
        description: A list of strings containing the net commands to run.
        required: false
        type: list
        elements: str
    template:
        description: A single, multi-line string with jinja2 formatting. This string will be broken and executed by lines.
        required: false
        type: str
    apply:
        description: When true, performs a "nvue apply" at the end of the block.
        required: false
        default: false
        type: bool
    assume_yes:
        description: When true, adds a "-y" flag to the "nvue apply" command.
        required: false
        default: false
        type: bool
    detach:
        description: When true, performs `nv config detach` before this block.
        required: false
        default: false
        type: bool
    atomic:
        description: When true, equivalent to both `apply` and `detach` being true.
        required: false
        default: false
        type: bool
    save:
        description: Saves NVUE configuration to disk
        required: false
        default: false
        type: bool
    msg:
        description: Add message to apply
        required: false
        default: None
        type: str
"""

EXAMPLES = r"""
# Pass in a single command
- name: Set system pre-login message
  nvidia.nvue.command:
    commands:
    - set system message pre-login "{{ MSG }}"
    atomic: true
    assume_yes: true
  vars:
    MSG: WARNING

# Using command templating
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
"""

RETURN = r"""
# These are examples of possible return values, and in general should use other names for return values.
changed:
  description: whether a configuration was changed
  returned: always
  type: bool
  sample: true
message:
    description: a message returned from the supplied NVUE commands
    type: str
    returned: always
    sample: "Failed on line \"set system m123ssage pre-login \"WARNING\"\"\nInvalid Command: set system m123ssage pre-login WARNING\n"
"""

from ansible.module_utils.basic import AnsibleModule


def run_nvue_cmd(module, command, errmsg=None):
    """Run a command, catch any nvue errors"""
    prefix = "nv "
    # Check if user passed on an "nv " while passing on the command to the module and strip it
    if command.startswith(prefix):
        command = command[len(prefix):]
    (_rc, output, _err) = module.run_command("/usr/bin/nv %s" % command)
    if _rc or "error" in _err.lower():
        msg = "\n".join((x for x in [errmsg, _err] if x))
        module.fail_json(msg=msg)
    return str(output)


def run_nvue(module):
    changed = False
    atomic = module.params.get("atomic")

    commands = []

    cmds = module.params.get("commands", None)
    cmd_str = module.params.get("template", None)
    if cmds:
        commands = cmds
    elif cmd_str:
        commands = cmd_str.splitlines()

    abort_cmd = "config detach"
    if module.params.get("detach") or atomic:
        run_nvue_cmd(module, abort_cmd)

    output_lines = []

    for line in commands:
        if line.strip():
            output_lines += [
                run_nvue_cmd(module, line.strip(), 'Failed on line "%s"' % line)
            ]

    output = "\n".join(output_lines)

    diff = {}
    # TODO: add diff implementation

    apply_cmd = "config apply"
    apply = module.params.get("apply")
    if module.params.get("assume_yes"):
        apply_cmd += " --assume-yes"

    msg = module.params.get("msg")
    if msg:
        apply_cmd += " --message " + msg

    if apply or atomic:
        result = run_nvue_cmd(module, apply_cmd)
        output += result
        changed = True

    save_cmd = "config save"
    save = module.params.get("save")
    if save:
        result = run_nvue_cmd(module, save_cmd)
        output += result
        changed = True

    return changed, output, diff


def run_module():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        commands=dict(type="list", required=False, elements='str'),
        template=dict(type="str", required=False),
        apply=dict(type="bool", required=False, default=False),
        assume_yes=dict(type="bool", required=False, default=False),
        detach=dict(type="bool", required=False, default=False),
        atomic=dict(type="bool", required=False, default=False),
        save=dict(type="bool", required=False, default=False),
        msg=dict(type="str", required=False, default=False),
    )

    # seed the result dict in the object
    # we primarily care about changed and state
    # changed is if this module effectively modified the target
    # state will include any data that you want your module to pass back
    # for consumption, for example, in a subsequent task
    result = dict(changed=False, original_message="", message="")

    # the AnsibleModule object will be our abstraction working with Ansible
    # this includes instantiation, a couple of common attr would be the
    # args/params passed to the execution, as well as if the module
    # supports check mode
    module = AnsibleModule(
        argument_spec=module_args,
        mutually_exclusive=[
            ("commands", "template"),
            ("apply", "atomic"),
            ("detach", "atomic"),
        ],
        supports_check_mode=True,
    )

    # if the user is working with this module in only check mode we do not
    # want to make any changes to the environment, just return the current
    # state with no modifications
    if module.check_mode:
        module_args["apply"] = False
        module.exit_json(**result)

    changed, output, diff = run_nvue(module)

    # manipulate or modify the state as needed (this is going to be the
    # part where your module will do what it needs to do)
    # result['original_message'] = module.params['name']
    result["message"] = output
    result["diff"] = diff

    # use whatever logic you need to determine whether or not this module
    # made any modifications to your target
    # if module.params['new']:
    #    result['changed'] = changed

    # during the execution of the module, if there is an exception or a
    # conditional state that effectively causes a failure, run
    # AnsibleModule.fail_json() to pass in the message and the result
    # if module.params['name'] == 'fail me':
    #    module.fail_json(msg='You requested this to fail', **result)

    # in the event of a successful module execution, you will want to
    # simple AnsibleModule.exit_json(), passing the key/value results
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
