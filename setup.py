from setuptools import setup, find_packages
import subprocess
import sys


setup(
    name="smo",
    version="1.0.0",
    author="Prudhvi Duba",
    author_email=["duba.prudhvi@5g.iith.ac.in"],
    description=("smo"),
    #long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://githost.wisig.com/smo.git",  # Replace with your repo URL
    packages=find_packages(),  # Automatically detects packages (module, gNB, git_url, etc.)
    py_modules=["smo"],  # Include standalone Python files
    include_package_data=True,
    install_requires=[
        "requests>=2.25.0", "faker>=8.0.0","InquirerPy" ],

    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Wisig License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    entry_points={
        "console_scripts": [
            "smo=smo:main_menu"
        ],
    },
)

