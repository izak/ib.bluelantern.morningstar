from setuptools import setup, find_packages

version = '0.1'

setup(
    name='ib.blexample',
    version=version,
    description="Python tool for Frobnicating a Bar into BlueLantern",
    long_description=open("README.md").read(),
    # Get more strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Programming Language :: Python",
        ],
    keywords='python high availability IP',
    author='Izak Burger',
    author_email='isburger@gmail.com',
    url='https://github.com/izak/ib.blexample',
    license='GPL',
    packages=find_packages(exclude=['ez_setup']),
    namespace_packages=['ib'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'setuptools',
        'paho-mqtt',
    ]
    )
