import sys  # noqa
import subprocess  # noqa
from setuptools import setup, find_packages
try: # for pip >= 10
    from pip._internal.req import parse_requirements
except ImportError: # for pip <= 9.0.3
    from pip.req import parse_requirements

commit = subprocess.Popen(
    'git rev-parse --short HEAD'.split(),
    stdout=subprocess.PIPE,
).stdout.read().decode('utf-8').strip()

install_reqs = parse_requirements('requirements.txt', session='')

setup(
    name='scp-prototype',
    version='0.1+%s' % commit,
    description='simulation for scp consensus protocol',
    author='BOSNet team',
    license='GPLv3+',
    keywords='bosnet blockchainos blockchain fba stellar quorum python byzantine agreement',
    zip_safe=False,
    install_requires=list(map(lambda x: str(x.req), install_reqs)),
    package_dir={'': 'src'},
    packages=find_packages('src', exclude=('test',)),
    scripts=(
        'script/run-application.py',
        'script/run-client.py',
    ),
)
