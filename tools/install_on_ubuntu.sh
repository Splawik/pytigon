apt install python3.5
apt install python3.5-dev
apt install virtualenv
apt install git
apt install libxml2-dev
apt install libxslt1-dev
apt install zlib1g-dev
apt install libffi-dev
apt install libjpeg-dev


cd /home
mkdir www-data
cd /home/www-data
git clone  https://github.com/Splawik/pytigon.git
cd pytigon
bash install.sh

python/bin/pip install uwsgi
python/bin/pip install asgi_redis
python/bin/pip install PyMySql

apt install nginx
apt install mysql-server
apt install redis-server

#Add:
#    iptables -t nat -A PREROUTING -p tcp --dport 80 -j REDIRECT --to-port 8080
#to /etc/rc.local

cp  /home/www-data/pytigon/tools/pytigon-nginx /etc/nginx/sites-available/
ln -s /etc/nginx/sites-available/pytigon-nginx /etc/nginx/sites-enabled/pytigon-nginx

cp  /home/www-data/pytigon/tools/pytigon-uwsgi.service  /etc/systemd/system/

systemctl enable pytigon-uwsgi

#run
#mysql -uroot -ppassword
#CREATE SCHEMA `pytigon` DEFAULT CHARACTER SET utf8 COLLATE utf8_polish_ci ;

cd /home/www-data/pytigon
chown -R www-data:www-data .
