"""
import subprocess

modules = subprocess.Popen("ls States/",shell=True,stdout=subprocess.PIPE)
modulelist = modules.stdout.read().strip().split('\n')
modulelist.remove('__init__.py')
modulelist.remove('State')

for i in modulelist:
    if '.pyc' not in i:
        exec 'from %s import *'%i.replace('.py','')
"""
