#project script - used to create a new project
import os.path
import os

from .common.failure import Failure
from .common.tools import related_project

from .common.console import console
from rich import prompt


def eval_args(args):
    params = dict()
    w = 0 #initialize w
     
    while w < len(args):
        #if concerns the directory
        if args[w] == "-d":
         
            #check if not already setted
            if params.get("directory") == None: 
             
                #check if the second element exists, or raises an exception, enriched by notes
                if w+1 >= len(args):
                    Failure("Wrong syntax used", "'-d' command truncates before the directory is given").throw()
 
                #if the second element exists, check if the path is a valid directory
                #with positive response add the absolutized path into dirpath
                if os.path.isdir(args[w+1]):
                    params["directory"] = os.path.abspath(args[w+1])
                    w += 2
                    continue
                else:
                    Failure("Directory not found", "provided path isn't a directory,", "doesn't exist or cannot be accessed").throw()
 
            else:
                e = Failure("Multiple directories chosen") 
                e.add_hint("use '-d' once")
                e.throw()
        w += 1
    else:
        del w
        
    #if the directory is not given, use the current working directory
    if params.get("directory") == None:
        params["directory"] = os.getcwd()

    #check if provided directory is part of another project, it excludes the directory to distinguish from a project reset
    finding = related_project(os.path.join(params["directory"], '..'))
    if finding != None:
        Failure(f"'{params['directory']}' is inside another project", f"project found in '{finding}'").throw()
    else:
        pass

    #in the end, returns the 'params' dictionary
    return params

def make_project(params):



    #change the directory to the project path
    os.chdir(params['directory'])
    
    #control system
    if os.path.isdir(".projectpmr"):
        console.print(f"[green]'.projectpmr'[/green] found in path [green]'{os.getcwd()}'[/green]:")
        console.print("it's likely that a project already exists")
        console.print("if you want to continue, [bold red]the content related to the project will be wiped")
        console.line(2)

        #give prompt
        confirm = prompt.Confirm.ask("[magenta]Do You wish to continue?[/]", default=False )
        if not confirm:
            console.print("Abort", style="bold blue")
            return #stops the function
    else:
        os.mkdir(".projectpmr")
    
    #start building the project files
    #the effectctive directory, which will contain every information about the project
    os.chdir(".projectpmr")   
   
    #create the required files
    _initialize_json("files.json") 
    _initialize_json("config.json")

    #wipe the old directories, to be replaced next, if they exist.
    import shutil
    if os.path.isdir("profiles"):
        shutil.rmtree("profiles")
    if os.path.isdir("output"):
        shutil.rmtree("output")
    del shutil

    #make the desired directories
    os.mkdir("profiles")
    os.mkdir("output")

    #create a .gitignore in the output folder, the directory change is required for platform-independence
    os.chdir("output")
    with open(".gitignore", 'w') as f:
        f.write('*')
    os.chdir("..")


def _initialize_json(path):
    with open(path, 'w', encoding="utf-8") as f:
        f.write("[]")


