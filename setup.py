from setuptools import setup

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
        "wxPython (>=3.0.0.0)",
        "watchdog (>=0.8.3)",
        "matplotlib (>=1.5.1)",
        "lmdb (>=0.84)",
    ],
    packages   =["calmtools"],
    scripts    =[],
    ext_modules=[],
    cmdclass   =[],
)
