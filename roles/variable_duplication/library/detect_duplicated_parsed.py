#!/usr/bin/python

import json
import yaml

from ansible.module_utils.basic import AnsibleModule
from pathlib import Path
DOCUMENTATION = '''
---
module: detect_duplicated_parsed.py
short_description: Search for duplicated variables in vars register and set_fact sentences
'''

EXAMPLES = '''
- name: Search for duplicated variables in register and set_fact sentences
  required_duplicated:
    file_content: "yaml file parsed"
'''


class CheckRegisterDuplicated(object):

    def __init__(self, module):
        self.msg =""
        self.module = module
        self.yaml_content = module.params['yaml_content']
        self.failed = False
        self.variables={}
        self.recurrentAnalyzer(self.yaml_content)
        self.analyzeResult()


    def recurrentAnalyzer(self,branch):
        if type(branch) == list:
            for elemento in branch:
                self.recurrentAnalyzer(elemento)
        elif type(branch) == dict:
            for key, value in branch.items():
                #if the element is vars
                if (type(value) ==list):
                    self.recurrentAnalyzer(value)
                if(key=="vars"):
                    for keyvar, valuevar in value.items():
                        self.addVariableCount(keyvar)
                elif ("register" in key):
                    self.addVariableCount(value)
                elif ("set_fact" in key and type(value) == dict):
                        for keyfact, valuefact in value.items():
                            if ("cacheable" not in keyfact):
                                self.addVariableCount(keyfact)             

    def addVariableCount(self, value):
            if (value in self.variables):
                self.variables[value] += 1
            else:
                self.variables[value] = 1

    def analyzeResult(self):
        self.failed = False
        
        errorMsg = "[KO] Duplicated variables found in register/set_fact: "

        for key, value in self.variables.items():
            if (value > 1):
                self.failed = True
                errorMsg += key +", "

        if self.failed:
            self.msg += errorMsg
        else:
            self.msg = "[OK] No variables duplicated in register/set_fact"

def main():
    module = AnsibleModule(
        argument_spec=dict(
            yaml_content=dict(type='list', required=True),
        ),
        supports_check_mode=True,
    )
  
    checker = CheckRegisterDuplicated(module)

    result = {}

    result['msg'] = checker.msg
    result['failed'] = checker.failed
    result['changed'] = False
    module.exit_json(**result)

if __name__ == '__main__':
    main()