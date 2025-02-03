# setup.py
from setuptools import setup, find_packages

setup(
    name="financial-automation",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        'pandas>=1.5.0',
        'numpy>=1.21.0',
        'matplotlib>=3.5.0',
        'seaborn>=0.11.0',
        'pytest>=7.0.0',
        'pyyaml>=6.0.0',
        'jupyter>=1.0.0',
        'python-dateutil>=2.8.2'
    ],
    author="Your Name",
    author_email="your.email@example.com",
    description="A financial analysis and process automation system",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/financial-automation",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.9',
)