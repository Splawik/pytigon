import os, sys

base_path = __file__.replace("wsgi.py", "")
print(base_path)    
if base_path == "":
    base_path = "./"
else:
    os.chdir(base_path)

sys.path.insert(0,base_path)
sys.path.insert(0,base_path + "ext_lib")
sys.path.insert(0,base_path + "app_pack/")


import schdevtools.wsgi 

def application(environ, start_response):
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>", environ, start_response)
    return schdevtools.wsgi.application(environ, start_response)

if __name__ == '__main__': 
    from schlib.schdjangoext.server import run_server
    run_server('0.0.0.0', 8080)
