from setuptools import setup, find_packages

setup(
    name='graphnado',
    version='0.0.1',
    description='Adds GraphQL support to your Tornado application',
    long_description=open('README.md').read(),
    url='https://github.com/phndiaye/graphnado',
    author='Philippe Ndiaye',
    author_email='phndiaye@gmail.com',
    licenes='MIT',
    classifiers=[
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: Implementation :: PyPy',
        'License :: OSI Approved :: MIT License',
    ],
    keywords='api graphql tornado relay',
    packages=find_packages(exclude=['tests']) + ['graphnado/templates'],
    include_package_data=True,
    install_requires=['tornado', 'graphql-core'],
    platforms='any'
)
