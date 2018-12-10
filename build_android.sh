docker run \
    --interactive \
    --tty \
    --volume "$HOME/prj/pytigon":/home/user/prj/pytigon \
    --volume "$HOME/.local":/home/user/.local \
    --volume "$HOME/prj/python-for-android/pythonforandroid/recipes":/home/user/pythonforandroid/recipes \
    --volume "$HOME/prj/python-for-android/pythonforandroid/bootstraps":/home/user/pythonforandroid/bootstraps \
    --volume "$HOME/prj/python-for-android/home_data/":/home/user/home_data \
    p4a sh -c '. venv/bin/activate \
        && cd prj/pytigon \
        && bash build_android_entrypoint.sh'

adb uninstall cloud.pytigon
adb install $HOME/.local/share/python-for-android/dists/pytigon/build/outputs/apk/pytigon-debug.apk
