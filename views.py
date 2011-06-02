from urlparse import parse_qs
import subprocess
import os
import globaldata
import web

class url_handler(object):
    __url__ = '/'
    
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
    __url__='/content\$(.*)'
    def called(self,options,query):
        with open(options) as arq:
            return arq.read()

class execute(url_handler):
    __url__='/execute\$(.*)'
    
    def get_env(self,query, prefix='bbv_'):
        join_options = lambda opt: (prefix+opt[0],";".join([x.replace(';','\;') for x in opt[1]]))
        return dict(map(join_options, query.items()))
        
    def _execute(self, command, wait=False, extra_env={}):
        env = os.environ.copy()
        env['bbv_ip']=globaldata.ip()
        env['bbv_port']=globaldata.port()
        env.update(extra_env)
        
        po = subprocess.Popen(command, stdin=None, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, env=env)
        if wait:
            return po.communicate()    
            
    def called(self,options,query):         
        (stdout, stderr) = self._execute(options, wait=True,extra_env=self.get_env(query))
        return stdout
        
class execute_background(execute): 
    __url__='/execute_background\$(.*)'
    def called(self,options,query):
        self._execute(options,extra_env=self.get_env(query))
        return ''