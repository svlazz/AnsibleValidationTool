Role variable_duplication
=========

This role detects duplication of variables inside a playbook. It warns about what variables are defined at least twice on the same dictionary or
variables defined twice in register or set_fact sentences.

Requirements
------------

3 global variables must be provided:
  - output_msg: List to store result messages
  - output_sections: Dictionary in whith store the result of the analysis as boolean
  - path: Path of the file to be checked

Role Variables
--------------

  - path: The playbook to be analyzed
  - result_key: key in wich store de result of the check in the output_sections dictionary

  
Dependencies
------------

None

Example Playbook
----------------

Example of usage:

    tasks:
    - name: Check spaces in Jinja template annotations
      ansible.builtin.include_role:
        name: variable_duplication

Be aware of the requeriments explained in the section Requirements

License
-------

BSD

Author Information
------------------

Jose Javier Bailón Ortiz.
