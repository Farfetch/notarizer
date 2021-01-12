from setuptools import find_packages, setup
from os import getenv

VERSION = getenv('RELEASE_VERSION')

setup_requirements = ["wheel"]
test_requirements = []

setup(
    name='notarizer',
    version=VERSION,
    url="https://github.com/Farfetch/notarizer.git",
    license="MIT License (MIT)",
    include_package_data=True,
    packages=find_packages(exclude=["notarizer/test"]),    
    entry_points={
        'console_scripts': [
            'notarizer = notarizer.cli:main'
        ]
    },
    setup_requires=setup_requirements,
    install_requires=open('requirements.txt').read().splitlines(),
    author="Farfetch",
    author_email="opensource@farfetch.com",
    description="Notarizer is a tool that provides a way of verifying the authenticity of docker images.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown"
)
