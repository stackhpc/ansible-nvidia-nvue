from __future__ import (absolute_import, division, print_function)
from time import sleep
__metaclass__ = type
# This code is part of Ansible, but is an independent component.
# This particular file snippet, and this file snippet only, is BSD licensed.
# Modules you write using this snippet, which is embedded dynamically by Ansible
# still belong to the author of the module, and may assign their own license
# to the complete work.
#
# Copyright © 2022 NVIDIA
#
# Redistribution and use in source and binary forms, with or without modification,
# are permitted provided that the following conditions are met:
#
#    * Redistributions of source code must retain the above copyright
#      notice, this list of conditions and the following disclaimer.
#    * Redistributions in binary form must reproduce the above copyright notice,
#      this list of conditions and the following disclaimer in the documentation
#      and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
# IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE
# USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

import requests
import urllib.parse
import base64
import json

def new_revision(arguments):
# Function to initiate a revision/changeset and retrieve a revision ID
    result={}
    revision_url = arguments["base_url"] + "revision"
    payload={}
    response = requests.request("POST", revision_url, headers=arguments["headers"], data=payload, verify=False)
    revid = urllib.parse.quote_plus(list(response.json().keys())[0])
    result["revid"] = urllib.parse.quote_plus(list(response.json().keys())[0])
    result["status_code"] = response.status_code
    return result

def apply_revision(arguments,revid):
# Function to apply a revision/changeset
    revision_url = arguments["base_url"] + "revision"
    payload={"state": "apply","auto-prompt":{"ays": "ays_yes"}}
    requests.request("PATCH", revision_url + "/" + revid, headers=arguments["headers"], data=json.dumps(payload), verify=False)
    result = get_api("revision/" + revid,arguments)
    return result

def get_api(object,arguments):
# function to fetch information fromt he API endpoint
    result={"changed":False}
    endpoint_url = arguments["base_url"] + object

    # implemented for revid - need to implement for include and omit
    if arguments["filters"] is not None:
        if arguments["filters"]["rev"] is not None:
            endpoint_url = endpoint_url + "?rev=" + arguments["filters"]["rev"]

    payload={}
    response = requests.request("GET", endpoint_url, headers=arguments["headers"], data=payload, verify=False)

    result["api_results"] = response.json()
    result["status_code"] = response.status_code

    return result

def normalize_keys(config):
    """
    Function normalize all the keys - Replace all underscore seperated keys with hyphen seperated keys. For example, mac_flooding is replaced with mac-flooding
    """
    new_config = {}
    if isinstance(config,dict):
        if not bool(config):
            return new_config
        for key,value in config.items():
            new_config[key.replace("_","-")] = normalize_keys(value)
    elif isinstance(config,list):
        if not len(config):
            return new_config
        new_config = []
        for items in config:
            new_config.append(normalize_keys(items))
    else:
        return config
    return new_config

def normalize_spec(config):
    """ 
    Function to normalize config parameters
    Remove the input value id and make it a dictionary with the rest of the values. For example, in bridges, we take id as an input:
    config:
        - id: br_default
          untagged: 1
          type: vlan-aware
          vlan:
            - id: 10
              vni:
                - id: 10
            - id: 20
              vni: 
                - id: 20
    This needs to be converted for the API as below:
    {
        'br_default': 
        {
            'type': 'vlan-aware', 
            'untagged': '1', 
            'vlan': 
            {
                '10': 
                {
                    'vni': 
                    {
                        '10': {}
                    }
                }, 
                '20': 
                {
                    'vni': 
                    {
                        '20': {}
                    }
                }
            }
        }
    }

    """
    new_config = {}
    if isinstance(config,dict):
        if not bool(config):
            return new_config
        for key,value in config.items():
            new_config[key] = normalize_spec(value)
    elif isinstance(config,list):
        if not len(config):
            return new_config
        for item in config:
            if("id" in item):
                id = item.pop('id')
                new_config[id] = item
                for key,value in item.items():
                    #if isinstance(value,list):
                    new_config[id][key]=normalize_spec(value)
    else:
        return config
    return new_config

def patch_api(object,arguments):
# function to update configuration at the API endpoint
    result={"changed":False}
    # Create a new revision ID, if not already initiated using a previous step in the playbook
    if("revid" not in arguments):
        revid = new_revision(arguments)["revid"]
    else:
        revid = arguments["revid"]
    config = normalize_keys(arguments["config"])
    payload = normalize_spec(config)
    
    endpoint_url = arguments["base_url"] + object + "?rev=" + revid
    response = requests.request("PATCH", endpoint_url, headers=arguments["headers"], data=json.dumps(payload), verify=False)

    # If revision not already initiated using a previous step in the playbook, apply changes right away
    if("revid" not in arguments):
        apply_revision(arguments,revid)
        # wait for the revision changes to get applied - modify to monitor status of revision
        sleep(5)
        result = get_api(object,arguments)
        result["changed"]=True
    else:
        # Since no changes have been applied yet, return the response from the PATCH operation
        result["api_results"] = response.json()
        result["status_code"] = response.status_code
    return result

def del_api(object,arguments):
# function to delete configuration at the API endpoint
    result={"changed":False}
    # Create a new revision ID, if not already initiated using a previous step in the playbook
    if(revid in arguments):
        revid = new_revision(arguments)["revid"]
    else:
        revid = arguments["revid"]

    # Check logic 
    endpoint_url =  arguments["base_url"] + object + "?rev=" + revid
    response = requests.request("DELETE", endpoint_url, headers=arguments["header"], verify=False)
    
    # If revision not already initiated using a previous step in the playbook, apply changes right away
    if(revid not in arguments):
       apply_revision(arguments,revid)

     # wait for the revision changes to get applied - modify to monitor status of revision
    sleep(5)

    # since the endpoint contains the ID fof the object that was reconfigured, extract the base object by splitting at the first /
    result = get_api( object.split('/')[0],arguments)
    result["changed"]=True
    return result

def run(object,pb_arguments):
    # Based on values in arguments passed from the playbook, set common variables in arguments
    arguments = {}
    arguments["base_url"] = "https://" + pb_arguments["provider"]["cl_url"] + ":" + pb_arguments["provider"]["cl_port"] + "/nvue_v1/"
    arguments["endpoint_auth"] = base64.b64encode(str.encode(pb_arguments["provider"]["cl_username"] + ":" + pb_arguments["provider"]["cl_password"])).decode()
    arguments["headers"] = {
        'Authorization': 'Basic ' + arguments["endpoint_auth"],
        'Content-Type': 'application/json',
        'Accept': 'application/json',
    }
    if('filters' in pb_arguments):
        arguments["filters"] = pb_arguments["filters"]
    # Check if config details is passed as an argument
    if('config' in pb_arguments):
        arguments["config"] = pb_arguments["config"]
    # Check if a revision has already been initiated and passed as an argument
    if('revid' in pb_arguments):
        arguments["revid"] = pb_arguments["revid"]

    # Check if this is a revision request
    if object == "revision":
        if pb_arguments["state"] == "new":
            result = new_revision(arguments)
        elif pb_arguments["state"] == "apply":
            result = apply_revision(arguments,arguments["revid"])

    # check request state - Gathered => Fetch data; Patched => Update data; Deleted => Delete data
    if pb_arguments["state"] == "gathered":
        result = get_api(object,arguments)
    elif pb_arguments["state"] == "merged":
        result = patch_api(object,arguments)
    elif pb_arguments["state"] == "deleted":
        result = del_api(object,arguments)

    return result
  