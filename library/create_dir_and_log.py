from ansible.module_utils.basic import AnsibleModule
import os
import datetime
import shutil

def log_directory_exists(path, name):
    """
    Checks if the specified directory exists. If it exists, creates a subdirectory inside with a name including the date.
    If not, it creates the directory and then the subdirectory with the specified name.

    Args:
        path (str): The path to the directory.
        name (str): The name given to the new subdirectory.

    Returns:
        new_dir (str): The path of the new subdirectory created to be used for logs.
    """
    if os.path.exists(path):
        time = datetime.datetime.now()
        formatted_datetime = time.strftime("%Y-%m-%d_%H-%M-%S")
        new_dir = os.path.join(path, f"{formatted_datetime}_{name}")
        os.makedirs(new_dir)
    else:
        os.makedirs(path)
        time = datetime.datetime.now()
        formatted_datetime = time.strftime("%Y-%m-%d_%H-%M-%S")
        new_dir = os.path.join(path, f"{formatted_datetime}_{name}")
        os.makedirs(new_dir)

    return new_dir

def create_log(log_dir, log_name, log_list):
    """
    Creates a log file to be filled with the status report of the playbook.

    Args:
        log_dir (str): Path to the log directory.
        log_name (str): Name for this log.
        log_list (list): List of items to write to the log.

    Returns:
        log_path (str): Path of the new log file created.
    """
    log_date = datetime.date.today()
    log_name = f"{log_date}_{log_name}.log"
    log_path = os.path.join(log_dir, log_name)

    with open(log_path, "w") as log:
        for item in log_list:
            log.write(f"{item}\n")

    return log_path

def modify_directory_name(log_created, output_values):
    """
    Modifies the directory name based on the status of output_values and moves files accordingly.

    Args:
        log_created (str): Path to the log directory.
        output_values (dict): A dictionary containing status values (True/False).

    Returns:
        new_dir_path (str): Path of the new log file created.
    """
    # Get the directory path from the log_created argument
    dir_path = os.path.dirname(log_created)

    # Get the parent directory
    parent_dir = os.path.dirname(dir_path)

    # Create a new directory name based on the status of output_values
    new_dir_name = "OK_" + os.path.basename(dir_path)

    # Check if any status in output_values is False
    for status in output_values.values():
        if not status:
            new_dir_name = "KO_" + os.path.basename(dir_path)
            break

    # Create the new directory path
    new_dir_path = os.path.join(parent_dir, new_dir_name)

    # Create the new directory
    os.makedirs(new_dir_path, exist_ok=True)

    # Move all files from the old directory to the new one
    for filename in os.listdir(dir_path):
        shutil.move(os.path.join(dir_path, filename), new_dir_path)

    # Remove the old directory
    os.rmdir(dir_path)

    return new_dir_path



def main():
    module = AnsibleModule(
        argument_spec=dict(
            main_path=dict(type='str', required=True),
            output_log=dict(type='list', required=True),
            output_values=dict(type='dict', requiered=True)
        )
    )

    # Variables taken from the playbook
    main_path = module.params['main_path']
    output_log = module.params['output_log']
    output_values = module.params['output_values']

    log_name = os.path.basename(main_path) # Name of the playbook for the log to be created
    dir_path = "/tmp/dir_logs" # Main dir for logs
    dir_name = "dir_check" # Name that will be received by every subdirectory created and will contain the logs

    dir_log_created = log_directory_exists(dir_path, dir_name)
    log_created = create_log(dir_log_created, log_name, output_log)
    modify_directory_name(log_created, output_values)

    module.exit_json(changed=False)

if __name__ == '__main__':
    main()
