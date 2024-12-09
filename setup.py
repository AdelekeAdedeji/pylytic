from setuptools import setup, find_packages

classifiers = [
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Intended Audience :: Developers"
    "Operating System :: OS Independent",
]

setup(
    name="pylytic",
    version="0.1.0",
    description="A lightweight library for evaluating mathematical expressions and functions",
    long_description=open("README.md").read(),
    long_description_context_type="text/markdown",
    author="Adeleke Adedeji",
    author_email="aadeleke91618330@gmail.com",
    license="MIT",
    license_files="LICENSE",
    url="https://github.com/AdelekeAdedeji/pylytic.git",
    packages=find_packages(),
    include_package_data=True,
    classifiers=classifiers,
    python_requires=">=3.8",
    install_requires=[],
)
