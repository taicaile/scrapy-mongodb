"""setup"""

import io

from setuptools import setup


def read_file(filename):
    """read file content"""
    with io.open(filename, encoding="utf-8") as fp:
        return fp.read().strip()


def read_requirements(filename):
    """read requirements"""
    return [
        line.strip()
        for line in read_file(filename).splitlines()
        if not line.startswith("#")
    ]


setup(
    name="scrapy-mongodb",
    version="0.1.0",
    description="MongoDB-based components for Scrapy",
    long_description=read_file("README.md"),
    author="taicaile",
    url="https://github.com/taicaile/scrapy-mongodb",
    packages=["scrapy_mongodb"],
    # license="MIT",
    install_requires=read_requirements("requirements.txt"),
)
