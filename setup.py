from setuptools import setup

with open("README.md", 'r') as f:
    long_description = f.read()

setup(
    name='finary_assistant',
    version='0.0.1',
    description='Finary Assistant',
    license="GPLv3",
    long_description=long_description,
    author='MadeInPierre',
    author_email='pielaclau@gmail.com',
    url="https://github.com/MadeInPierre/finary_assistant",
    packages=['finary_assistant'],
    install_requires=[
        'rich>=12.0.1',
        'docopt>=0.6.2'
    ],
    extras_require={
        'dev': [
            'black',
            'pdoc3'
        ]
    }
)