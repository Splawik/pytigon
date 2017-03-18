#!/usr/bin/env bash
if [ "$(expr substr $(uname -s) 1 5)" == "Linux" ]; then
    virtualenv --python=python3.5 python
    ./python/bin/pip install  -r requirements.txt
    curl -L -o ./ext_prg/tcc-0.9.26.tar.bz2 http://download.savannah.gnu.org/releases/tinycc/tcc-0.9.26.tar.bz2
    tar xjf ./ext_prg/tcc-0.9.26.tar.bz2 -C ./ext_prg/
    rm ./ext_prg/tcc-0.9.26.tar.bz2
    mv ./ext_prg/tcc-0.9.26 ./ext_prg/tcc
    cd ./ext_prg/tcc
    ./configure --disable-static
    make
else 
    curl -o python-3.6.0-embed-win32.zip https://www.python.org/ftp/python/3.6.0/python-3.6.0-embed-win32.zip
    mkdir python
    unzip python-3.6.0-embed-win32.zip -d ./python
    rm python-3.6.9-embed-win32.zip
    unzip ./python/python35.zip -d ./python/Lib
    rm ./python/python35.zip
    curl -o ./python/get-pip.py https://bootstrap.pypa.io/get-pip.py
    ./python/python ./python/get-pip.py
    ./python/Scripts/pip install -r requirements.txt
    ./python/Scripts/pip install -r requirements.txt
    curl -L -o ./python/lxml-3.4.4-cp35-none-win32.whl https://pypi.anaconda.org/giumas/simple/lxml/3.4.4/lxml-3.4.4-cp35-none-win32.whl
    ./python/Scripts/pip install ./python/lxml-3.4.4-cp35-none-win32.whl
    curl -L -o ext_lib_cli_win.zip http://pytigon.tk/download/ext_lib_cli_win.zip
    unzip ext_lib_cli_win.zip
    rm ext_lib_cli_win.zip    
    curl -L -o ./ext_prg/tcc-0.9.26-win32-bin.zip http://download.savannah.gnu.org/releases/tinycc/tcc-0.9.26-win32-bin.zip
    unzip ./ext_prg/tcc-0.9.26-win32-bin.zip -d ./ext_prg
    rm ./ext_prg/tcc-0.9.26-win32-bin.zip
    curl -L -o ./ext_prg/LinkRes2Exe.zip http://pytigon.tk/download/LinkRes2Exe.zip
    unzip ./ext_prg/LinkRes2Exe.zip -d ./ext_prg
    rm ./ext_prg/LinkRes2Exe.zip
    ./ext_prg/tcc/tcc pytigon.c -ladvapi32
    ./ext_prg/LinkRes2Exe pytigon.res pytigon.exe
    ./ext_prg/tcc/tcc pytigon_cmd.c -ladvapi32
    ./ext_prg/LinkRes2Exe pytigon.res pytigon_cmd.exe
    curl -L -o ./install/vcredist_x86.exe http://pytigon.tk/download/vcredist_x86.exe
fi
