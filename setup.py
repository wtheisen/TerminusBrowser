from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()

setup(
    name='commandChan',
    version='0.69',
    description='terminal 4chan/reddit browser',
    long_description=readme,
    long_description_content_type="text/markdown",
    author='wtheisen',
    url='https://github.com/wtheisen/commandChan',
    entry_points={
        'console_scripts': [
            'commandChan = commandChan.commandChanVim:main'
        ]
    },
    package_dir={'': 'src'},
    packages=['commandChan'],
    install_requires=[
        'requests==2.18.4',
        'urwid==2.0.1',
        'beautifulsoup4==4.7.1',
        'lxml'
    ],
    python_requires='>=3.0'
)
