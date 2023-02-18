from setuptools import setup, find_packages

with open("README.md", 'r') as f:
    long_description = f.read()

setup(
    name='finary_assistant',
    version='0.0.1',
    description='A command line investment assistant to organize your portfolio and simulate its future to reach your life goals.',
    license='GNU General Public Version 3',
    long_description=long_description,
    long_description_content_type = "text/markdown",
    author='MadeInPierre',
    author_email='pielaclau@gmail.com',
    url="https://github.com/MadeInPierre/finary_assistant",
    packages=find_packages(),
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