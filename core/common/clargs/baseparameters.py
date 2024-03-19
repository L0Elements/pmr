#this is the BaseParameters class 
#this class(along with is derivates) is in charge of these functions:
#interpreting the command-line arguments and storing them in the object fields.
from core.common.failure import Failure

class BaseParameters:

    safe = True
    
    def __init__(self, args=tuple()):
        self.eval_args(args)



    def eval_args(self, args):
        
        #reading string by string
        w = 0 #initialize w
        while w < len(args):
    
    
         
            #if concerns the 'safe' parameter
            if args[w] in ("-s", "--safe"):
                self.safe = True
            if args[w] in ("-S", "--no-safe"):
                self.safe = False
             
    
            w += 1
        else:
            del w
                 
