Playbook check
========================
This playbook checks if other playbook follows some rules. 

## Rules checked
-------------
 - **variable_duplication**: Checks if the playbook overrides some variable using same variable name twice or more in a _vars_ section, a _set_fact_ task or a _register sentence_
 - **template_spaces**: Checks if the playbook uses Jinja annotations with a white space next to the  _{{_ or _}}_ meaning that _{{expression}}_ is bad formated and _{{ expression }}_ is well formated
 - **check_snake_case**: Check that the playbook name and the variable names inside the playbook follow the snake_case format.
 - **syntax_check**: Checks that the indentation of the file content is correct and the modules called on it are correct and exist.
 - **filename_check**: Checks that the playbook name follows some rules.
 - **readmefile_check**: Checks if exists a readme file on the playbook directory and if it follows some rules.
 - **namescheck**: Checks tasks for either a lack of defined name or improper formatting (less than 10 characters and not starting with an uppercase letter or starting with '[' and next character not being upper case).
 - **password check**: Check that the passwords given are not written in plain text and are encrypted by sha, vault or base64. 
 - **infinite loop check**: Check that the playbook does not contain any potential infinite loops. 
 -  **error_structure_check**: Check the presence of desirable control error structure in order to provide a vision of a good formed playbook. Detects blocks, rescues and always, also detailed if any of them is missing tasks inside.

## Requeriments
------------
-	Git
- Ansible v 2.16.x or latest
-	Ansible-lint 24.2.x or latest
-	Python v 3.1.x or latest
-	Yaml module for Python
-	Github/BitBucket access


## Execution
---------
In order to execute this playbook a **repository path** parameter must be provided during execution pointing to the repository url to be checked:

`ansible-playbook playbook_check.yml -e "repo_clone_path=<URL TO REPOSITORY>"`

By default you dont need to declare more parameters, but is possible to moddify the logs and clone:
 - log_path `(defaults to /tmp/dir_logs)`
 - repo_clone_path `(defaults to /tmp/repo_clone)`
 
`ansible-playbook playbook_check.yml -e "repo_clone_path=<URL TO REPOSITORY> log_path=<NEW PATH TO LOGS DIR> repo_clone_path=<NEW PATH TO LOCAL REPO DIR>"`

## Result
------
The final result is shown as a list of direcories in **/tmp/dir_logs** containin the following structure:


