import setuptools


setuptools.setup(
    name="cosmopy",
    version="0.0.1",
    author="Michael Garstka",
    author_email="michael@garstka.org",
    description="An interface to the Julia solver COSMO.jl.",
    url="https://github.com/oxfordcontrol/cosmopy",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
