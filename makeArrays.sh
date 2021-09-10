nevents=1000
nevents=500
nevents=100
python test_hepmc.py --mass "100" --lifetime "1ns" --nevents ${nevents}
python test_hepmc.py --mass "200" --lifetime "1ns" --nevents ${nevents}
python test_hepmc.py --mass "300" --lifetime "1ns" --nevents ${nevents}
python test_hepmc.py --mass "400" --lifetime "1ns" --nevents ${nevents}
python test_hepmc.py --mass "500" --lifetime "1ns" --nevents ${nevents}
python test_hepmc.py --mass "600" --lifetime "1ns" --nevents ${nevents}

#python test_hepmc.py --mass "500" --lifetime "stable" --nevents ${nevents}
#python test_hepmc.py --mass "500" --lifetime "10ns" --nevents ${nevents}
#python test_hepmc.py --mass "500" --lifetime "1ns" --nevents ${nevents}
#python test_hepmc.py --mass "500" --lifetime "0p1ns"   --nevents ${nevents}
#python test_hepmc.py --mass "500" --lifetime "0p01ns"  --nevents ${nevents}
##python test_hepmc.py --mass "500" --lifetime "0p001ns" --nevents ${nevents}

