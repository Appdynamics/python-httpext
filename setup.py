from distutils.core import setup

setup(
    name='HttpExt',
    version='0.1.4',
    author='Andrew Udvare',
    author_email='audvare@gmail.com',
    py_modules=['httpext'],
    url='http://pypi.python.org/pypi/HttpExt/',
    license='LICENSE.txt',
    description='Helpers for downloading files.',
    long_description=open('README.rst').read(),
    install_requires=[
        'OSExtension>=0.1.2',
    ]
)
