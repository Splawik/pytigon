import os
import sys
#import traceback
#import site
#import atexit
import tempfile
import re

from transcrypt import __main__ as tmain

programDir = os.getcwd () .replace ('\\', '/')
transpilerDir = os.path.dirname (os.path.abspath (tmain.__file__)) .replace ('\\', '/')
modulesDir = '{}/modules'.format (transpilerDir)
tempDir = tempfile.gettempdir()

try:
    sys.path.remove (transpilerDir)	
except:
    pass
                                                    
sys.path += [modulesDir]
sys.modules.pop ('org', None)	

from org.transcrypt import utils
from org.transcrypt import compiler

utils.nrOfExtraLines = 0
utils.extraLines = ""

def _log (always, *args):
    pass

utils.log = _log

def compile(python_code, temp_dir=None):
    global tempDir

    if temp_dir:
        tmp = temp_dir
    else:
        tmp = tempDir

    compilerPath = [programDir, modulesDir, tmp] + sys.path

    src = os.path.join(tmp, "input.py")
    dest = os.path.join(os.path.join(tmp, "__javascript__"), "input.mod.js")

    if os.path.exists(dest):
        os.remove(dest)

    with open(src, "wt") as pyinput:
        pyinput.write(python_code)

    x = {
        'source': src, 
        'anno': False, 
        'build': False, 
        'complex': False,
        'docat': False, 
        'dcheck': False, 
        'dassert': False, 
        'dextex': False, 
        'dmap': False, 
        'dtree': False, 
        'dstat': False, 
        'esv': None, 
        'fcall': False, 
        'gen': False,
        'iconv': False, 
        'jskeys': False, 
        'jsmod': False, 
        'kwargs': False, 
        'license': False, 
        'map': False, 
        'nomin': True, 
        'opov': False, 
        'parent': None, 
        'run': False, 
        'symbols': None, 
        'tconv': False, 
        'verbose': False, 
        'ext': None, 
        'star': False,
        'keycheck': False,
    }

    utils.commandArgs.__dict__.update (x)

    __symbols__ = []
    __symbols__.append ('__py{}.{}__'.format (* sys.version_info [:2]))
    #if utils.commandArgs.esv:
    #    __symbols__.append ('__esv{}__'.format (utils.commandArgs.esv))
    #else:
    __symbols__.append ('__esv{}__'.format (utils.defaultJavaScriptVersion))

    error = False
    try:
        compiler.Program (compilerPath, __symbols__)
        with open(dest,"rt") as pyoutput:
            ret = pyoutput.read()        
            s = ret.split('(function () {\n', 1)[1]
            s = s.rsplit('}) ();', 1)[0]            
            
            tab = []
            for line in s.split("\n"):
                tab.append(line[2:])
            ret = "\n".join(tab)
            
    except Exception as exception:
        error = True
        tab = []
        print(str(exception))
        for line in str(exception).split("\n"):
            if line.startswith('Error in program'):                
                m = re.search(".*line (\d*):(.*)", line)
                if m:
                    try:
                        row = int(m.groups()[0]) - 1
                        description = m.groups()[1]
                        tab.append("Python to javascript compile error:" + description)
                        tab.append("")
                        tab.append("code:")
                        lines = python_code.split('\n')
                        start = row - 4
                        end = row + 4
                        if start < 0:
                            start = 0
                        if end >= len(lines):
                            end = len(lines) - 1
                        for i in range(start, end):
                            if row == i:
                                tab.append("====>" + lines[i])
                            else:
                                tab.append("     " + lines[i])
                        tab.append("")
                    except:
                        tab.append(line)
                else:
                    tab.append(line)
                    
        ret = "\n".join(tab)
        
    return (error, ret)
