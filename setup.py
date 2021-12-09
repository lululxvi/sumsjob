import io
import os
from setuptools import setup
from setuptools import find_packages


def read(rel_path: str) -> str:
    here = os.path.abspath(os.path.dirname(__file__))
    # intentionally *not* adding an encoding option to open, See:
    #   https://github.com/pypa/virtualenv/issues/201#issuecomment-3145690
    with open(os.path.join(here, rel_path)) as fp:
        return fp.read()


def get_version(rel_path: str) -> str:
    for line in read(rel_path).splitlines():
        if line.startswith("__version__"):
            # __version__ = "0.11.2"
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    raise RuntimeError("Unable to find version string.")


version = get_version("sumsjob/__about__.py")

with io.open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="SumsJob",
    version=version,
    description="A simple Linux command-line utility which submits a job to one of the multiple servers",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Lu Lu",
    author_email="lululxvi@gmail.com",
    url="https://github.com/lululxvi/sumsjob",
    download_url="https://github.com/lululxvi/deepxde/tarball/v" + version,
    license="GPL-3.0",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Utilities",
    ],
    keywords=[
        "Command-line utility",
        "Multiple servers",
        "GPU",
        "Job submission",
    ],
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "gpuresource=sumsjob.gpuresource:main",
            "submit=sumsjob.submit:main",
        ]
    },
)
