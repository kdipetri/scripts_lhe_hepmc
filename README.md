Setup for LHE reading.
First, an lcg view to get a python3 installation that works with ROOT. We won't use ROOT in this project unless we can help it, but the LHE parser uses it. This line is something you need every time you log in, so maybe put it in a shell script or something.

lsetup "views LCG_97python3 x86_64-centos7-gcc8-opt"

Now we need a Python virtual environment where you can install the LHE reader. Make one and install it.

python3 -m venv pythonenv
source pythonenv/bin/activate
pip install lhereader
pip install dataclasses
pip install pyhepmc-ng 

You'll get a message saying pip needs to be updated - ignore it, we don't have permissions to update pip on lxplus. You need to source the activate script every time you log in, but nothing else, since your virtual env will keep everything you installed.
Now try running the example script! It should print out a ton of particle properties in Python format.
