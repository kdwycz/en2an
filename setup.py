import sys
from setuptools import setup
from setuptools import find_packages

py_version = sys.version_info[:2]

if py_version < (3, 6):
    raise RuntimeError('en2an requires Python 3.6 or later')

setup(
    name="en2an",
    version="0.0.5",
    author="Ailln",
    author_email="kinggreenhall@gmail.com",
    url="https://github.com/Ailln/en2an",
    packages=find_packages(),
    include_package_data=True,
    install_requires=open("./requirements.txt", "r", encoding="utf-8").read().splitlines(),
    description="Convert English numerals and Arabic numerals.",
    long_description=open("./README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    zip_safe=False,
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ]
)
