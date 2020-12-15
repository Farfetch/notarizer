from setuptools import find_packages, setup

setup_requirements = ["wheel"]
test_requirements = []

setup(
    name='notarizer',
    version="0.0.1b0",
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