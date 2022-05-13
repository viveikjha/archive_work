class init_data:
    def __init__(self,telescope,pixscale_err,percent_error,index_ver_arr):
        self.telescope=telescope
        self.pixscale_err=pixscale_err
        self.percent=percent_arr
        self.index_ver_arr=index_ver_arr


    def description(self):
        return f"{self.telescope} pixel scale is {self.pix} ."

    def test_object(self):
        return f"This is a test object for {self.telescope}."

files=sorted(glob.glob('*fits'))
for line in files:
    if 'bias' in line:
        print(line)


path=os.getcwd()

folders = ([name for name in os.listdir(path)
            if os.path.isdir(os.path.join(path, name))])

for folder in folders:
    contents = os.listdir(os.path.join(path,folder)) # get list of contents
    if len(contents) >0: # if greater than the limit, print folder and number of contents
        print(folder,len(contents))

root=os.getcwd()

for path, subdirs, files in os.walk(root):
    for name in files:
        print(os.path.join(path, name))
