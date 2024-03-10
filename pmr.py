import sys
from rich.console import Console
from rich.style import Style

#definition of standard (in the program) styles

style_critical = Style(color="red", bold=True)
style_error = Style(color="red", italic=True)
style_warning = Style(color="yellow", italic=True)

#default console
console = Console()

#err console
cerr = Console(stderr=True,style=style_critical)


def print_help_message(args=[]): #TODO: implement args to this function.
    pass

def make_new_project(args=[]): #code: 0
    from core import project
    digest = project.eval_args(args)
    
    return project.make_project(digest)

def add_file_in_project(args=[]): #code: 1
    pass






#main func.
def main():

    #imports the tokens file and tries to get the unique number associated to the command
    #if not found, code == None
    from core.tokens import tokens
    code = int()
    try:
        code = tokens[sys.argv[1]][sys.argv[2]]
    except:
        code = None
        pass
    finally:
        del tokens #not needed anymore



    #if command not found, tell the user and print help message
    if code == None:
        cerr.print("Command not found!")
        console.print("check your syntax and type again", style=style_error)
        console.line(3)
        print_help_message()
        
        return
    
    #the following commands will execute the functions related to each command/code
    #this tuple will contain a reference to each of these functions, ordered by code.
    commands = (make_new_project, add_file_in_project)

    #execute the command, each command will take as argument the other execution arguments (in practice sys.argv[3:]
    #if one exception occours, handle it, print the errors and exit
    try:
        commands[code](sys.argv[3:])
    except Exception as stdexception:
        cerr.print(f"An error has occurred: {type(stdexception).__name__}" )
        cerr.print(stdexception)

        if '__notes__' in stdexception.__dict__:
            console.rule(style="bold white")
            for note in stdexception.__notes__:
                console.print(note, style=style_error)
        console.rule(style="bold white")
        console.line(2)

        #ask the user if (s)he wants to see the traceback
        conf = console.input("Would you like to see the tracebacks? (y) -> ")
       
        if conf.lower() == 'y':
            console.print_exception()

        sys.exit(1)




if __name__ == '__main__':
    #reading argv and interpret it
    #with no arguments, print help message and exit
    if len(sys.argv) <= 1 or sys.argv[1] == 'help':
        print_help_message()
        sys.exit(0)
    
    #command interpreter
    main()
