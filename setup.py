from setuptools import setup, find_packages
from glob import glob

with open("README.md", 'r') as f:
    long_description = f.read()

setup(
    name='finary_assistant',
    version='0.0.1',
    description='A command line investment assistant to organize your portfolio and simulate its future to reach your life goals.',
    license='GNU General Public Version 3',
    long_description=long_description,
    long_description_content_type = "text/markdown",
    author='Pierre Laclau (MadeInPierre)',
    author_email='pielaclau@gmail.com',
    url="https://github.com/MadeInPierre/finary_assistant",
    packages=find_packages(),
    package_data={
        'doc': ['*.png'],
        'finary_assistant': ['finary_api/*'],
    },
    include_package_data=True,
    install_requires=[
        'rich>=12.0.1',
        'docopt>=0.6.2',
        'fuzzywuzzy[speedup]>=0.18.0',
        'requests==2.28.2',
    ],
    extras_require={
        'dev': [
            'black',
            'pdoc3'
        ]
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: Financial and Insurance Industry",
        "Intended Audience :: Information Technology",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ]
)