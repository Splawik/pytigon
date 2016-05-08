if [ "$(expr substr $(uname -s) 1 5)" == "Linux" ]; then
    ./python/bin/pip install  -r requirements.txt
    ./python/bin/python ./ext_prg/http -dco ./ext_prg/tcc-0.9.26.tar.bz2 http://download.savannah.gnu.org/releases/tinycc/tcc-0.9.26.tar.bz2
    tar xjf ./ext_prg/tcc-0.9.26.tar.bz2 -C ./ext_prg/
    mv ./ext_prg/tcc-0.9.26 ./ext_prg/tcc
    cd ./ext_prg/tcc
    ./configure --disable-static
    make
else 
    curl -o python-3.5.1-embed-win32.zip https://www.python.org/ftp/python/3.5.1/python-3.5.1-embed-win32.zip
    mkdir python
    unzip python-3.5.1-embed-win32.zip -d ./python
    unzip ./python/python35.zip -d ./python/Lib
    rm ./python/python35.zip
    curl -o ./python/get-pip.py https://bootstrap.pypa.io/get-pip.py
    ./python/python ./python/get-pip.py
    ./python/Scripts/pip install -r requirements.txt
    curl -L -o ./python/lxml-3.4.4-cp35-none-win32.whl https://pypi.anaconda.org/giumas/simple/lxml/3.4.4/lxml-3.4.4-cp35-none-win32.whl
    ./python/Scripts/pip install ./python/lxml-3.4.4-cp35-none-win32.whl
    curl -L -o ./ext_prg/tcc-0.9.26-win32-bin.zip http://download.savannah.gnu.org/releases/tinycc/tcc-0.9.26-win32-bin.zip
    unzip ./ext_prg/tcc-0.9.26-win32-bin.zip -d ./ext_prg
fi
