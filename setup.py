# This setup file is inspired from https://github.com/pypa/sampleproject/blob/master/setup.py

from setuptools import setup, find_packages

requirements = (
    'psycopg2',
    'pyyaml'
)

setup(
    name='UD-Serv',
    version='0.1',
    description='Collection of server-side tools for converting and analysing urban data',
    url='https://github.com/MEPP-team/UD-Serv',
    author='VCity',
    author_email='vincent.jaillot@liris.cnrs.fr',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Lesser General Public License v2 or later (LGPLv2+)'
        'Programming Language :: Python :: 3.4',
    ],
    packages=find_packages(),
    install_requires=requirements, install_requires=['pytest']
)
