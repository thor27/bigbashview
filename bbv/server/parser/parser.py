from chameleon import PageTemplate
from chameleon.codegen import template
from chameleon.astutil import Symbol
import subprocess
import ast
import os

def execute(command,context,context_ext):
    env = os.environ.copy()
    context.update(context_ext)
    for value in context:
        env[value] = str(context[value])
    
    po = subprocess.Popen(command.encode('utf-8'), stdin=None, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, env=env)
    (stdout,stderr) = po.communicate()
    return stdout

def sh_expression(command):
    def compiler(target, engine):
        value = template(
            "EXECUTE(NAME,econtext,rcontext)",
            EXECUTE=Symbol(execute),
            NAME=ast.Str(s=command),
            mode="eval",
            )
        return [ast.Assign(targets=[target], value=value)]
    return compiler

        
PageTemplate.expression_types['sh'] = sh_expression

def parse(template):
    return PageTemplate(template)()