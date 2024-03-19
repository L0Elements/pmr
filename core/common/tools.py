#these are useful tools used by the lower part of the program to avoid repetitions
import os, os.path


#find the main project path, given a path to a directory
def related_project(dirpath):
    #convert to absolute
    dirpath = os.path.abspath(dirpath)

    #stops when it reaches the filesystem root
    while os.path.splitroot(dirpath)[2] != '':
        #if directory contains the project, proj_dir exists
        proj_dir = os.path.join(dirpath, ".projectpmr")
         
        #check if proj_dir exists
        if os.path.isdir(proj_dir):
            #returns the relative path
            return dirpath
         
         
        #down by one directory
        dirpath = os.path.normpath(os.path.join(dirpath, ".."))
