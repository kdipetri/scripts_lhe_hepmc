# Setup for HEPMC reading.

We'll be working on lxplus. This line is something you need every time you log in, so maybe put it in your .bashrc.

```
source /cvmfs/cms.cern.ch/cmsset_default.sh
```

To check out this package

```
git clone https://github.com/kdipetri/scripts_lhe_hepmc.git
cd scripts_lhe_hepmc
```

Now we need a Python virtual environment where you can install the HEPMC reader and any other python packages you need for plotting. Make one and install it.

```
python3 -m venv pythonenv
source pythonenv/bin/activate
pip install pyhepmc-ng 
pip install matplotlib
pip install numpy
pip install scipy
pip install uproot4
pip install pandas
```

You'll get a message saying `pip` needs to be updated - ignore it, we don't have permissions to update pip on lxplus. You need to source the activate script every time you log in, but nothing else, since your virtual env will keep everything you installed.  

Now try running the example script! It should print out a ton of particle properties in Python format.

```
python test_hepmc.py
```
Edit the script to study your favorite BSM particle and its decay products! 


To deactivate your virtual environment
``` 
deactivate
```

The next time you login all you need to do is
```
cd scripts_lhe_hepmc 
source pythonenv/bin/activate
```
