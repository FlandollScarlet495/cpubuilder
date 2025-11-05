from setuptools import setup, find_packages

setup(
    name="cpubuilder",
    version="0.1.0",
    author="Yukino Kotone",
    author_email="nakamurakensuke5@gmail.com",
    description="A library for building CPU emulators in Python",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/FlandollScarlet495/cpubuilder",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Embedded Systems",
    ],
    python_requires=">=3.7",
    install_requires=[
        "typing; python_version < '3.7'",
    ],
)