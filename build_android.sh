export ANDROIDSDK="$HOME/Android/"
export ANDROIDNDK="$HOME/Android/crystax-ndk-10.3.2/"
export ANDROIDAPI="21" 

bash $HOME/prj/pytigon/_android_src/libpytigon2/gradlew build
cp $HOME/prj/pytigon/_android_src/libpytigon2/build/intermediates/bundles/default/classes.jar $HOME/prj/pytigon/install/android/pytigon.jar

p4a apk --private $HOME/prj/pytigon --dist-name=pytigon  --package=cloud.pytigon --arch=armeabi-v7a --name "Pytigon" --version 0.1 --bootstrap=sdl2 \
    --requirements=android,sdl2,kivy,python3crystax,django-bootstrap4,ldap3,django_python3_ldap,django_select2,whitenoise,fpdf,html5lib,markdown2,wsgi_intercept,openpyxl,httpie,PyDispatcher,polib,django-appconf,fs,portend,tempora,cheroot,pillow,lxml,transcrypt,pyexcel_odsr,pyexcel_io\
,lml,chardet,django-cors-headers,jdcal\
    --permission=INTERNET --permission=READ_EXTERNAL_STORAGE --permission=WRITE_EXTERNAL_STORAGE --permission=INSTALL_SHORTCUT \
    --blacklist=./blacklist.txt --whitelist=./whitelist.txt \
    --icon=$HOME/prj/pytigon/pytigon.png --presplash=$HOME/prj/pytigon/pytigon_splash.jpeg \
    --service=pytigon:pytigon_android_service.py \
    --add-jar=$HOME/prj/pytigon/install/android/pytigon.jar 
    

adb uninstall cloud.pytigon
adb install $HOME/.local/share/python-for-android/dists/pytigon/build/outputs/apk/pytigon-debug.apk
