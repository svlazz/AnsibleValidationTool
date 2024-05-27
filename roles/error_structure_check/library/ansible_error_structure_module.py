import re
from ansible.module_utils.basic import AnsibleModule

def good_practice_search(playbook):
    keywords = ["block:", "rescue:", "always:"] # Structures we're looking for in the playbook
    block_counter = 0
    rescue_counter = 0 # Counters of the structures
    always_counter = 0
    msg = "" # Output message will get

    try:
        with open(playbook, 'r') as code: # We read the playbook
            for line in code:
                for key in keywords: # Checking line after line looking for the keywords
                    if key in line:
                        if key == "block:":
                            block_counter += 1 # If we found a coincidence we add 1 to the counter
                            tasks_inside_block = next(code, None) # If the next line is empty we launch a warning
                            if not tasks_inside_block or not re.search(r'^\s*-\s+name:', tasks_inside_block):
                                msg += f"[WARNING] Block with no task detected \n"
                        elif key == "rescue:":
                            rescue_counter += 1 # We do this with all the strcutures
                            tasks_inside_rescue = next(code, None) # If they are empty we create a warning for each one of the structures
                            if not tasks_inside_rescue or not re.search(r'^\s*-\s+name:', tasks_inside_rescue):
                                msg += f"[WARNING] Rescue with no task detected \n"
                        elif key == "always:":
                            always_counter += 1
                            tasks_inside_always = next(code, None)
                            if not tasks_inside_always or not re.search(r'^\s*-\s+name:', tasks_inside_always):
                                msg += f"[WARNING] Always with no task detected \n"
        # If the block and rescues are the same and both are more than 0 we show an OK report
        if block_counter == rescue_counter and block_counter > 0 and rescue_counter > 0:
            msg += f"[OK] Block: ({block_counter}) Rescue: ({rescue_counter})."
        # If both are 0, then it doesn't have any error control structures
        elif block_counter == 0 and rescue_counter == 0:
            msg += f"[KO] No error control structures found"
        # The third option is a missmatch between the blocks and the rescues, then a KO is reported
        else:
            msg += f"[KO] Block: ({block_counter}) Rescue: ({rescue_counter}) MISSMATCH."

        # Always structures are not mandatory so we only show their presencen in the playbook
        msg += f"\n[INFO] Always: {always_counter} structures where found"

        # Return of the function with TRUE statement and the report message
        return True, msg

    # If the file is not found, we launch an error
    except FileNotFoundError:
        return False, f"\n[ERROR] File '{playbook}' not found"

# Ansible module configuration
def main():
    module = AnsibleModule(
        argument_spec=dict(
            playbook=dict(type='str', required=True)
        )
    )

    playbook_path = module.params['playbook']
    success, result_msg = good_practice_search(playbook_path)

    if success:
        module.exit_json(changed=False, msg=result_msg)
    else:
        module.fail_json(msg=result_msg)

if __name__ == '__main__':
    main()
