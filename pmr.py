import sys
from core.common.console import console
from rich.style import Style


def print_help_message(args=[]): #TODO: implement args to this function.
    pass


def make_new_project(args=[]): #code: 0
    from core import project 
    params = project.make_params(args)
    
    return project.make_project(params)


def add_file_in_project(args=[]): #code: 1
    from core import files 
    
    params = files.file_parameters(args)
    return files.add_file(params)


def remove_file_from_project(args=[]):
    from core import files

    params = files.file_parameters(args)
    return files.remove_file(params)


#main function
def main():

    #imports the tokens file and tries to get the unique number associated to the command
    #if not found, code == None
    from core.tokens import tokens
    code = int()
    try:
        code = tokens[sys.argv[1]]
    except:
        code = None
        pass
    finally:
        del tokens #not needed anymore



    #if command not found, tell the user and print help message
    if code == None:
        console.print("Command not found!", style="red")
        console.print("check your syntax and type again")
        console.line(3)
        print_help_message()
        
        return
    
    #the following commands will execute the functions related to each command/code
    #this tuple will contain a reference to each of these functions, ordered by code.
    commands = (make_new_project, add_file_in_project, remove_file_from_project)

    #execute the command, each command will take as argument the other execution arguments (in practice sys.argv[3:]
    commands[code](sys.argv[2:])


if __name__ == '__main__':
    #reading argv and interpret it
    #with no arguments, print help message and exit
    if len(sys.argv) <= 1 or sys.argv[1] == 'help':
        print_help_message()
        sys.exit(0)
    
    #command interpreter
    main()
