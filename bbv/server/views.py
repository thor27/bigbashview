from urlparse import parse_qs
import subprocess
import os
import web
try:
    from bbv import globals as globaldata
except ImportError:
    import globaldata

class url_handler(object):
    __url__ = '/'
    
    def GET(self, name=''):
        return self.parse_and_call(web.ctx.query[1:],name)
        
    def POST(self, name=''):
        return self.parse_and_call(web.data(),name)
        
    def parse_and_call(self,qs,name):
        qs = parse_qs(qs)
        options,content = self._get_set_default_options(name)
        return self.called(options,content,qs)
    
    def _get_set_default_options(self,options):
        if not options:
            return []
        
        optlist = options.split('$')
        content = '$'.join(optlist[1:])
        optlist = optlist[0]
        if 'plain' in optlist:
            web.header('Content-Type', 'text/plain')
        else:
            web.header('Content-Type', 'text/html')
        
        return optlist,content
    
    def called(self,options,query):
        raise NotImplementedError

class about(url_handler):
    def called(self,*args):
        return '<html><body><h1>Welcome to BigBashView 2!</h1></body></html>'

class content(url_handler):        
    __url__='/content(.*)'
    def called(self,options,content,query):
        with open(content) as arq:
            return arq.read()

class execute(url_handler):
    __url__='/execute(.*)'
    
    def get_env(self,query, prefix='bbv_'):
        join_options = lambda opt: (prefix+opt[0],";".join([x.replace(';','\;') for x in opt[1]]))
        return dict(map(join_options, query.items()))
        
    def _execute(self, command, wait=False, extra_env={}):
        env = os.environ.copy()
        env['bbv_ip']=str(globaldata.ADDRESS())
        env['bbv_port']=str(globaldata.PORT())
        env.update(extra_env)
        
        po = subprocess.Popen(command.encode('utf-8'), stdin=None, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, env=env)
        if wait:
            return po.communicate()
        return ('','')
            
    def called(self,options,content,query):
        wait = not 'background' in options
        (stdout, stderr) = self._execute(content, wait=wait,extra_env=self.get_env(query))
        return stdout
        