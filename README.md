calmtools -- Caffe and LMDB Tools
=================================

Tools for working with Caffe and LMDB in python.

These augment the respective python bindings for these two libraries.

Maintained by Jason Corso and COG Members (Corso Research Group at 
University of Michigan).

Brief Description and File System Layout

    calm/             --->  main package
      monitors/       --->  sub-package for monitors

Binaries created

    calmloss          --->  a loss monitor that will track a training 
                            process (requires wxPython)

License
-------

MIT license.

Setup
-----

To begin working with this project, clone the repository to your 
machine

    git clone https://github.com/jasoncorso/calmtools

It is expected that the CAFFE_ROOT environment variable is set.

If you are using conda and you want some of the packages installed by 
conda rather than pip, than you should do it manually (see the 
packages in setup.py).  For watchdog, you will probably need to 
specify the channel

    conda install --channel https://conda.anaconda.org/timbr-io watchdog
    conda install -c dougal lmdb=0.84
    conda install -c anaconda wxpython=3.0.0.0
    ...

    python setup.py install
    or              develop

If you want to let pip install them all, then just the following

    python setup.py install 
    or              develop



Uninstall
---------

If you have pip installed, it is easy to uninstall calmtools

    pip uninstall calmtools




