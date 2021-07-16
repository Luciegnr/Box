from setuptools import setup

setup(
   name='box',
   version='0.1.0',
   description='Notre projet de TIC/UNI2',
   author='Lucie & Anaïs',
   author_email='LA@gmail.com',
   packages=['box'],
   scripts=['/home/box/UNI2/box/box/script.py'],
   install_requires=['PyYAML'],
    entry_points={
        'console_scripts': [
            'box=box.script:script'
        ],
    },
)
