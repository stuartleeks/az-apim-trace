from codecs import open
from setuptools import setup, find_packages

VERSION = "0.0.4"

CLASSIFIERS = [
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'Intended Audience :: System Administrators',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'License :: OSI Approved :: MIT License',
]

DEPENDENCIES = []

setup(
    name='apim_trace',
    version=VERSION,
    description='Call APIs in API Management with a trace token',
    long_description='An extension to work with APIM trace tokens',
    license='MIT',
    author='Stuart Leeks',
    author_email='stuartle@microsoft.com',
    url='https://github.com/stuartleeks/az-apim-trace',
    classifiers=CLASSIFIERS,
    packages=find_packages(),
    install_requires=DEPENDENCIES
)