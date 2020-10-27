import setuptools
from os import path
this_directory = path.abspath(path.dirname(__file__))

with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setuptools.setup(
    name="cosmopy",
    version="0.0.2",
    author="Michael Garstka",
    author_email="michael@garstka.org",
    description="An interface to the Julia solver COSMO.jl.",
    url="https://github.com/oxfordcontrol/cosmopy",
    install_requires=["numpy >= 1.7", "scipy >= 0.13.2", "julia >= 0.5.6"],
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages= setuptools.find_packages(),
    python_requires='>=3.6',
    license='Apache 2.0'
)
