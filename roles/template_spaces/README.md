Role Name
=========

This role search for cases where Jinja templates annotation is used without adding space between curly braces and the rest of the expression:

{{expression}} -  BAD
{{ expression }} - GOOD

Requirements
------------

3 global variables must be provided:
  - output_msg: List to store result messages
  - output_sections: Dictionary in whith store the result of the analysis as boolean
  - path: Path of the file to be checked


Role Variables
--------------

  - result_key: key in wich store de result of the check in the output_sections dictionary
  - bad_template_start: Regex to detect bad jija template starting annotation: {{+any non white character
  - bad_template_end: Regex to detect bad jija template ending annotation: }}+any non white character


Dependencies
------------
 

Example Playbook
----------------

Example of usage:

    tasks:
    - name: Check spaces in Jinja template annotations
      ansible.builtin.include_role:
        name: template_spaces 

Be aware of the requeriments explained in the section Requirements

License
-------

BSD

Author Information
------------------

Jose Javier Bailón Ortiz
