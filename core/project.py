#project script - used to create a new project
import os.path
import os


class parameters():
    
    proj_path = str()




def eval_args(args):
    #checks the type of the function parameter args
    #args must be a tuple or a list, prefering one on the other is irrelevant in the function, since it'll be only read.
    if type(args) != list and type(args) != tuple:
        raise TypeError("args must be a list or a tuple")
    
    #declaring function variables:
    comprehension = parameters()
    dirpath = ""
   
    #reading string by string
    w = 0 #initialize w
    while w < len(args):


        #if concerns the directory
        if args[w] == "-d":
            
            #check if not already setted
            if dirpath == "": 
                
                #check if the second element exists, or raises an exception, enriched by notes
                try:
                    temp = args[w+1]
                except IndexError as e:
                    e.add_note("Wrong syntax used")
                    e.add_note("'-d' command truncates before the directory is given")
                    raise

                #if the second element exists, check if the path is a valid directory
                #with positive response add the absolutized path into dirpath
                if os.path.isdir(args[w+1]):
                    dirpath = os.path.abspath(args[w+1])
                    w += 2
                    continue
                else:
                    raise FileNotFoundError("provided directory doesn't exist or cannot be accessed")

            else:
                raise SyntaxError("Multiple directories chosen - use '-d' once")

        w += 1
    else:
        del w

    
    #TODO: fill a parameters() object with the obtained values, but if they're empty, use defaults or raise an exception
    
    if dirpath == "":
        dirpath = os.getcwd()

    comprehension.proj_path = dirpath

    return comprehension
