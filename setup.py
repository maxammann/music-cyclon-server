from setuptools import setup, find_packages

setup(
    name='music-cyclon-server',
    version='0.1',
    packages=find_packages(),
    url='',
    license='',
    author='max',
    author_email='',
    description='',
    install_requires=['flask',
                      'beets',
                      'tornado'],
    scripts=['scripts/music-cyclon-server'],
    include_package_data=True,
)