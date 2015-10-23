

import web
import os
import os.path

def build_array_with_dir(rootdir):
        str = ""
        dir_tree = []
    	for parent,dirnames,filenames in os.walk(rootdir):   
                cur_dir = []
		str += """<p>parent is: """ + parent + " </p> "
                cur_dir.append(parent)
                sub_dirs = []
		for dirname in  dirnames: 
                        sub_dirs.append(dirname)          
			str += " dirname is " + dirname + " <br> "

                cur_dir.append(sub_dirs)

                files = []
		for filename in filenames: 
                        file = []         
                        file.append(filename)
                        file.append(os.path.join(parent,filename))
                        files.append(file)              #
			str += " filename is: " + filename + " <br> "
			str += " the full name of the file is: " + os.path.join(parent,filename)  + " <br> "
                cur_dir.append(files)
                last_dir = parent.split("/")[-1]
                if last_dir:
                    parent_dir = parent.split(last_dir)[0][0:-1]
                else:
                    parent_dir = ""
                cur_dir.append(parent_dir)
                dir_tree.append(cur_dir)
	return dir_tree

render = web.template.render('templates/', globals={'print_dir':build_array_with_dir})


urls = (
    '/', 'index',
    '/upload', 'upload',
    '/upload_and_store', 'upload_and_store',
)

class index:
    def GET(self):
	#name = 'Bob'    
        i = web.input(name=None)
	return render.index(i.name)

class upload:
    def GET(self):
        return """<html><head></head><body>
<form method="POST" enctype="multipart/form-data" action="">
<input type="file" name="myfile" />
<br/>
<input type="submit" />
</form>
</body></html>"""

    def POST(self):
        x = web.input(myfile={})
        web.debug(x['myfile'].filename) # This is the filename
        web.debug(x['myfile'].value) # This is the file contents
        web.debug(x['myfile'].file.read()) # Or use a file(-like) object
        raise web.seeother('/upload')

class upload_and_store:
    def GET(self):
        web.header("Content-Type","text/html; charset=utf-8")
        return """<html><head></head><body>
<form method="POST" enctype="multipart/form-data" action="">
<input type="file" name="myfile" />
<br/>
<input type="submit" />
</form>
</body></html>"""

    def POST(self):
        x = web.input(myfile={})
        filedir = './upload' # change this to the directory you want to store the file in.
        if 'myfile' in x: # to check if the file-object is created
            filepath=x.myfile.filename.replace('\\','/') # replaces the windows-style slashes with linux ones.
            filename=filepath.split('/')[-1] # splits the and chooses the last part (the filename with extension)
            fout = open(filedir +'/'+ filename,'w') # creates the file where the uploaded file should be stored
            fout.write(x.myfile.file.read()) # writes the uploaded file to the newly created file.
            fout.close() # closes the file, upload complete.
        raise web.seeother('/upload_and_store')



if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()



