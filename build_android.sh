#p4a apk --private $HOME/prj/pytigon --dist-name=pytigon --ndk-dir='/home/sch/Android/crystax-ndk-10.3.2' --arch=x86 --android-api=21 --package=tk.pytigon --name "Pytigon" --version 0.1 --bootstrap=webview \
    --requirements=python3crystax,Django,django-crispy-forms,ldap3,django_python3_ldap,django_select2,whitenoise,fpdf,html5lib,markdown2,wsgi_intercept,openpyxl,httpie,PyDispatcher,polib,django-appconf,fs \
    --permission=INTERNET --permission=READ_EXTERNAL_STORAGE --permission=WRITE_EXTERNAL_STORAGE --permission=INSTALL_SHORTCUT \
    --blacklist=./blacklist.txt --whitelist=./whitelist.txt \
    --icon=$HOME/prj/pytigon/pytigon.png --presplash=$HOME/prj/pytigon/pytigon_splash.jpeg
#fs==0.5.4,lxml

p4a apk --private $HOME/prj/pytigon --dist-name=pytigon --ndk-dir='/home/sch/Android/crystax-ndk-10.3.2' --arch=armeabi-v7a --android-api=21 --package=tk.pytigon --name "Pytigon" --version 0.1 --bootstrap=schwebview \
    --requirements=python3crystax,Django,django-crispy-forms,ldap3,django_python3_ldap,django_select2,whitenoise,fpdf,html5lib,markdown2,wsgi_intercept,openpyxl,httpie,PyDispatcher,polib,django-appconf,fs,cherrypy,cheroot,portend,tempora \
    --permission=INTERNET --permission=READ_EXTERNAL_STORAGE --permission=WRITE_EXTERNAL_STORAGE --permission=INSTALL_SHORTCUT \
    --blacklist=./blacklist.txt --whitelist=./whitelist.txt \
    --icon=$HOME/prj/pytigon/pytigon.png --presplash=$HOME/prj/pytigon/pytigon_splash.png