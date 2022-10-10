from setuptools import setup

setup(
    name="BluePySubcellular",
    version="1.0",
    description="A Python interface to BlueNaaS-Subcellular. It allows users to import BNGL models, create and run simulations with STEPs and BioNetGen.",
    author="Blue Brain Project, EPFL",
    author_email="",
    packages=["BluePySubcellular"],  # same as name
    install_requires=["requests"],  # external packages as dependencies
)
