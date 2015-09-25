from setuptools import setup
import os

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

version = '1.3.1'

install_requires = [
    'python-etcd'
]

setup(name='pyetcdlock',
    version=version,
    description="python etcd network mutux lock,support watch ,force ,incr lock time",
    long_description = read('README.md'),
    classifiers = [
         'Development Status :: 2 - Pre-Alpha',
         'Intended Audience :: Developers',
         'License :: OSI Approved :: MIT License',
         'Programming Language :: Python :: 2.7',
         'Programming Language :: Python :: 3.0',
         'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    keywords = ['mutux network lock based on etcd','fengyun'],
    author='ruifengyun',
    author_email='rfyiamcool@163.com',
    url='https://github.com/rfyiamcool',
    license='MIT',
    packages=['pyetcdlock'],
    install_requires=install_requires,
)
