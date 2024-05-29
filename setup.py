# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
import re, ast
from pip._internal.req import parse_requirements
from pip._internal.network.session import PipSession

# get version from __version__ variable in ibt_call_center/__init__.py
_version_re = re.compile(r'__version__\s+=\s+(.*)')

with open('ibt_call_center/__init__.py', 'rb') as f:
    version = str(ast.literal_eval(_version_re.search(
        f.read().decode('utf-8')).group(1)))

# Parsing requirements.txt using pip's internal API
requirements = parse_requirements("requirements.txt", session=PipSession())

setup(
    name='ibt_call_center',
    version=version,
    description='Call Center',
    author='IBT',
    author_email='callcenteribt@gmail.com',
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    install_requires=[str(ir.requirement) for ir in requirements],
    dependency_links=[str(ir.link.url) for ir in requirements if ir.link]
)