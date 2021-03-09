from setuptools import setup, find_packages

setup(
    name="inginious-extra-test",
    version="0.1",
    description="Plugin to allow extra tests without extra input from student",
    packages=find_packages(),
    install_requires=["inginious"],
    test_require=[],
    extras_require={},
    scripts=[],
    include_package_data=True,
    author="Stephen Pauwels - UAntwerpen",
    author_email="stephen.pauwels@uantwerpen.be",
    license="AGPL 3",
    url=""
)