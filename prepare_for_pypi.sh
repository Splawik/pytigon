rm -rf /tmp/pytigon
mkdir /tmp/pytigon
cd pytigon
#python ptig.py manage_schdevtools prepare_installer_files 
export DATA_PATH=/tmp/pytigon
python ptig.py manage__schdata makeallmigrations
python ptig.py manage__schtools makeallmigrations
python ptig.py manage__schwiki makeallmigrations
python ptig.py manage_schdevtools makeallmigrations
python ptig.py manage_schdevtools migrate
python ptig.py manage_schdevtools createautouser
python ptig.py manage_schdevtools import_projects
python ptig.py manage_schpytigondemo makeallmigrations
python ptig.py manage_schpytigondemo migrate
python ptig.py manage_schpytigondemo createautouser
python ptig.py manage_schsetup makeallmigrations
python ptig.py manage_schsetup migrate
python ptig.py manage_schsetup createautouser
python ptig.py manage_schwebtrapper makeallmigrations
python ptig.py manage_schwebtrapper migrate
python ptig.py manage_schwebtrapper createautouser
python ptig.py manage_scheditor makeallmigrations
python ptig.py manage_scheditor migrate
python ptig.py manage_scheditor createautouser
python ptig.py manage_schportal makeallmigrations
python ptig.py manage_schportal migrate
python ptig.py manage_schportal createautouser
echo -n "[DEFAULT]
GEN_TIME='" > /tmp/pytigon/install.ini
echo -n $(date +"%Y-%m-%d %H:%M:%S") >> /tmp/pytigon/install.ini
echo "'" >> /tmp/pytigon/install.ini
rm ./pytigon/install/.pytigon.zip
7z a $PWD/install/.pytigon.zip /tmp/pytigon/*
cd ..
