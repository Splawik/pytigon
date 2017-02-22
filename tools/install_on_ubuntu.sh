apt install python3.5
apt install python3.5-dev
apt install virtualenv

cd /var
mkdir www
cd /var/www
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

cp  /var/www/pytigon/tools/pytigon-nginx /etc/nginx/sites-available/
ln -s /etc/nginx/sites-available/pytigon-nginx /etc/nginx/sites-enabled/pytigon-nginx

cp  /var/www/pytigon/tools/pytigon-uwsgi.service  /etc/systemd/system/

systemctl enable pytigon-uwsgi

#run
#mysql -uroot -ppassword
#CREATE SCHEMA `pytigon` DEFAULT CHARACTER SET utf8 COLLATE utf8_polish_ci ;

cd /var/www/pytigon
chown -R www-data:www-data .
