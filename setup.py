# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
from os import path
import os

here = os.path.abspath(os.path.dirname(__file__))

with open(path.join(here, 'readme.md')) as f:
    long_description = f.read()


setup(
    name="UnicodeTokenizer",
    packages=find_packages(),
    version='0.0.0',
    description='UnicodeTokenizer: tokenize all Unicode text',
    long_description=long_description,
    long_description_content_type="text/markdown",
    python_requires='>=3.0',
    url='https://github.com/laohur/UnicodeTokenizer',
    keywords=['UnicodeTokenizer', 'Tokenizer', 'Unicode', 'laohur'],
    author='laohur',
    author_email='laohur@gmail.com',
    license='[Anti-996 License](https: // github.com/996icu/996.ICU/blob/master/LICENSE)',
)