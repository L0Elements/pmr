import os.path as ph
import os

import json

def create_project(path):
    
    working_dir = os.getcwd()
    os.chdir(path)

    if not ph.isdir(".projectpmr"):
        os.mkdir(".projectpmr")

    os.chdir(".projectpmr")
    
    import shutil
    if ph.isdir("profiles"):
        shutil.rmtree("profiles")
    if ph.isdir("output"):
        shutil.rmtree("output")
    del shutil

    os.mkdir("profiles")
    os.mkdir("output")

    filesfd = open("files.json", "w", encoding="utf-8")
    configfd = open("config.json", "w", encoding="utf-8")
    manifestfd = open("project.pmr", "w", encoding="utf-8")

    filesfd.write("[]")
    configfd.write("{}")
    manifestfd.write("{}")

    for fd in [filesfd, configfd, manifestfd]:
        fd.close()

    os.chdir("output")

    with open(".gitignore", 'w') as f:
        f.write('*')
    
    os.chdir(working_dir)


def get_json(file_path):
    with open(file_path, "r", encoding="utf-8") as fp:
        return json.load(fp)

def write_json(file_path, obj):
    with open(file_path, "w", encoding="utf-8") as fp:
        json.dump(obj, fp, indent="\t")
