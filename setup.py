import setuptools
from os import path
this_directory = path.abspath(path.dirname(__file__))

with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setuptools.setup(
    name="cosmopy",
    version="0.0.1",
    author="Michael Garstka",
    author_email="michael@garstka.org",
    description="An interface to the Julia solver COSMO.jl.",
    url="https://github.com/oxfordcontrol/cosmopy",
    package_dir={ 'cosmopy' : 'cosmopy'},
    setup_requires=["numpy >= 1.7", "scipy >= 0.13.2", "julia >= 0.5.6"],
    install_requires=requirements,
    long_description=long_description,
    long_description_content_type='text/markdown',
    python_requires='>=3.6',
    license='Apache 2.0'
)