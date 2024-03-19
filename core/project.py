#project script - used to create a new project
import os.path
import os

from .common.clargs.baseparameters import BaseParameters
from .common.failure import Failure

from .common.console import console
from rich import prompt

class make_params(BaseParameters):
    working_dir = os.getcwd() 

    def eval_args(self, args):
        super().eval_args(args)
        current_path = os.getcwd()
        w = 0 #initialize w
        
        while w < len(args):

            #if concerns the directory
            if args[w] == "-d":
             
                #check if not already setted
                if self.working_dir == current_path: 
                 
                    #check if the second element exists, or raises an exception, enriched by notes
                    if w+1 >= len(args):
                        Failure("Wrong syntax used", "'-d' command truncates before the directory is given").throw()
    
                    #if the second element exists, check if the path is a valid directory
                    #with positive response add the absolutized path into dirpath
                    if os.path.isdir(args[w+1]):
                        self.working_dir = os.path.abspath(args[w+1])
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
            del current_path


def make_project(params):



    #change the directory to the project path
    os.chdir(params.working_dir)
    
    #control system
    if os.path.isdir(".projectpmr"):
        console.print(f"[green]'.projectpmr'[/green] found in path [green]'{os.getcwd()}'[/green]:")
        console.print("it's likely that a project already exists")
        console.print("if you want to continue, [bold red]the content related to the project will be wiped")
        console.line(2)
        if not params.safe: 
            confirm = prompt.Confirm.ask("[magenta]Do You wish to continue?[/]", default=False )
            if not confirm:
                console.print("Abort", style="bold blue")
                return #stops the function
        else:
            console.print("[bold blue]safe[/] option is set. [green]Auto aborting[/] [red](--no-safe)[red]")
            return #stops the function
    else:
        os.mkdir(".projectpmr")
    
    #if control doesn't return, start building the project files
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


