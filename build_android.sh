docker run \
    --interactive \
    --tty \
    --volume "$HOME/prj/pytigon-android/pytigon":/home/user/prj/pytigon \
    --volume "$HOME/.local":/home/user/.local \
    --volume "$HOME/prj/pytigon-android/python-for-android/home_data/":/home/user/home_data \
    p4apy3 sh -c '. venv/bin/activate \
        && cd prj/pytigon \
        && bash build_android_entrypoint.sh'

adb uninstall cloud.pytigon
adb install $HOME/.local/share/python-for-android/dists/pytigon/build/outputs/apk/debug/pytigon-debug.apk

