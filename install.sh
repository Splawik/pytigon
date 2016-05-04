pip3 install --target=./ext_lib -r requirements.txt

if [ "$(expr substr $(uname -s) 1 5)" == "Linux" ]; then
    python3 ./ext_lib/http -dco ./ext_prg/tcc-0.9.26.tar.bz2 http://download.savannah.gnu.org/releases/tinycc/tcc-0.9.26.tar.bz2
    tar xjf ./ext_prg/tcc-0.9.26.tar.bz2 -C ./ext_prg/
    mv ./ext_prg/tcc-0.9.26 ./ext_prg/tcc
    cd ./ext_prg/tcc
    ./configure --disable-static
    make
else 
    python3 ./ext_lib/http -dco ./ext_prg/tcc-0.9.26-win32-bin.zip http://download.savannah.gnu.org/releases/tinycc/tcc-0.9.26-win32-bin.zip
    python3 -c "import zipfile;zip_ref = zipfile.ZipFile('./ext_prg/tcc-0.9.26-win32-bin.zip', 'r');zip_ref.extractall('./ext_prg/');zip_ref.close()"
fi
