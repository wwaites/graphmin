from setuptools import setup, find_packages
import sys, os

version = '0.1.7'

def readme():
    dirname = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(dirname, "README.txt")
    return open(filename).read()

setup(name='graphmin',
    version=version,
    description="RDF Graph Minimisation",
    long_description=readme(),
    classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    keywords='',
    author='William Waites',
    author_email='ww@styx.org',
    url='http://river.styx.org/ww/2010/10/graphmin',
    license='BSD',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
    ],
    entry_points="""
        [console_scripts]
        graphmin=graphmin:graphmin
    """,
    )
