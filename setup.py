from setuptools import setup, find_packages

setup(
    name='BetterOpenSCAD',
    packages=find_packages(),
    version='0.1.0',
    install_requires=['solidpython', 'numpy-stl']
)