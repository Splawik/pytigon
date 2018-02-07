pip3 install -r requirements.txt
cd app_pack
zip -r ../install/app_pack.zip *
cd ..
curl -L -o ./ext_prg/tcc-0.9.26.tar.bz2 http://download.savannah.gnu.org/releases/tinycc/tcc-0.9.26.tar.bz2
tar xjf ./ext_prg/tcc-0.9.26.tar.bz2 -C ./ext_prg/
rm ./ext_prg/tcc-0.9.26.tar.bz2
mv ./ext_prg/tcc-0.9.26 ./ext_prg/tcc
cd ./ext_prg/tcc
./configure --disable-static
make
