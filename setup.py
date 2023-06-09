from setuptools import setup, find_packages

setup(
    name='crpy',
    version='1.0.0',
    author='Christopher J. Stehno',
    description='A simple 5e encounter difficulty calculator.',
    packages=find_packages(),
    install_requires=[
        'altgraph==0.17.3',
        'astroid==2.15.5',
        'click==8.1.3',
        'dill==0.3.6',
        'iniconfig==2.0.0',
        'isort==5.12.0',
        'lazy-object-proxy==1.9.0',
        'macholib==1.16.2',
        'mccabe==0.7.0',
        'mypy==1.3.0',
        'mypy-extensions==1.0.0',
        'packaging==23.1',
        'platformdirs==3.5.1',
        'pluggy==1.0.0',
        'pyinstaller==5.11.0',
        'pyinstaller-hooks-contrib==2023.3',
        'pylint==2.17.4',
        'pytest==7.3.1',
        'tomlkit==0.11.8',
        'typing_extensions==4.5.0',
        'wrapt==1.15.0',
    ],
)
