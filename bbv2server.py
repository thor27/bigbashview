import web
import subprocess
import shlex
import os
import sys
import socket
import threading
from urlparse import parse_qs

class url_handler:
    def GET(self, name=''):
        qs = parse_qs(web.ctx.query[1:])
        return self.called(name,qs)
    
    def POST(self, name=''):
        qs = parse_qs(web.data())
        return self.called(name,qs)
    
    def called(self,options,query):
        raise NotImplementedError

class about(url_handler):
    def called(self,options,query):
        return '<html><body><h1>Welcome to BigBashView 2!</h1></body></body>'

class content(url_handler):        
    def called(self,options,query):
        with open(options) as arq:
            return arq.read()

class execute(url_handler):
    def get_env(self,query, prefix='p_'):
        join_options = lambda opt: (prefix+opt[0],";".join([x.replace(';','\;') for x in opt[1]]))
        return dict(map(join_options, query.items()))
        
    def _execute(self, command, wait=False, extra_env={}):
        env = os.environ
        env.update(extra_env)
        
        po = subprocess.Popen(command, stdin=None, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, env=env)
        if wait:
            return po.communicate()    
            
    def called(self,options,query):         
        (stdout, stderr) = self._execute(options, wait=True,extra_env=self.get_env(query))
        return stdout
        
class execute_background(execute):        
    def called(self,options,query):
        self._execute(options,extra_env=self.get_env(query))
        return ''

class Server ( threading.Thread ):
    def run(self):
        urls = (
            '/content\$(.*)', 'content',
            '/execute\$(.*)', 'execute', 
            '/execute_background\$(.*)', 'execute_background',  
            '/', 'about', 
        )
        app = web.application(urls, globals())
        web.config.debug = False
        app.run()
        
    def stop(self):
        pass

def run_server(ip='127.0.0.1'):
    soc = socket.socket()
    for port in range(9000,9100):
        try:
            soc.bind((ip,port))
            soc.close()
            break
        except socket.error, e:
            if e[0] != 98:
                raise socket.error(e)
            print 'Port %d already in use, trying next one' %port
    
    sys.argv = [ sys.argv[0], '' ]
    sys.argv[1] = ':'.join((ip,str(port)))
    thread = Server()
    thread.daemon = True
    thread.start()

if __name__ == "__main__":
    run_server()
