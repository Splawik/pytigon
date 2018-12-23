if [ ! -d ./pytigon  ]; then
    git clone https://github.com/Splawik/pytigon.git
    mkdir pytigon/_android_src/recipes/none
else
    cd pytigon
    git pull
    cd ..
fi

if [ ! -d ./python-for-android  ]; then
    git clone https://github.com/kivy/python-for-android.git
    yes | cp pytigon/install/android/Dockerfile python-for-android/Dockerfile
    cd python-for-android
    docker build --tag p4apy3 .
    mkdir home_data
    cd ..
fi

if [ ! -d ./venv  ]; then
    virtualenv --python=python3.7 venv
    venv/bin/python -m pip install -r pytigon/install/android/requirements.txt 
else
    venv/bin/python -m pip install --upgrade -r pytigon/install/android/requirements.txt 
fi 

yes | cp -Rf venv/lib/python3.7/site-packages pytigon/_android

cd pytigon
bash build_android.sh
cd ..
