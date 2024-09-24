import os

def add_path(folder,file=None):
    """Function to make path of file"""
    if file:return os.path.join(folder, file)
    else: return os.path.join(folder)


def read_file(file_path):
    """Function to read file"""

    with open(file_path , 'r' ) as file:
        content = file.read()
    return content


def wirte_file(file_path,contents):
    """Function to wirte in file"""

    with open(file_path , 'w' ) as file:
        content = file.write(contents)
    return content



def append_file(file_path,append):
    """Function to append file"""

    with open(file_path , 'a' ) as file:
        content = file.write(append)
    return content

def CopyFiles(file_name ,func, base_path:...,target_dir:...):        
        src = os.path.join(base_path, file_name)
        dest = os.path.join(target_dir, file_name)
        func(src, dest)        
        return dest


def get_all_modules(folder_path):
    modules = [
        module
        for module in os.listdir(folder_path)
        if module.endswith('.py')
    ]
    return modules

def add_module(module,folder_path,content:...):
    new_module = os.path.join(folder_path,module+'.py')
    
    with open(new_module,'w') as module:
        module.write(content)
        module.close()
