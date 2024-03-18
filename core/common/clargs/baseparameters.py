#this is the BaseParameters class 
#this class(along with is derivates) is in charge of these functions:
#interpreting the command-line arguments and storing them in the object fields.
import os
import os.path

from core.common.failure import Failure

class BaseParameters:

    safe = True
    working_dir = os.getcwd() 
    
    def __init__(self, args=tuple()):
        self.eval_args(args)



    def eval_args(self, args):
        
        #reading string by string
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
         
            #if concerns the 'safe' parameter
            if args[w] in ("-s", "--safe"):
                self.safe = True
            if args[w] in ("-S", "--no-safe"):
                self.safe = False
             
    
            w += 1
        else:
            del w
            del current_path
                 
