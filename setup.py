from setuptools import setup, find_packages
import os


def package_files(directory, ext=None):
    paths = []
    for (path, directories, filenames) in os.walk(directory):
        for filename in filenames:
            if not ext or (ext and filename.endswith(ext)):
                paths.append(os.path.join("..", path, filename))
    return paths


extra_files = package_files("pytigon/static")
extra_files += package_files("pytigon/templates")
extra_files += package_files("pytigon/ext_prg")
extra_files += package_files("pytigon/appdata")
extra_files += package_files("pytigon", ".html")
extra_files += package_files("pytigon/install")
extra_files += package_files("pytigon/prj")
extra_files.append("pytigon.ini")
extra_files.append("pytigon_splash.jpeg")
extra_files.append("pytigon.svg")
extra_files.append("pytigon.png")
extra_files.append("pytigon.ico")
extra_files.append("ptig")


setup(
    name="pytigon",
    version="0.97",
    description="Pytigon",
    author="Sławomir Chołaj",
    author_email="slawomir.cholaj@gmail.com",
    license="LGPLv3",
    packages=find_packages(exclude=["pytigon_gui*", "pytigon_lib*"]),
    package_data={"": extra_files},
    scripts=["pytigon/ptig"],
    install_requires=[
        "pytigon-lib",
        "Twisted[tls,http2]",
        "channels",
        "asgiref",
        # "django_python3_ldap",
        "django-bootstrap4",
        "django_select2",
        "django-cors-headers",
        "django-bulk_update",
        "dj-database-url",
        "dj-email-url",
        "django-mptt",
        "django_polymorphic",
        "django-mailer",
        "django_redis",
        "django-cache-url",
        "django-allauth",
        "django-sql-explorer",
        "graphene-django",
        "easy_thumbnails",
        "whitenoise",
        "markdown2",
        "ldap3",
        "pypyodbc",
        "daphne",
        "polib",
        "hypercorn",
        "xonsh",
        # "git+https://github.com/Splawik/django-filer.git@feature/django2-support",
        "Transcrypt",
        "netifaces",
        "cython",
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3",
    zip_safe=False,
)

# print(extra_files)
# print(find_packages(exclude=["pytigon_gui*", "pytigon_lib*"]))
