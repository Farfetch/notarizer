from setuptools import find_packages, setup
from os import getenv
from datetime import datetime

MAJOR = '0'
MINOR = '1'
PATCH = datetime.now().timetuple().tm_yday
BRANCH = getenv('CURRENT_BRANCH')
BUILD_ID = getenv('BUILD_ID')

def get_version(major, minor, patch, branch, build_id):
    version_core = f'{major}.{minor}.{patch}'
    if branch == 'main':
        return version_core

    return f'{version_core}-beta-{build_id}'


setup_requirements = ["wheel"]
test_requirements = []

setup(
    name='notarizer',
    version=get_version(MAJOR, MINOR, PATCH, BRANCH, BUILD_ID),
    url="https://github.com/Farfetch/notarizer.git",
    license="MIT License (MIT)",
    include_package_data=True,
    packages=find_packages(exclude=["notarizer/test"]),
    setup_requires=setup_requirements,
    install_requires=open('requirements.txt').read().splitlines(),
    tests_require=test_requirements,
    author="farfetch",
    author_email="opensource@farfetch.com",
    description="Notarizer is a tool that provides a way of verifying the authenticity of docker images.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown"
)