from setuptools import find_packages, setup

setup(
    name="kubeclient",
    version="0.0.1",
    description="Kubescape team kubernetes client wrapper",
    author="Kubescape team",
    find_packages=find_packages(exclude=["tests", "tests.*"]),
    install_requires=[
        "kubernetes~=28.1",
    ],
)
