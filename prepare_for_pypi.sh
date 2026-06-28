rm -rf /tmp/pytigon
mkdir /tmp/pytigon
cd pytigon
ptig manage_schdevtools prepare_installer_files 
export DATA_PATH=/tmp/pytigon
ptig manage__schdata makeallmigrations
ptig manage__schtools makeallmigrations
ptig manage__schwiki makeallmigrations
ptig manage_schdevtools makeallmigrations
ptig manage_schdevtools migrate
ptig manage_schdevtools createautouser
ptig manage_schdevtools import_projects
ptig manage_schpytigondemo makeallmigrations
ptig manage_schpytigondemo migrate
ptig manage_schpytigondemo createautouser
ptig manage_schmanage makeallmigrations
ptig manage_schmanage migrate
ptig manage_schmanage createautouser
ptig manage_schwebtrapper makeallmigrations
ptig manage_schwebtrapper migrate
ptig manage_schwebtrapper createautouser
ptig manage_scheditor makeallmigrations
ptig manage_scheditor migrate
ptig manage_scheditor createautouser
ptig manage_schportal makeallmigrations
ptig manage_schportal migrate
ptig manage_schportal createautouser
echo -n "[DEFAULT]
GEN_TIME='" > /tmp/pytigon/install.ini
echo -n $(date +"%Y-%m-%d %H:%M:%S") >> /tmp/pytigon/install.ini
echo "'" >> /tmp/pytigon/install.ini
rm ./pytigon/install/.pytigon.zip
7z a $PWD/install/.pytigon.zip /tmp/pytigon/*
cd ..
