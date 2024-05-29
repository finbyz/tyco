# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
import re, ast
from pip._internal.req import parse_requirements
from pip._internal.network.session import PipSession

# get version from __version__ variable in tyco/__init__.py
_version_re = re.compile(r'__version__\s+=\s+(.*)')

with open('tyco/__init__.py', 'rb') as f:
    version = str(ast.literal_eval(_version_re.search(
        f.read().decode('utf-8')).group(1)))

requirements = parse_requirements("requirements.txt", session="")

setup(
	name='tyco',
	version=version,
	description='Custom App for Tyco',
	author='Finbyz Tech Pvt Ltd',
	author_email='info@finbyz.com',
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=[str(ir.requirement) for ir in requirements],
	dependency_links=[str(ir.link) for ir in requirements if ir.link]
)