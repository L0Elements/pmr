#project script - used to create a new project
import os.path
import os

from core.common.clargs.baseparameters import BaseParameters
from core.common.failure import Failure

from core.common.console import console
from rich import prompt

class make_params(BaseParameters):
    pass



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
    open("files.json", 'w').close() 
    open("config.json", 'w').close()

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





