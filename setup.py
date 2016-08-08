from setuptools import setup
import unittest

def test_suite():
    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover('calm.tests', pattern='*_test.py')
    return test_suite

setup(
    name="calmtools",
    version="0.0.1",
    author="Jason Corso",
    author_email="jjcorso@umich.edu",
    url="https://github.com/jasoncorso/calmtools",
    license="MIT",
    description="Tools for working with Caffe and LMDB in Python",
    requires=[
        "numpy (>=1.7.0)",
        "scipy (>=0.13.0)",
        "wxPython (>=3.0.0)",
        "watchdog (>=0.8.3)",
        "matplotlib (>=1.5.1)",
        "lmdb (>=0.84)",
        "cv2 (>=2.4.10)",
    ],
    packages   =["calm","calm.monitors"],
    #scripts    =[],
    #ext_modules=[],
    #cmdclass   =[],
    entry_points = {
        'console_scripts': [
            'calmmaketestdata=calm.tests.maketestdata:main'
        ],
        'gui_scripts': [
            'calmloss=calm.monitors.loss:main'
        ],
    },
    test_suite='setup.test_suite',
)
