from ansible.module_utils.basic import AnsibleModule
import os
import glob

def find_playbooks_tasks_roles_dirs(mainpath):
    """
    Finds directories named 'tasks', 'roles', 'playbooks' and all the yaml in the within the directory tree.
    Args:
        mainpath (str): The root directory to start the search.
    Returns:
        funct_file_paths (dict): Dictionary with all the paths inside the directory given, roles directory, and tasks directory
    """
    funct_file_paths = {'roles': [], 'tasks': [], 'main_dir': [], 'playbooks': []}

    # Search for 'roles' directories
    funct_file_paths['roles'] = glob.glob(os.path.join(mainpath, 'roles'), recursive=True)

    # Search for 'tasks' directories
    funct_file_paths['tasks'] = glob.glob(os.path.join(mainpath, 'tasks'), recursive=True)

    # Search for 'playbooks' directories
    funct_file_paths['playbooks'] = glob.glob(os.path.join(mainpath, 'playbooks'), recursive=True)

    # Search for YAML files in the main directory
    yml_files = glob.glob(os.path.join(mainpath, '*.yml'))
    yaml_files = glob.glob(os.path.join(mainpath, '*.yaml'))

    funct_file_paths['main_dir'].extend(yml_files)
    funct_file_paths['main_dir'].extend(yaml_files)

    return funct_file_paths

def find_playbooks_to_check(paths):
    """
    Finds the playbooks inside the dir we've looked for previously.
    Args:
        path (list): The paths (absolute paths) that may have the playbooks to check.
    Returns:
        playbooks_found (list): List of playbooks found and ready to be checked out.
    """
    playbooks_found = []

    for yaml_path in paths:
        # Search for .yml or .yaml files recursively within the specified path
        yml_files = glob.glob(os.path.join(yaml_path, '*.yml'), recursive=True)
        yaml_files = glob.glob(os.path.join(yaml_path, '*.yaml'), recursive=True)
        
        # Append the absolute file paths to the list
        playbooks_found.extend(yml_files)
        playbooks_found.extend(yaml_files)

    return playbooks_found

def find_main_roles_tasks(path):
    """
    Find the main.yml inside tasks dir of every role.
    The roles dir can contain a requirements.yml which means it imports the roles from other repository
    we will consider the roles from other repositories as OK files
    Args:
        paths (str): Paths of the roles dir.
    Returns:
        main_roles_tasks (list): The main.yml files found inside every role dir.
    """
    main_roles_tasks = []
    
    path_roles = os.path.join(path, "roles")
    for path_roles in glob.iglob(f"{path_roles}/*"):
        if "requirements.yml" in path_roles:
            return main_roles_tasks
        elif "requirements.yaml" in path_roles:
            return main_roles_tasks
            
    main_yml = glob.glob(f"{path}/roles/**/main.yml", recursive=True)
    main_yaml = glob.glob(f"{path}/roles/**/main.yaml", recursive=True)

    main_roles_tasks.extend(main_yml)
    main_roles_tasks.extend(main_yaml)

    return main_roles_tasks

def filter_playbooks(file_paths):
    """
    Filters the yaml files based on playbooks basis, in order to not analyze files that are not playbooks.
    Args:
        file_paths (list): A list of absolute file paths of the yaml files found previously.
    Returns:
        filtered_playbooks (list): A filtered list of file paths that are indeed playbooks.
    """
    filtered_playbooks = []
    playbook_pattern = ["- name:", "tasks:"]

    for file_path in file_paths:
        with open(file_path, 'r') as f:
            lines = f.readlines()
            if any(playbook_pattern[0] in line or playbook_pattern[1] in line for line in lines):
                filtered_playbooks.append(file_path)

    return filtered_playbooks

def main():
    module = AnsibleModule(
        argument_spec=dict(
            main_path=dict(type='str', required=True)
        )
    )

    # Path given as an argument to check
    mainpath = module.params['main_path']
    # Dictionary with paths of the dirs and playbooks inside the main dir
    file_paths = find_playbooks_tasks_roles_dirs(mainpath)
    # Building the returning dictionary
    omega_dict = {'roles':[], 'tasks':[], 'playbooks':[], 'main_dir':[]}
    omega_dict['roles'] = find_main_roles_tasks(mainpath)
    omega_dict['tasks'] = find_playbooks_to_check(file_paths['tasks'])
    omega_dict['playbooks'] = find_playbooks_to_check(file_paths['playbooks'])
    omega_dict['main_dir'] = filter_playbooks(file_paths['main_dir'])

    # Returni the dictionary filtered and ready to be check by the main playbook
    module.exit_json(changed=False, omega_dict=omega_dict)

if __name__ == '__main__':
    main()