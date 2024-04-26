#this is the failure class, it will be used if some error happens in the front-end code
#the output from this class will be more readable and user-friendly than  a python exception
from rich.console import Console
from rich.markup import escape
import sys

fconsole = Console()
class Failure:
    error = str()
    error_notes = []
    hints = []
    
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.throw()


    def __init__(self, *args):
        
        if len(args) == 0:
            self.error = "Error"
        else:
            self.error = args[0]
         
            for err in args[1:]:
                self.error_notes.append(err)

    def add_note(self, *args): #insert a comma-separated list of notes
        for err in args:
            self.error_notes.append(err)

    def add_hint(self, *args): #insert a comma-separated list of hints
        for hint in args:
            self.hints.append(hint)

    def throw(self):
        fconsole.print("An [red]error[/] occurred: ", end="")
        fconsole.print(escape(self.error), style="red italic")
        fconsole.line()

        for note in self.error_notes:
            fconsole.print("--> ", escape(note))

        fconsole.line()

        for hint in self.hints:
            fconsole.print("hint -> ", escape(hint), style="yellow italic")

        sys.exit(1)
