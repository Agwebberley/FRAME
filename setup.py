from setuptools import setup, find_packages
from .frame import __version__

setup(
    name='frame',
    version=__version__,
    packages=find_packages(),
    include_package_data=True,
    description='Framework for Rapid Application Modeling and Efficiency',
    author='Agwebberley',  # Author name
    install_requires=[
        'Django>=5.0',
        'boto3>=1.34.144',
        # Add other dependencies here
    ],
    python_requires='>=3.10',
    classifiers=[
        'Framework :: Django',
        'Programming Language :: Python :: 3',
    ],
)
