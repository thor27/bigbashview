import web
import sys
import socket
import threading
import inspect

import views
try:
    from bbv import globals as globaldata
except ImportError:
    import globaldata

class Server(threading.Thread):
    def _get_subclasses(self, classes=None):
        """ Get subclasses recursively """
        if classes is None:
            classes = views.url_handler.__subclasses__()
        result = classes
        for cls in classes:
            result += self._get_subclasses(cls.__subclasses__())
        return result
        
    def get_urls(self):
        """ Return supported URLs. """
        classes = self._get_subclasses()
        result = []
        for cls in classes:
            result.append(cls.__url__)
            result.append(cls.__name__)
        return tuple(result)
    
    def get_classes(self):
        """ Return all view classes. """
        classes = self._get_subclasses()
        result = {}
        for cls in classes:
            result[cls.__name__] = cls
        return result
    
    def run(self):
        """ Run the webserver """
        ip = globaldata.ip()
        port = globaldata.port()
        sys.argv = [ sys.argv[0], '' ]
        sys.argv[1] = ':'.join((ip,str(port)))
        
        urls = self.get_urls()
        classes = self.get_classes()
        app = web.application(urls, classes)
        app.run()
        
    def stop(self):
        pass

def run_server(ip='127.0.0.1',background=True):
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
    
    globaldata.ip = lambda: ip
    globaldata.port = lambda: port
    
    server = Server()
    
    if background:
        server.daemon = True
        web.config.debug = False
        server.start()
    else:
        web.config.debug = True
        server.run()

if __name__ == "__main__":
    run_server(background=False)
