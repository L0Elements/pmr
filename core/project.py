#project script - used to create a new project
import os.path
import os

from rich.console import Console
from rich import prompt

def make_project(project_dict):
    console = Console()

    #checking type:
    if type(project_dict) != dict:
        raise ValueError("'project_dict' must be a dictionary")

    #change the directory to the project path
    os.chdir(project_dict["proj_path"])

    if os.path.isdir(".projectpmr"):
        console.print(f"[green]'.projectpmr'[/green] found in path [green]'{os.getcwd()}'[/green]:")
        console.print("it's likely that a project already exists")
        console.print("if you want to continue, [bold red]the content related to the project will be wiped")
        console.line(2)
        
        if not prompt.Confirm.ask("[magenta]Do You wish to continue?[/]", default='n'):
            return
    else:
        os.mkdir(".projectpmr")

    #the effectctive directory, which will contain every information about the project
    os.chdir(".projectpmr")   
   
    #create the required files
    open("files.json", 'w').close() 
    open("config.json", 'w').close()

    import shutil
    if os.path.isdir("profiles"):
        shutil.rmtree("profiles")
    if os.path.isdir("output"):
        shutil.rmtree("output")

    os.mkdir("profiles")
    os.mkdir("output")

    #create a .gitignore in the output folder
    os.chdir("output")
    with open(".gitignore", 'w') as f:
        f.write('*')
    os.chdir("..")


def eval_args(args):
    #checks the type of the function parameter args
    #args must be a tuple or a list, prefering one on the other is irrelevant in the function, since it'll be only read.
    if type(args) != list and type(args) != tuple:
        raise TypeError("args must be a list or a tuple")
    
    #declaring function variables:
    comprehension = {\
            "proj_path": "" \
            }
   
    #reading string by string
    w = 0 #initialize w
    while w < len(args):


        #if concerns the directory
        if args[w] == "-d":
            
            #check if not already setted
            if comprehension["proj_path"] == "": 
                
                #check if the second element exists, or raises an exception, enriched by notes
                try:
                    temp = args[w+1]
                except IndexError as e:

                    e.add_note("Wrong syntax used")
                    e.add_note("'-d' command truncates before the directory is given")

                #if the second element exists, check if the path is a valid directory
                #with positive response add the absolutized path into dirpath
                if os.path.isdir(args[w+1]):
                    comprehension["proj_path"] = os.path.abspath(args[w+1])
                    w += 2
                    continue
                else:
                    raise FileNotFoundError("provided path isn't a directory or doesn't exist or cannot be accessed")

            else:
                raise SyntaxError("Multiple directories chosen - use '-d' once")

        w += 1
    else:
        del w

    if comprehension["proj_path"] == "":
        comprehension["proj_path"] = os.getcwd()


    return comprehension

