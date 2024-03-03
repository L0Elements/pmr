#project script - used to create a new project
import os.path


class parameters():
    template_name = str()  
    template_path = str()
    
    proj_path = str()


def get_templates():
    pass





def eval_args(args):
    #checks the type of the function parameter args
    if type(args) != list and type(args) != tuple:
        raise TypeError("args must be a list or a tuple")
    
    #declaring function variables:
    comprehension = parameters()
    template = ""
    dirpath = ""
   
    #reading string by string
    w = 0 #initialize w
    templateslist = get_templates()
    while w < len(args):


        #if concerns the directory
        if args[w] == "-d":
            
            if dirpath == "": 
                
                if os.path.isdir(args[w+1]):
                    dirpath = os.path.abspath(args[w+1])
                    w += 2
                    continue
                else:
                    raise FileNotFoundError("provided directory does't exist or cannot be accessed")

            else:
                raise SyntaxError("Multiple directories chosen - use '-d' once")
        #if concerns the template
        if args[w] in templateslist:
            if template == ""
                template = args[w]
            else:
                raise SyntaxError("Multiple templates given - use only one of them")

        w++
    else:
        del w

    
    #TODO: fill a parameters() object with the obtained values, but if they're empty, use defaults or raise an exception
