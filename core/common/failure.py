#this is the failure class, it will be used if some error happens.
#it'll be used to separate the python builtin Exceptions from program's errors
#also, this class will offer more versatility than a python exception
from .console import console
from rich.markup import escape
import sys


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
        console.print("An [red]error[/] occurred: ", end="")
        console.print(escape(self.error), style="red italic")
        console.line()

        for note in self.error_notes:
            console.print("--> ", escape(note))

        console.line()

        for hint in self.hints:
            console.print("hint -> ", escape(hint), style="yellow italic")

        sys.exit(1)
