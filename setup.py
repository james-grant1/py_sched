from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='py_sched',
      version='0.1a',
      description='A tool for generating and submitting jobscripts for common schedulers and HPC systems',
      url='http://github.com/james-grant1/py_sched',
      author='James Grant',
      author_email='rjg20@bath.ac.uk',
      long_description=long_description,
      license='BSD3',
      packages=setuptools.find_packages())
