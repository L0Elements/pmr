import sys
import os
from core.console import console
from core.failure import Failure

from rich.prompt import Confirm


def print_help_message(args=[]): #TODO: implement args to this function.
    pass


def make_new_project(args=[]): #code: 0
    from core import project
    
    directory = None
    w = 0 #initialize w
     
    while w < len(args):
        if args[w] == "-d":
         
            #check if not already setted
            if directory == None: 
             
                #check if the second element exists, or raises an exception, enriched by notes
                if w+1 >= len(args):
                    Failure("Wrong syntax used", "'-d' command truncates before the directory is given").throw()
 
                #if the second element exists, check if the path is a valid directory
                #with positive response add the absolutized path into dirpath
                if os.path.isdir(args[w+1]):
                    directory = os.path.abspath(args[w+1])
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
     


    if directory == None:
        directory = os.getcwd()
    
    if os.path.isfile(os.path.join(directory, ".projectpmr", "project.pmr")):
        console.print(f"a project exists in [green]'{directory}'")
        p = Confirm.ask("Do you want to overwrite it?", default=False)

        if not p:
            console.print("Abort", style="bold bright_blue")
            return


    project.create_project(directory) 
        
    console.print("Empty project initialized at ", directory, style="bold green")

def add_file_in_project(args=[]): #code: 1
    import files 
    
    params = files.eval_args(args)
    return files.add_file(params)


def remove_file_from_project(args=[]):
    import files

    return files.remove_file(args)

def list_files(args=[]):
    import files

    files.print_files(args)

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
