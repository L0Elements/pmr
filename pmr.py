import sys
from rich.console import Console
from rich.style import Style

#definition of standard (in the program) styles

style_critical = Style(color="bright_red", bgcolor="white", bold=True)
style_error = Style(color="red", italic=True)
style_warning = Style(color="yellow", italic=True)

#default console
console = Console()

#err console
cerr = Console(stderr=True,style=style_critical)


def print_help_message():
    pass

#main func.
def main():
   
    #discriminate between commands and options
    commands = list()
    options = list()
    
    for arg in sys.argv[1:]:
        if arg.startswith(('-','--','/')):
           options.append(arg.lstrip("--/")) 
        else:
            commands.append(arg)
    console.log(commands, options)
    
    if sys.argv[1] == 'project': #BEGIN pmr.project range of commands
          #make a new project in the current folder       
          if sys.argv[2] == 'new':
              pass


    #if command not found, tell the user and print help message
    cerr.print("Command not found:")
    console.print("check your syntax and type again", style=style_error)
    console.line(3)
    print_help_message()


if __name__ == '__main__':
    #reading argv and interpret it
    #with no arguments, print help message and exit
    if len(sys.argv) <= 1:
        print_help_message()
        sys.exit(0)
    
    #command interpreter
    main()
