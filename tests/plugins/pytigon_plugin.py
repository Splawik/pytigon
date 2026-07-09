import os


def pytest_configure(config):
    os.environ["SECRET_KEY"] = "anawa"
    os.environ["SCRIPT_MODE"] = "1"
    os.environ["DJANGO_SETTINGS_MODULE"] = "settings_app"

    from pytigon.django_min_init import init

    init(prj="_schtest", pytigon_standard=True)


def pytest_unconfigure(config):
    pass
