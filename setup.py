from setuptools import setup, find_packages

setup(
    name='inventory',           
    version='1.0.2',
    description='KAZZA inventory management system',
    author='Zakir Aghayev.',
    author_email='zakir-aghayev@outlook.com',
    url='https://github.com/KAZTorant/kazza_inventory.git',
    packages=find_packages(),
    include_package_data=True,  # Ensures static files, templates, etc. are included
    install_requires=[
        'Django>=3.2',  # Adjust as needed
    ],
    classifiers=[
        'Framework :: Django',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',  # Choose the correct license
    ],
)
