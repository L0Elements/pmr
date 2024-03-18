#the 'files.py' module is intended to manage all the source files
#including and excluding them from the project
#each file will have a separate json entry, that will be used by other modules in this project
from core.common.clargs.baseparameters import BaseParameters
from core.common.failure import Failure
import os.path

class file_parameters(BaseParameters):
    filepath = ""
    
    def __init__(self, args):
        if len(args) == 0:
            Failure("File not provided").throw()
        super().__init__(args)

    def eval_args(self, args):
        super().eval_args(args)
        
        filepath = os.path.join(self.working_dir, args[0]) #tries to find the requested file

        if os.path.isfile(filepath):
            self.filepath = filepath

        else:
            e = Failure("File provided doesn't exist")
            e.add_hint("Use the syntax 'pmr add/rm [file] <commands>'")
            e.throw()



def add_file(params):
    pass


def remove_file(params):
    pass


