from setuptools import setup, find_packages
import sys, os

version = '0.1'

if (sys.version_info > (3, 2) or 
    (sys.version_info < (3,) and sys.version_info > (2,7))):
    requires = []
else:
    requires = ['argparse']

#TODO: Make setuptools create a phynk script in the [/usr/local/]bin directory.
long_description = open('README.rst').read()

setup(name='Phynk',
      version=version,
      description="Photography syncer",
      long_description=long_description,
      classifiers=[
          'Development Status :: 4 - Beta',
          'Environment :: Console',
          'Intended Audience :: End Users/Desktop',
          'License :: CC0 1.0 Universal (CC0 1.0) Public Domain Dedication',
          'Operating System :: OS Independent',
          'Programming Language :: Python :: 2.7', #TODO: test with others including Python 3
          'Topic :: Multimedia :: Graphics',
      ],
      keywords='photo synchroniser',
      author='Lennart Regebro',
      author_email='regebro@gmail.com',
      url='',
      license='CC0 1.0 Universal (CC0 1.0) Public Domain Dedication',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=True,
      install_requires=requires,
      entry_points={
          'console_scripts': [
              'phynk=phynk.phynk:phynk_entry_point',
              ]},
      test_suite='phynk.tests.test_all',
      )
