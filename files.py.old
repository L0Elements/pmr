#the 'files.py' module is intended to manage all the source files
#including and excluding them from the project
#each file will have a separate json entry, that will be used by other modules in this project
from core.failure import Failure
from core.console import console
from core.tools import related_project
import os.path, os

import json


 
def eval_args(args):
    params = dict()
    
    #checks if the file is provided
    if len(args) == 0:
        with Failure("File not provided") as f:
            f.add_hint("use the syntax 'pmr add [file] <options>'")

    params.update(_get_path(args[0]))
     
     
    w = 1 #because args[0] has just been read
    while w < len(args):
        #if concerns the name
        if args[w] == "--name":
            if w+1 >= len(args):
                with Failure("Incomplete command-line arguments") as e:
                    e.add_note("'--name' statement truncates before giving the actual name")
                    e.add_hint("remember to use the syntax '--name [name]'")
            else:
                params['name'] = args[w+1]
                w += 2
                continue
        w += 1
    else:
        #final dispositions
        del w
        #if the name is not provided, try to use it's name
        if params.get('name') == None:
            params['name'] = os.path.basename(params['filepath'])

    return params



    #gets the file path, returns a dictionary with the relative path and the project directory, if it doesn't failes
def _get_path(filepath):
    if os.path.isfile(filepath):
        proj_dir = related_project(os.path.dirname(filepath))
        if proj_dir != None:
            filepath = os.path.relpath(filepath, proj_dir)
            return {'proj_dir': proj_dir, 'filepath': filepath} 
        else:
            Failure("Path provided is not bound to a project").throw()
    else:
        e = Failure("path not provided or doesn't point to an existing file")
        e.add_hint("Use the syntax 'pmr add [file] <commands>'")
        e.throw()

                
def get_json(rootpath="."):
    with open(os.path.join(rootpath, "files.json"), "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.decoder.JSONDecodeError as err:
            fail = Failure("Error in JSON decoding")
            fail.add_note(f"in file 'files.json': {err.msg}")
            fail.add_note(f"error encountered in line {err.lineno}, {err.colno}")
            fail.add_hint("Make sure this is valid JSON code")
            fail.throw()

def update_json(content, rootpath="."):
    with open(os.path.join(rootpath, "files.json"), 'w', encoding='utf-8') as f:
        json.dump(content, f, indent='\t')

def add_file(params):
    
    os.chdir(os.path.join(params['proj_dir'], ".projectpmr"))
    content = get_json()


    entry = {"name": params['name'], "path": params['filepath']}

    if not is_duplicate(entry["name"], entry["path"] , content):
        content.append(entry) 
  
        update_json(content)
         
        console.print("[blue]new file added: ")
        console.print(f"'{entry['path']}' with name = '{entry['name']}'")
    else:
        e = Failure("pmr doesn't admit duplicates")
        e.add_note(f"{entry['path']} already included or name {entry['name']} already used")
        e.add_hint("if you want to include a file with the same name but a different directory of another file, you should use the '--name' directive")
        e.add_hint("remember: if you don't provide a name, pmr will chose the file name", "you can always change the name in files.json")
        e.throw()

def remove_file(identifiers): 
    identifiers = frozenset(identifiers)
    successes = 0
    failures = 0
    
    prj_path = related_project('.')
    
    if prj_path == None:
        Failure("you are currently outside a valid project").throw()
        #program end
    
    projectpmr_dir = os.path.join(prj_path, ".projectpmr")
    content = get_json(projectpmr_dir)
    uniqueattr = get_unique_attributes(content)

    names = uniqueattr[0]
    paths = uniqueattr[1]

    del uniqueattr

    for identifier in identifiers:
        #used to check if it's a failure or a success.
        found = False

        if os.path.isfile(identifier): #if the identifier is a file, search between the files
            
            #gets the relative path and compare it.
            relativepath = os.path.relpath(identifier, prj_path)
            for i in range(len(paths)):
                if relativepath == paths[i]:
                    content[i] = None
                    found = True
                    break #stop searching for the file
        else: #if not, search between the names
            for i in range(len(names)):
                if identifier == names[i]:
                    content[i] = None
                    found = True
                    break #stop searching for the name
            
        if found:
            console.print("[green]removed[/] ", identifier)
            successes += 1
        else:
            console.print(identifier, " was not found", style='bright_red')
            failures += 1

    if successes != 0: #avoid to rewrite the file if nothing was changed
        #clear all removed elements

        while i < successes:
            content.remove(None)
            i += 1


        update_json(content, projectpmr_dir)

    console.print(f"removed {successes} files, it wasn't possible to remove {failures} files")




def is_duplicate(name, path , contents):
    
    attributes = get_unique_attributes(contents)
    
    for i in range(len(attributes[0])):
        if name == attributes[0][i] \
                or \
                path == attributes [1][i]:

                    return True
    else:
        return False



def get_unique_attributes(contents):
    
    
    names = list()
    filepaths = list()

    for i in contents:
        names.append(i["name"])
        filepaths.append(i["path"])

    return (names, filepaths)

def print_files(args=[]):
    prj_path = related_project(".")
    
    if prj_path == None:
        Failure("you are currently outside a valid project").throw()

    os.chdir(os.path.join(prj_path, ".projectpmr"))
    content = get_json()

    console.print("files in", prj_path, style="bold magenta")
    console.line(2)
    if '-v' in args or '--verbose' in args:
        console.print_json(data=content)
    else:
        attr = get_unique_attributes(content)
        names = attr[0]
        paths = attr[1]
        del attr

        for i in range(len(names)):
            console.print(f"[bold blue]{names[i]}", " --> ", f"[green]'{paths[i]}'") #format and print the names and the paths
