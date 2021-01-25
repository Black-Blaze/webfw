from webob import Request, Response
#from BBWebFw.FileRenderer import Template
import inspect
import urllib.request as httpRequest
import os, sys, re, datetime
from gunicorn.app.wsgiapp import run 

class api:
    """
    docstring
    """

    def __init__(wrapper, name, server):
        wrapper.urls = {}
        wrapper.server = server
        wrapper.name = name
        wrapper.out404 = '<!DOCTYPE html>\n<html lang="en">\n<head>\n    <meta charset="UTF-8">\n    <meta name="viewport" content="width=device-width, initial-scale=1.0">\n    <title>Document</title>\n</head>\n<body>\n    Hello\n</body>\n</html>'
        wrapper.error = {"urlcatcherexists" : "ERR:URL_CATCHER_ALREADY_EXISTS"}
    
    def __call__(wrapper, environ, start_response):
        request = Request(environ)

        response = wrapper.handle_request(request)
        return response(environ, start_response)

    def getFileType(wrapper, f):
        wrapper.extList={
                    ".css": "text/css",
                    ".html": "text/html",
                    ".htm": "text/html",
                    ".ico": "image/vnd.microsoft.icon",
                    ".js": "text/javascript",
                    ".jpg": "image/jpeg",
                    ".jpeg": "image/jpeg",
                    ".png": "image/png",
                    ".txt": "text/plain",
                    ".map": "application/json",
                }
        wrapper.noText={
                    ".ico": "image/ico",
                    ".jpg": "image/jpg",
                    ".jpeg": "image/jpeg",
                    ".png": "image/png",
                }
        fileType = wrapper.extList[os.path.splitext(f)[1]]

        return fileType, fileType in wrapper.noText.values()

    def handle_request(wrapper, request):
        #user_agent = request.environ.get('HTTP_USER_AGENT')
        response = Response()
        response.status_code = 200
        response.text = "Blank"
        
        handler = wrapper.find_handler(request)

        if handler is not None:
            if(inspect.isclass(handler)):
                handler = getattr(handler(), request.method.lower(), None)
                if handler is not None:
                    handler(response)
                else:
                    wrapper.err503(response)
            else:
                handler(response)
        else:
            try:
                try:
                    FileType ,noText = wrapper.getFileType(request.path)
                    print(FileType, noText)
                    response.content_type = FileType
                    if(noText):
                        response.body = open(os.path.join(wrapper.staticDir,"static"+request.path), "rb").read()
                    else:
                        response.text = open(os.path.join(wrapper.staticDir,"static"+request.path)).read()
                except Exception as e:
                    print(e)
                    wrapper.err404(response)
            except Exception as e:
                print(e)
                response.text = "Well My Work Was Not Clean Enough, but...<br><b>Thats A Server Problem</b>"
                response.status_code = 500

        with open("access-log.txt", "a") as f:
            f.write("\n")
            f.write((request.remote_addr + ' - - ['+(datetime.date.today().__str__())+' '+(datetime.datetime.now().strftime("%H:%M:%S"))+ ']' + request.method))
            f.write("\n")
            f.write("Request" + ":" + request.path)
            f.write("\n")
            f.write("Response Code" + ":" + response.status_code.__str__())
            f.write("\n")
        return response

    def catchURL(wrapper, path):
        def wrapperFunction(handler):
            if(not(wrapper.urls.__contains__(path))):
                wrapper.urls[path] = handler
                print(wrapper.urls[path])
                return handler
            else:
                print("hi")
                raise AssertionError(wrapper.error["urlcatcherexists"])
                return wrapper.error["urlcatcherexists"]

        return wrapperFunction

    def find_handler(wrapper, request):
        for path, handler in wrapper.urls.items():
            if path == request.path:
                return handler

    def return_external(wrapper, response, domain, uri, mimetype=None):
        FileType ,noText = wrapper.getFileType(uri)
        if mimetype == None:
            response.content_type = FileType 

        if(noText):
            response.body = httpRequest.urlopen(domain+uri).read()            
        else:
            try:
                response.text = httpRequest.urlopen(domain+uri).read()
            except:          
                response.text = httpRequest.urlopen(domain+uri).read().decode()
        pass


    def err404(wrapper,response):
        response.status_code = 404
        response.text = wrapper.out404

    def err503(wrapper,response):
        response.status_code = 404
        response.text = wrapper.out503

    def setError(wrapper, code, data):
        if code == 404:
            wrapper.out404 = data
        elif code == 503:
            wrapper.out503 = data
        else:
            raise Exception("Invalid Error Code")

    def setStaticDir(wrapper, dir_):
        wrapper.staticDir = dir_

    def run(wrapper, app, host):
        print("run")

        if (wrapper.name).endswith(".py"):
            wrapper.fname = wrapper.name
            wrapper.name = (wrapper.name).replace(".py", "")
        else:
            wrapper.fname = wrapper.name + ".py"
        
        sys.argv = [re.sub(r'(-script\.pyw|\.exe)?$', '', "env/bin/gunicorn"),wrapper.name+':'+ app, "-b", host]
        print(sys.argv)
        sys.exit(run())