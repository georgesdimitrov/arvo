from setuptools import setup, find_packages

setup(
    name='arvo',
    version='0.1.0',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    url='https://github.com/georgesdimitrov/arvo',
    license='MIT',
    author='Georges Dimitrov',
    author_email='georges.dimitrov@gmail.com',
    description='Python library for procedural music composition',
    install_requires=['music21']
)
