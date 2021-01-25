#import os, sys, re
from BBWebFw import backend
#BBlazeWeb
class webApp:
    def __init__(self, name, server):
        self.urls = {}
        self.server = server
        self.name = name
        self.out404 = '<!DOCTYPE html>\n<html lang="en">\n<head>\n    <meta charset="UTF-8">\n    <meta name="viewport" content="width=device-width, initial-scale=1.0">\n    <title>Document</title>\n</head>\n<body>\n    Hello\n</body>\n</html>'
        self.out503 = '<!DOCTYPE html>\n<html lang="en">\n<head>\n    <meta charset="UTF-8">\n    <meta name="viewport" content="width=device-width, initial-scale=1.0">\n    <title>Document</title>\n</head>\n<body>\n    Hello\n</body>\n</html>'
        self.error = {"urlcatcherexists" : "ERR:URL_CATCHER_ALREADY_EXISTS"}
        self.MIMETypes={
                    ".png": "image/png",
                    ".jpg": "image/jpg",
                    ".jpeg": "image/jpeg",
                    ".ico": "image/ico",
                    ".txt": "text/txt",
                    ".html": "text/html",
                    ".css": "text/css",
                    ".js": "text/js",
                }
        backend.api(name, server)

    def __call__(self, environ, start_response):
        return backend.api.__call__(self, environ, start_response)
    
    def catchURL(self, path):
        return backend.api.catchURL(self, path)

    def run(self, app, debug=False, hostAddr="0.0.0.0:8000"):
        backend.api.run(self, app, host=hostAddr)

    def handle_request(self, request):
        return backend.api.handle_request(self, request)
    
    def find_handler(self, request):
        return backend.api.find_handler(self, request)

    def return_external(self, response, domain, uri, mimetype=None):
        return backend.api.return_external(self, response, domain, uri, mimetype)

    def err404(self,response):
        return backend.api.err404(self, response)

    def err503(self,response):
        return backend.api.err404(self, response)

    def setError(self, code, data):
        return backend.api.setError(self, code, data)
        
    def setStaticDir(self, dir_):
        return backend.api.setStaticDir(self, dir_)

    def getFileType(self, f):
        return backend.api.getFileType(self, f)






















'''
def run(self, app, debug=False):
        print("run")
        host = "127.0.0.1"
        port = 6000

        if (self.name).endswith(".py"):
            self.fname = self.name
            self.name = (self.name).replace(".py", "")
        else:
            self.fname = self.name + ".py"
        
        sys.argv = [re.sub(r'(-script\.pyw|\.exe)?$', '', "env/bin/gunicorn"),self.name+':'+ app]
        print(sys.argv)
        if debug: 
            with open(self.fname) as f:
                self.old = f.read()
                while True:
                    print("11")
                    with open(self.fname) as f:
                        if f.read() == self.old:
                            print("12")
                            self.old = f.read()
                            print("changed!!!")

                        time.sleep(5)
        else:
            backend.run()
        
'''