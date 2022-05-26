#nevents=1000
#nevents=500
#nevents=100

#python test_hepmc.py --mass "1000" --lifetime "stable" --nevents 10 --doTest True
#python test_bkg.py --nevents 10  --doTest True
#python test_bkg.py --nevents 10000

# basic vary lifetime, 500
#python test_hepmc.py --mass "500" --lifetime "stable"  --nevents ${nevents}
#python test_hepmc.py --mass "500" --lifetime "10ns"    --nevents ${nevents}
#python test_hepmc.py --mass "500" --lifetime "1ns"     --nevents ${nevents}
#python test_hepmc.py --mass "500" --lifetime "0p1ns"   --nevents ${nevents}
#python test_hepmc.py --mass "500" --lifetime "0p01ns"  --nevents ${nevents}
#python test_hepmc.py --mass "500" --lifetime "0p001ns" --nevents ${nevents}

# basic vary lifetime, 100
#python test_hepmc.py --mass "100" --lifetime "stable"  --nevents ${nevents}
#python test_hepmc.py --mass "100" --lifetime "10ns"    --nevents ${nevents}
#python test_hepmc.py --mass "100" --lifetime "1ns"     --nevents ${nevents}
#python test_hepmc.py --mass "100" --lifetime "0p1ns"   --nevents ${nevents}
#python test_hepmc.py --mass "100" --lifetime "0p01ns"  --nevents ${nevents}
#python test_hepmc.py --mass "100" --lifetime "0p001ns" --nevents ${nevents}

# vary mass 10 ns
#python test_hepmc.py --mass "100" --lifetime "10ns" --nevents ${nevents}
#python test_hepmc.py --mass "300" --lifetime "10ns" --nevents ${nevents}
#python test_hepmc.py --mass "500" --lifetime "10ns" --nevents ${nevents}
#python test_hepmc.py --mass "700" --lifetime "10ns" --nevents ${nevents}
#python test_hepmc.py --mass "1000" --lifetime "10ns" --nevents ${nevents}

# vary mass 1 ns
#python test_hepmc.py --mass "100" --lifetime "1ns" --nevents ${nevents}
#python test_hepmc.py --mass "300" --lifetime "1ns" --nevents ${nevents}
#python test_hepmc.py --mass "500" --lifetime "1ns" --nevents ${nevents}
#python test_hepmc.py --mass "700" --lifetime "1ns" --nevents ${nevents}
#python test_hepmc.py --mass "1000" --lifetime "1ns" --nevents ${nevents}

## vary mass stable
nevents=1000
python test_hepmc.py --mass "100" --lifetime "stable" --nevents ${nevents}
python test_hepmc.py --mass "300" --lifetime "stable" --nevents ${nevents}
python test_hepmc.py --mass "500" --lifetime "stable" --nevents ${nevents}
python test_hepmc.py --mass "700" --lifetime "stable" --nevents ${nevents}
python test_hepmc.py --mass "1000" --lifetime "stable" --nevents ${nevents}

#whole set of samples
#python test_hepmc.py --mass "100" --lifetime "1ns" --nevents ${nevents}
#python test_hepmc.py --mass "200" --lifetime "1ns" --nevents ${nevents}
#python test_hepmc.py --mass "300" --lifetime "1ns" --nevents ${nevents}
#python test_hepmc.py --mass "400" --lifetime "1ns" --nevents ${nevents}
#python test_hepmc.py --mass "500" --lifetime "1ns" --nevents ${nevents}
#python test_hepmc.py --mass "600" --lifetime "1ns" --nevents ${nevents}
#python test_hepmc.py --mass "700" --lifetime "1ns" --nevents ${nevents}
#python test_hepmc.py --mass "1000" --lifetime "1ns" --nevents ${nevents}
