import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    
   
    python_requires=">=3.6",
)





from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.0.3'
DESCRIPTION = 'Mero Share API'
LONG_DESCRIPTION = 'A package that allows you to use MeroShare through code?'

# Setting up
setup(
   name="MeroShareAPI",
    version="0.0.3",
    author="Niraj Ghimire",
    author_email="nirajghimirexyz@gmail.com",
    description="Mero Share API",
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
     url="https://github.com/punkholic/meroshare_API",
    project_urls={
        "Bug Tracker": "https://github.com/punkholic/meroshare_API/issues",
    },
    install_requires=["requests", "simplejson"],
    keywords=['API', 'MeroShare', 'MeroShareAPI', 'NepalIPO', 'IPO', 'punkholic'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
