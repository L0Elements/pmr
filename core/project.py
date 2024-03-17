#project script - used to create a new project
import os.path
import os

from rich.console import Console
from rich import prompt

#core.project's console
pconsole = Console()

#class: make_params
#contains all the variables that direct the creation of a project
class make_params:
    proj_path = ""
    safe = True



# function: make_project
# args: params
#   type = make_params
def make_project(params):


    #checking type:
    if type(params) != make_params:
        raise TypeError("'params' is of the wrong type")

    #change the directory to the project path
    os.chdir(params.proj_path)
    
    #control system
    if os.path.isdir(".projectpmr"):
        pconsole.print(f"[green]'.projectpmr'[/green] found in path [green]'{os.getcwd()}'[/green]:")
        pconsole.print("it's likely that a project already exists")
        pconsole.print("if you want to continue, [bold red]the content related to the project will be wiped")
        pconsole.line(2)
        if not params.safe: 
            confirm = prompt.Confirm.ask("[magenta]Do You wish to continue?[/]", default=False )
            if not confirm:
                pconsole.print("Abort", style="bold blue")
                return #stops the function
        else:
            pconsole.print("[bold blue]safe[/] option is set. [green]Auto aborting[/] [red](--no-safe)[red]")
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





def eval_args(args):
    #checks the type of the function parameter args
    #args must be a tuple or a list, prefering one on the other is irrelevant in the function, since it'll be only read.
    if type(args) != list and type(args) != tuple:
        raise TypeError("args must be a list or a tuple")
    
    #declaring function variables:
    comprehension = make_params()
   
    #reading string by string
    w = 0 #initialize w
    while w < len(args):


        #if concerns the directory
        if args[w] == "-d":
            
            #check if not already setted, if 'safe' option is false, the last '-d' option is accepted
            if comprehension.proj_path == "": 
                
                #check if the second element exists, or raises an exception, enriched by notes
                try:
                    temp = args[w+1]
                except IndexError as e:

                    e.add_note("Wrong syntax used")
                    e.add_note("'-d' command truncates before the directory is given")

                #if the second element exists, check if the path is a valid directory
                #with positive response add the absolutized path into dirpath
                if os.path.isdir(args[w+1]):
                    comprehension.proj_path = os.path.abspath(args[w+1])
                    w += 2
                    continue
                else:
                    raise FileNotFoundError("provided path isn't a directory or doesn't exist or cannot be accessed")

            else:
                raise SyntaxError("Multiple directories chosen - use '-d' once")
        
        #if concerns the 'safe' parameter
        if args[w] in ("-s", "--safe"):
            comprehension.safe = True
        if args[w] in ("-S", "--no-safe"):
            comprehension.safe = False
            

        w += 1
    else:
        del w
    
    #final dispositions
    if comprehension.proj_path == "":
        comprehension.proj_path = os.getcwd()


    return comprehension

