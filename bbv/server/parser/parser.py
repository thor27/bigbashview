from chameleon import PageTemplate
import subprocess
import ast

def sh_expression(command):
    def compiler(target, engine):
        po = subprocess.Popen(command.encode('utf-8'), stdin=None, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        (stdout,stderr) = po.communicate()
        
        value = ast.Str(stdout)
        return [ast.Assign(targets=[target], value=value)]
    return compiler

PageTemplate.expression_types['sh'] = sh_expression

print PageTemplate("""

<div tal:content="sh:ls">hello</div>

""")()