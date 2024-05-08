import os
import os.path as ph

from core import project as cproject
from core.tools import related_project

from core.config import FileConfigurator

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

    files = None
    config = None
    manifest = None
    
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

    def __init__(self, main_dir=os.getcwd(), create=False):
        self.main_dir = main_dir 
        self.virtual = create
         
        self.manifest_path = ph.join(self.main_dir, ".projectpmr", "project.pmr")
        self.config_path = ph.join(self.main_dir, ".projectpmr", "config.json")
        self.files_path = ph.join(self.main_dir, ".projectpmr", "files.json")
            
        if not self.virtual:


            if not self.exists():
               e = ProjectError("Project files not found")
               e.add_note(f"make sure that {self.manifest_path}, {self.config_path} and {self.files_path} do exist")

               raise e
            else:
                self.get()
            

        else:
            if self.is_inner_project():
                raise ProjectExistsError("Another project exists in a parent directory")
            if not ph.isdir(self.main_dir):
                raise ProjectError(f"{self.main_dir} is not a valid directory")
    def create(self):
        if self.virtual:
            cproject.create_project(self.main_dir)
            self.get()
            self.virtual = False
        else:
            raise ProjectExistsError("the project is not virtual")

    
    def sync(self):
        
        cproject.write_json(self.files_path, self.files)
        cproject.write_json(self.config_path, self.config)
        cproject.write_json(self.manifest_path, self.manifest)

    def get(self):
        
        self.files = cproject.get_json(self.files_path)
        self.config = cproject.get_json(self.config_path)
        self.manifest = cproject.get_json(self.manifest_path)

    def __str__(self):

        string = ""
        if self.virtual:
            string += "virtual " 

        return f"<{string}Project at {self.main_dir}>"
    
    def file_append(self,file):
        if isinstance(file, dict):
            file = FileConfigurator(file, convert=True)
        elif isinstance(file, FileConfigurator):
            pass
        else:
            raise TypeError("`file` must be of 'dict' or 'FileConfigurator' type")
        
        file["path"] = ph.relpath(file["path"], self.main_dir)

        if not (self.file_exists(file["path"]) or self.file_exists(file.get("name"))):
            self.files.append(file())
        else:
            raise FileExistsError(f"'{file['path']}' already included or name already used") 

    def file_getindex(self, fileid):
        #find the file by name or path
        #check if fileid is None or Empty
        if not fileid:
            return None
        #checks if fileid is a file or not
        if ph.isfile(fileid):
            path = ph.relpath(fileid, self.main_dir)
            
            i = 0
            while i < len(self.files):
                e = self.files[i]
                if path == e["path"]:
                   return i
                i += 1
        #if path wasn't found, try to find by name
        names = list()
        for e in self.files:
            names.append(e.get("name"))

        i = 0
        while i < len(names):
            if not names[i]:
                pass
            else:
                if fileid == names[i]:
                    return i
            i += 1



    def file_get(self, fileid):
        i = self.file_getindex(fileid) 
        if i != None:
            return self.files[i]

    def file_exists(self, fileid):
        return self.file_getindex(fileid) != None

    
    

