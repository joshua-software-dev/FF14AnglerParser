#!/usr/bin/env python3

from setuptools import setup, find_packages


with open('README.rst') as readme_file:
    readme = readme_file.read()

# noinspection SpellCheckingInspection
requirements = [
    'aiohttp',
    'asyncio-throttle',
    'beautifulsoup4',
    'dataclasses_json',
    'falcon<2.0.0,>=1.0.0',
    'falcon-autocrud',
    'falcon-ratelimit',
    'falcon_sslify',
    'gunicorn',
    'lxml',
    'selenium',
    'sqlalchemy',
]

setup_requirements = []

test_requirements = []

setup(
    author="Joshua Field",
    author_email='joshua.software.dev@gmail.com',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="Package for scraping and hosting ff14angler.com data in a useful manner.",
    entry_points={
        'console_scripts': [
            'angler_scraper=ff14angler.scraper_main:main',
            'angler_api_server=ff14angler.server_main:main'
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme,
    include_package_data=True,
    keywords='ff14angler',
    name='ff14angler',
    packages=find_packages(include=['ff14angler', 'ff14angler.*']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/joshua.software.dev/ff14angler',
    version='0.1.0',
    zip_safe=False,
)
