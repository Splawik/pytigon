from setuptools import Extension
from setuptools import setup

setup(
    name="c_sum",
    version="1.0.0",
    python_requires=">=3.7.15",
    build_zig=True,
    ext_modules=[
        Extension(
            "c_sum",
            [
                "sum.c",
            ],
            include_dirs = [ "/usr/lib/python3.10/", ],
        )
    ],
    setup_requires=["setuptools-zig"],
)
