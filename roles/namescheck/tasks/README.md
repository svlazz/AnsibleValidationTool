Playbook check
========================
This playbook checks if other playbook follows some rules.

Rules checked
-------------
 - **variable_duplication**: Checks if the playbook overrides some variable using same variable name twice or more in a _vars_ section, a _set_fact_ task or a _register sentence_
 - **template_spaces**: Checks if the playbook uses Jinja annotations with a white space next to the  _{{_ or _}}_ meaning that _{{expression}}_ is bad formated and _{{ expression }}_ is well formated
 - **check_snake_case_version**: Check that the playbook name and the variable names inside the playbook follow the snake_case format.
 - **syntax_check**: Checks that the playbook name is in lower case, doesnt contains special chars and ends in .yml or yml. Also, checks if the syntax of the playbook itself is correct and that exists a README file in the playbook directory.
 - **namescheck**: Checks tasks for either a lack of defined name or improper formatting (less than 10 characters and not starting with an uppercase letter or starting with '[' and next character not being upper case).
 - **password check**: Check that the passwords given are not written in plain text and are encrypted by sha, vault or base64. 
 - **infinite loop check**: Check that the playbook does not contain any potential infinite loops. 
 -  **error_structure_check**: Check the presence of desirable control error structure in order to provide a vision of a good formed playbook. Detects blocks, rescues and always, also detailed if any of them is missing tasks inside.


Execution
---------
In order to execute this playbook a **path** parameter must be provided during execution pointing to the playbook to be checked:

`ansible-playbook playbook_check.yml -e "path=<ABSOLUTE_PATH_TO_A_PLAYBOOK>"`


Result
------
The final result is shown as JSON objects with a list of messages pointing to possible problems in the checked playbok and a dictionary with boolean values indicating if a specific check has been passed. True means the specific check was pased ok. False means that the playbook break the checked rule. Finally a overall status is showed  if all checks passed OK or not.
