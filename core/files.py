#the 'files.py' module is intended to manage all the source files
#including and excluding them from the project
#each file will have a separate json entry, that will be used by other modules in this project
from .common.clargs.baseparameters import BaseParameters
from .common.failure import Failure
from .common.console import console
from .common.tools import related_project
import os.path, os

import json

class file_parameters(BaseParameters):
    filepath = ""
    proj_dir = ""
    name = ""

    def __init__(self, args):
        if len(args) == 0:
            Failure("File not provided").throw()
        super().__init__(args)
    
    def eval_args(self, args):
        super().eval_args(args)

        self.get_path(args[0])
        
        if self.filepath == None:
            Failure(f"'{args[0]}' is not bound to a project").throw()
        
        w = 1 #because args[0] has just been read
        while w < len(args):

            #if concerns the name
            if args[w] == "--name":
                if w+1 >= len(args):
                    e = Failure("Incomplete command-line arguments")
                    e.add_note("'--name' statement truncates before giving the actual name")
                    e.add_hint("remember to use the syntax '--name [name]'")
                    e.throw()
                else:
                    self.name = args[w+1]
                    w += 2
                    continue
            w += 1

        else:
            #final dispositions
            del w
            if self.name == "":
                self.name = os.path.split(self.filepath)[1]



    #gets the file path and puts it into self.filepath
    def get_path(self, filepath):
        

        if os.path.isfile(filepath):
            self.proj_dir = related_project(os.path.dirname(filepath))

            if self.proj_dir != None:
                self.filepath = os.path.relpath(filepath, self.proj_dir)
            
            else:
                Failure("Path provided is not bound to a project").throw()


        else:
            e = Failure("path not provided or doesn't point to an existing file")
            e.add_hint("Use the syntax 'pmr add/rm [file] <commands>'")
            e.throw()

                
def get_json():
    with open("files.json", "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.decoder.JSONDecodeError as err:
            fail = Failure("Error in JSON decoding")
            fail.add_note(f"in file 'files.json': {err.msg}")
            fail.add_note(f"error encountered in line {err.lineno}, {err.colno}")
            fail.add_hint("Make sure this is valid JSON code")
            fail.throw()
    
def add_file(params):
    
    os.chdir(os.path.join(params.proj_dir, ".projectpmr"))
    content = get_json()


    with open("files.json", "w", encoding="utf-8") as f:
        entry = {"name": params.name, "path": params.filepath}

        if not is_duplicate(entry["name"], entry["path"] , content):
            content.append(entry) 
        
            json.dump(content, f, indent='\t')
        
        else:
            json.dump(content, f, indent='\t')
            Failure("pmr doesn't admit duplicates").throw()


def remove_file(params):
    path = params.filepath
    
    os.chdir(os.path.join(params.proj_dir, ".projectpmr"))
    
    content = get_json()
    index = find_entry(path, content)
    if index != None:
        content.pop(index)
    else:
        e = Failure("Entry not found")
        e.add_hint("perhaps the file provided wasn't added in the project")
        e.throw()
    with open("files.json", 'w', encoding="utf-8") as f:
        json.dump(content, f, indent='\t')

    return index

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

def find_entry(path, contents):
    paths = get_unique_attributes(contents)[1]


    for i in range(len(paths)):
        
        if path == paths[i]:
            return i
    else:
        return None

