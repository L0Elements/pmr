import sys
import os
from rich.console import Console
from core.failure import Failure

from rich.prompt import Confirm

console = Console()
def cl_args_eval(clargs=[]):
    
    params = {} #the parameters as a dictionary, it'll be the return value
    w = 0 #iterator
    while w < len(clargs):
        if clargs[w] == "-d":
         
            #check if not already setted
            if params.get("directory") == None: 
             
                #check if the second element exists, or raises an exception, enriched by notes
                if w+1 >= len(clargs):
                    Failure("Wrong syntax used", "'-d' command truncates before the directory is given").throw()
 
                #if the second element exists, check if the path is a valid directory
                #with positive response add the absolutized path into "directory"
                if os.path.isdir(clargs[w+1]):
                    params["directory"] = os.path.abspath(clargs[w+1])
                    w += 2
                    continue
                else:
                    Failure("Directory not found", "provided path isn't a directory,", "doesn't exist or cannot be accessed").throw()
 
            else:
                e = Failure("Multiple directories chosen") 
                e.add_hint("use '-d' once")
                e.throw()
        
        elif clargs[w] in ("-v", "--verbose"):
            params["verbose"] = True
        
        elif clargs[w] in ("-q", "--quiet"):
            params["quiet"] = True

        else:
            with Failure("Syntax error") as f:
                f.add_note(f"'{clargs[w]}' parameter was not found")
                f.add_hint("make sure you wrote the command correctly")

        w += 1
    else:
        del w
    
    if not params.get("directory"): #explain: if it's None (Automatically evaluated to False), it will be setted at the current directory
        params["directory"] = os.getcwd()
    return params

def print_help_message(args=[]):
    pass


def make_new_project(args=[]): #code: 0
    from project import Project
    directory = cl_args_eval(args)["directory"] 
    
    if os.path.isfile(os.path.join(directory, ".projectpmr", "project.pmr")):
        console.print(f"a project exists in [green]'{directory}'")
        p = Confirm.ask("Do you want to overwrite it?", default=False)

        if not p:
            console.print("Abort", style="bold bright_blue")
            return
    
    Project(directory, create=True).create()
    
        
    console.print("Empty project initialized at ", directory, style="bold green")

def add_file_in_project(args=[]): #code: 1
    from project import Project
    from core.tools import related_project

    path = args[0]
    project = None
    
    #find and set the project, or throws a failure
    if os.path.isfile(path):
        prj_path = related_project(os.path.dirname(path))

        if prj_path != None:
            project = Project(prj_path)
        else:
            Failure(f"{path} doesn't belong to a project").throw()
    else:
        Failure(f"{path} is not an existing file").throw()
    
    file_entry = dict(path=path)
    project.files.append(file_entry)
    project.sync()

    console.print(f"{path} added to project")
def remove_file_from_project(args=[]):
    import files

    return files.remove_file(args)

def list_files(args=[]):
    from project import Project

    options = cl_args_eval(args)
    project = Project(options["directory"])

    if options.get("verbose"):
        console.print_json(data=project.files)
    else:
        from rich.table import Table
        from rich import box
        table = Table("Name", "File path", title=f"files indexed in '{options['directory']}'", \
                box=box.SIMPLE_HEAD, \
                title_style = "bright_blue", \
                expand = True, \
                )
        for f in project.files:
            table.add_row(f.get("name", ""), f["path"])

        console.print(table)

#main function
def main():
    
    command = sys.argv[1]

    if command == "new":
        make_new_project(sys.argv[2:])
    elif command == "add":
        add_file_in_project(sys.argv[2:])
    elif command == "rm":
        remove_file_from_project(sys.argv[2:])
    elif command == "list":
        list_files(sys.argv[2:])

    else:
        console.print("Command not found", style="red")
        console.line()
        
        print_help_message()
    

if __name__ == '__main__':
    #reading argv and interpret it
    #with no arguments, print help message and exit
    if len(sys.argv) <= 1 or sys.argv[1] == 'help':
        print_help_message()
        sys.exit(0)
    
    #command interpreter
    main()
