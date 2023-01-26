root='/data/DFOT/2012/'
for path, subdirs, files in os.walk(root):
    for name in files:
        if fnmatch(name,pattern):
            print(os.path.join(path,name))

