from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='heatequation',
    version='1.0.0',
    description='Calculate heat transfer in a matrix of heterogeneous materials',
    long_description=long_description,
    author='Eric Worden',
    url='https://github.com/worden341/heatequation',
    python_requires='>=2.7',
    install_requires=[
        "scipy"
    ],
    py_modules=["heatequation"],
    packages=find_packages(),
    license='GPL-3.0+',
    zip_safe=False,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Scientific/Engineering :: Physics",
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Natural Language :: English',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)'
    ],
    keywords='heat equation thermal transfer',
)

