import os
import os.path as ph

from core import project as cproject
from core.tools import related_project


class ProjectError(Exception):
    pass

class ProjectExistsError(ProjectError):
    pass



class Project():
    main_dir = None

    manifest_path = None
    config_path = None
    files_path = None

    profiles = []
    files_list = []


    files_editable = None
    config_editable = None
    manifest_editable = None
    
    #if False, the instance must point to an existing project
    #if True, the instance is a virtual rapresentation of a project
    virtual = False
   
    #checks if the project is a valid existing (in the filesystem) project
    def exists(self):
        test = ph.exists(self.manifest_path)
        test = test and ph.exists(self.config_path)
        test = test and ph.exists(self.files_path)    

        return test

    def is_inner_project(self):
        outer = related_project(ph.join(self.main_dir, ".."))

        return (outer != None)

    def __init__(self, main_dir=os.getcwd(), **kwargs):
        self.main_dir = main_dir 
        self.virtual = bool(kwargs.get("create", False))
         
        self.manifest_path = ph.join(self.main_dir, ".projectpmr", "project.pmr")
        self.config_path = ph.join(self.main_dir, ".projectpmr", "config.json")
        self.files_path = ph.join(self.main_dir, ".projectpmr", "files.json")
            
        if not self.virtual:
            if not self.exists():
               e = ProjectError("Project files not found")
               e.add_note(f"make sure that {self.manifest_path}, {self.config_path} and {self.files_path} do exist")

               raise e
        else:
            if self.is_inner_project():
                raise ProjectExistsError("Another project exists in a parent directory")
            if not ph.isdir(self.main_dir):
                raise ProjectError(f"{self.main_dir} is not a valid directory")
    def create(self):
        if self.virtual:
            cproject.create_project(self.main_dir)
            self.virtual = False
        else:
            raise ProjectExistsError("the project is not virtual")

    
    def sync(self):
        pass

    
