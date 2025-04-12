from setuptools import setup, find_packages

setup(
    name="factotumcli",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "requests",
        "rich",
    ],
    entry_points={
        "console_scripts": [
            "factotum = FactotumCLI.cli:main",
        ],
    },
    author="Xavier Dugal",
    author_email="xavierdugal2004@hotmail.com",
    description="Your personal command line assistant tool.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/factotumcli",  # Add your GitHub URL!
    license="MIT",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Environment :: Console",
        "Topic :: Utilities",
    ],
    python_requires='>=3.7',
)
