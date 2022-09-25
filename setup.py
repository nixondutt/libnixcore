from setuptools import setup, find_packages
import os
from sphinx.setup_command import BuildDoc
cmdclass = {'build_sphinx': BuildDoc}

exec(
    open(
        os.path.join(
            os.path.abspath(
                os.path.dirname(__file__)),
            'libcore',
            '_version.py')).read())

with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

name = 'libcore'
author = 'Nixon'

setup(
    name=name,
    version=__version__,
    description='Multithread Pipeline',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/nixondutt/libnixcore',
    author=author,
    author_email='nixondutta402@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 1 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3 :: Only',
    ],
    keywords='multithreaed pipeline',
    packages=find_packages(),
    install_requires=['Pillow'],
)
