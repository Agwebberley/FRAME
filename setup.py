from setuptools import setup, find_packages

setup(
    name='Meteor',
    version='0.1.0',
    packages=find_packages(),
    include_package_data=True,
    description='A Django app for creating meta models and templates',
    author='Agwebberley',  # Author name
    install_requires=[
        'Django>=5.0',
        # Add other dependencies here
    ],
    python_requires='>=3.10',
    classifiers=[
        'Framework :: Django',
        'Programming Language :: Python :: 3',
    ],
)
