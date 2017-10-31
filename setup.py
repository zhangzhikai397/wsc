from setuptools import setup, find_packages


setup(
    name='wsc',
    packages=find_packages(),
    version='2017.10.25-0',
    description='Python WebSocket Channel',
    author='Maxim Papezhuk',
    author_email='maxp.job@gmail.com',
    url='https://github.com/duverse/python-wsc',
    download_url='https://github.com/duverse/python-wsc/tarball/v2017.10.25-0.zip',
    keywords=['python', 'websocket', 'channel'],
    classifiers=[],
    install_requires=[
        'requests'
    ],
    entry_points={
        'console_scripts': [
            'wsc=wsc.application:run_server',
        ],
    },
)
