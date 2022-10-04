# IRS - Imported Requirements Search

import os 

import distutils.sysconfig as sysconfig
def std_modules():
    ret_list = []
    std_lib = sysconfig.get_python_lib(standard_lib=True)
    for top, dirs, files in os.walk(std_lib):
        for nm in files:
            if nm != '__init__.py' and nm[-3:] == '.py':
                ret_list.append(os.path.join(top, nm)[len(std_lib)+1:-3].replace('\\','.'))
    return ret_list


project_dir = os.path.abspath(os.getcwd())
print(f"Project Directory: {project_dir}\n")

python_files = []
dir_names, file_names, imported_packages = set(), set(), set()


for path, subdirs, files in os.walk(project_dir):
    dir_names.update(subdirs)
    file_names.update(files)
    for name in files:
        if name[-3:] == ".py":
            python_files.append(os.path.join(path, name))
            #print(os.path.join(path, name))

print(f"Number of Python Files: {len(python_files)}")


# Search Files for "import" and "from" Statements
for file in python_files:
    contents = open(file, "r").readlines()
    for line in contents: 
        line = line.split()
        # Empty Lines
        if len(line) == 0:
            continue 
        # Commented Out Code
        elif "#" in line[0]:
            continue 

        # Regular Imports
        if ("import" in line) and ("from" not in line):
            pos = line.index("import") 
            package = line[pos+1] 
            if "." in package: 
                package = package.split(".")[0] #1st element is module we care about
            #print(f"found {package} in {line}") 
            imported_packages.update([package])

        # From Statements
        elif ("from" in line[0]):
            #print("FROM DETECTED: ", line)
            pos = line.index("from")
            pkg = line[pos+1]
            if "." in pkg:
                pkg = pkg.split(".")[0] #1st element is module we care about
                #print(pkg)
            imported_packages.update([pkg])
            

# Clean Up Project Specific Code (imported but not in a requirements.txt) -- you have the source code homie/homette
remove_pkgs = []
additional_stds = ("collections", "json", "urllib", "requests", "distutils", "logging", "math", "settings", "sys", "os", "time", "unicodedata", "importlib")
std_pkgs = std_modules() #magic to check for Python standard modules
for pkg in imported_packages:
    if pkg in dir_names:
        remove_pkgs.append(pkg)
    elif pkg in std_pkgs:
        remove_pkgs.append(pkg)
    elif pkg in file_names:
        remove_pkgs.append(pkg)
    elif pkg in additional_stds:
        remove_pkgs.append(pkg)
for i in remove_pkgs:
    imported_packages.remove(i)

imported_packages = sorted(list(imported_packages)) #alphabetical is better
print(f"Number of Non-Local Packages: {len(imported_packages)}")
print(f"Imported Packages:\n{imported_packages}")


# Write out Package List
print(f"\nWriting Packages to 'irs_requirements.txt'")
outfile = os.open(os.path.join(project_dir, "irs_requirements.txt"), os.O_RDWR|os.O_CREAT) #to avoid an existing requirements file (User still manually reviews)
for pkg in imported_packages:
    pkg = pkg + "\n"
    os.write(outfile, pkg.encode())
os.close(outfile)


