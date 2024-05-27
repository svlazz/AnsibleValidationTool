#!/usr/bin/python
from ansible.module_utils.basic import AnsibleModule
import yaml
from pathlib import Path

class NamesChecker():

    def __init__(self, contenido):
        self.tasks_without_name = 0
        self.tasks_with_invalid_name = 0
        self.failed = False
        self.fail_info1 = "Tasks at lines: "
        self.fail_info2 = "Tasks at lines: "
        self.msg_final = "[KO] "
        self.lineas = []
        self.contenido = contenido

        playbook_content = self.load_file()
        
        # Si el playbook no esta vacio
        if playbook_content is not None:
            tasks = []
            
            if not isinstance(playbook_content, list):
                if 'tasks' in playbook_content:
                    tasks.extend(playbook_content['tasks'])
                
                if 'handlers' in playbook_content:
                    tasks.extend(playbook_content['handlers'])

                if 'block' in playbook_content:
                    tasks.extend(playbook_content['block'])

                if 'always' in playbook_content:
                    tasks.extend(playbook_content['always'])

                if 'rescue' in playbook_content:
                    tasks.extend(playbook_content['rescue'])
            
            else:
                for item in playbook_content:
                    if isinstance(item, dict):
                        if 'tasks' in item:
                            tasks.extend(item['tasks'])
                        if 'pre_tasks' in item:
                            tasks.extend(item['pre_tasks'])
                        if 'post_tasks' in item:
                            tasks.extend(item['post_tasks'])
                        if 'handlers' in item:
                            tasks.extend(item['handlers'])

                if len(tasks) == 0:
                    tasks = playbook_content

            self.check_tasks(tasks)
            self.set_fail_msg()

    def load_file(self):
            # El replace porque puedes poner block sin -, es necesario que lo tenga para iterar bien sobre las tareas
            self.contenido = self.contenido.replace('  block:', '- block:')
            self.contenido = self.contenido.replace('- tasks:', 'tasks:')
            self.contenido = self.contenido.replace('\r\n', '\n')
            return yaml.safe_load(self.contenido)

    def check_tasks(self, tasks):
        # Comprobar que hay tasks para iterar sobre ellas (para evitar que falle si se encuentra un block o rescue sin nada dentro)
        if tasks is not None:
            for task in tasks:

                # Si no tiene nombre y no es un block
                if ('name' not in task or task['name'] is None) and 'block' not in task:
                    self.tasks_without_name += 1
                    #self.failed = True
                    # yaml dump para pasar la tarea (el diccionario) a formato tal cual esta en el yml, importante sort_keys false para que lo ponga tal cual
                    task_text = yaml.dump(task, sort_keys=False, allow_unicode=True, default_flow_style=False, width=1000)
                    # se busca en el archivo la linea en la que aparece la tarea
                    self.find_task_block(task_text,"nameless")

                # Si el nombre no esta en formato correcto
                if 'name' in task and isinstance(task['name'], str):
                    name = task['name']
                    if len(name) < 10 or (name[0] != '[' and not name[0].isupper()) or (name[0] == '[' and not name[1].isupper()):
                        self.tasks_with_invalid_name += 1
                        #self.failed = True
                        task_text = yaml.dump(task, sort_keys=False, allow_unicode=True, default_flow_style=False, width=1000)
                        self.find_task_block(task_text, "invalid_name")

                if 'block' in task:
                    self.check_tasks(task['block'])
                
                if 'rescue' in task:  
                    self.check_tasks(task['rescue'])

                if 'always' in task:  
                    self.check_tasks(task['always'])

    def set_fail_msg(self):
        if self.tasks_without_name > 0:
            self.msg_final += self.fail_info1
            self.msg_final += "do NOT have a name. "

        if self.tasks_with_invalid_name > 0:
            self.msg_final += self.fail_info2
            self.msg_final += "do NOT have a proper name format."
            
    def find_task_block(self, task_text, type):
        # Se establece un formato correcto tanto en la tarea a buscar como en el playbook que se analiza
        # Para poder buscar la linea en la que se encuentra la tarea (a causa del yaml.dump)
        task_text = "- " + task_text
        task_text = task_text.replace("null", "")
        task_text = task_text.translate(str.maketrans('', '', '"\'\\ '))
        self.contenido = self.contenido.translate(str.maketrans('', '', '"\'\\ '))
        self.contenido += "\n"
        task_split = task_text.strip().split('\n')
        # + "\n" para encontrar explicitamente task_split[0], no una linea que contenga task_split[0] (seria la linea del name o del modulo en caso de que no tenga name)
        self.find_line(task_split[0] + "\n", self.contenido, 0, type)

    def find_line(self, task_text, contenido, pos, type):
        indice = contenido.find(task_text, pos)
        
        # Si se ha encontrado
        if indice != -1:
            
            # Calcular la linea en la que se ha encontrado la tarea
            linea = contenido.count('\n', 0, indice) + 1

            # Si la linea no esta en el array de lineas significa que ya se ha encontrado y se mete (Por si hay tareas repetidas)
            if(linea not in self.lineas):
                self.lineas.append(linea)
                self.failed = True
                if(type == "nameless"):
                    self.fail_info1 += str(linea) + ", "
                else:  
                    self.fail_info2 += str(linea) + ", "

            # Si esa linea ya ha sido encontrada significa que es una tarea repetida y tiene que seguir buscando mas abajo en el fichero
            else:
                self.find_line(task_text, contenido, indice + 1, type)

def main():
    module = AnsibleModule(
        argument_spec=dict(
            plain_file_content=dict(type='str', required=True)
        )
    )

    contenido = module.params['plain_file_content']
    names_checker = NamesChecker(contenido)

    result = {
    }

    result['msg'] = names_checker.msg_final
    result['failed'] = names_checker.failed

    module.exit_json(**result)

if __name__ == '__main__':
    main()