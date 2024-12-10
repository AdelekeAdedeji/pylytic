from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'Operating System :: OS Independent',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: 3.10',
    'License :: OSI Approved :: MIT License',
]

setup(
    name="pylytic",
    version="0.1.0",
    description="A lightweight library for evaluating mathematical expressions and functions",
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="Adeleke Adedeji",
    author_email="aadeleke91618330@gmail.com",
    license="MIT",
    license_files="LICENSE",
    url="https://github.com/AdelekeAdedeji/pylytic.git",
    packages=find_packages(),
    include_package_data=True,
    classifiers=classifiers,
    python_requires=">=3.8",
    install_requires=[]
)
