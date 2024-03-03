from setuptools import setup, find_packages
import os


def package_files(directory, ext=None):
    paths = []
    for path, directories, filenames in os.walk(directory):
        for filename in filenames:
            if not ext or (ext and filename.endswith(ext)):
                paths.append(os.path.join("..", path, filename))
    return paths


extra_files = package_files("pytigon/static")
extra_files += package_files("pytigon/templates")
extra_files += package_files("pytigon/templates_src")
extra_files += package_files("pytigon/ext_prg")
extra_files += package_files("pytigon/appdata")
extra_files += package_files("pytigon/install")

extra_files += package_files("pytigon/prj")

extra_files.append("pytigon.ini")
extra_files.append("pytigon_splash.jpeg")
extra_files.append("pytigon.svg")
extra_files.append("pytigon.png")
extra_files.append("pytigon.ico")
extra_files.append("ptig")
extra_files.append("../requirements.txt")

with open("requirements.txt") as f:
    tmp = f.read().strip().split("\n")
    install_requires = [pos for pos in tmp if "://" not in pos]
    dependency_links = [pos for pos in tmp if "://" in pos]

setup(
    name="pytigon",
    version="0.240303",
    description="Pytigon",
    author="Sławomir Chołaj",
    author_email="slawomir.cholaj@gmail.com",
    license="LGPLv3",
    packages=find_packages(exclude=["pytigon_gui*", "pytigon_lib*"]),
    package_data={"": extra_files},
    install_requires=install_requires,
    dependency_links=dependency_links,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3",
    zip_safe=False,
    entry_points={
        "console_scripts": [
            "ptig=pytigon.pytigon_run:run",
        ]
    },
)
