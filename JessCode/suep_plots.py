#!/usr/bin/env python

import json
import numpy
import matplotlib.pyplot as plt

f = open('SUEP_effieciencies.json',)
data = json.load(f)

masses = [125, 200, 400, 600, 800, 1000]
ntracks = [100, 150, 200]
pts = [0.5, 1, 2]

# #Plot for individual ntrack, mass on x-axis, different pt lines
# fixed_n100_pt05 = [data["data"][0]["efficiency"], data["data"][9]["efficiency"], data["data"][18]["efficiency"], 
#                    data["data"][27]["efficiency"], data["data"][36]["efficiency"], data["data"][45]["efficiency"]]
# fixed_n100_pt1 = [data["data"][3]["efficiency"], data["data"][12]["efficiency"], data["data"][21]["efficiency"], 
#                   data["data"][30]["efficiency"], data["data"][39]["efficiency"], data["data"][48]["efficiency"]]
# fixed_n100_pt2 = [data["data"][6]["efficiency"], data["data"][15]["efficiency"], data["data"][24]["efficiency"], 
#                   data["data"][33]["efficiency"], data["data"][42]["efficiency"], data["data"][51]["efficiency"]]
# fixed_n150_pt05 = [data["data"][1]["efficiency"], data["data"][10]["efficiency"], data["data"][19]["efficiency"], 
#                    data["data"][28]["efficiency"], data["data"][37]["efficiency"], data["data"][46]["efficiency"]]
# fixed_n150_pt1 = [data["data"][4]["efficiency"], data["data"][13]["efficiency"], data["data"][22]["efficiency"], 
#                   data["data"][31]["efficiency"], data["data"][40]["efficiency"], data["data"][49]["efficiency"]]
# fixed_n150_pt2 = [data["data"][7]["efficiency"], data["data"][16]["efficiency"], data["data"][25]["efficiency"], 
#                   data["data"][34]["efficiency"], data["data"][43]["efficiency"], data["data"][52]["efficiency"]]
# fixed_n200_pt05 = [data["data"][2]["efficiency"], data["data"][11]["efficiency"], data["data"][20]["efficiency"], 
#                   data["data"][29]["efficiency"], data["data"][38]["efficiency"], data["data"][47]["efficiency"]]
# fixed_n200_pt1 = [data["data"][5]["efficiency"], data["data"][14]["efficiency"], data["data"][23]["efficiency"], 
#                   data["data"][32]["efficiency"], data["data"][41]["efficiency"], data["data"][50]["efficiency"]]
# fixed_n200_pt2 = [data["data"][8]["efficiency"], data["data"][17]["efficiency"], data["data"][26]["efficiency"], 
#                   data["data"][35]["efficiency"], data["data"][44]["efficiency"], data["data"][53]["efficiency"]]

# err_n100_pt05 = [data["data"][0]["error"], data["data"][9]["error"], data["data"][18]["error"], 
#                  data["data"][27]["error"], data["data"][36]["error"], data["data"][45]["error"]]
# err_n100_pt1 = [data["data"][3]["error"], data["data"][12]["error"], data["data"][21]["error"], 
#                 data["data"][30]["error"], data["data"][39]["error"], data["data"][48]["error"]]
# err_n100_pt2 = [data["data"][6]["error"], data["data"][15]["error"], data["data"][24]["error"], 
#                 data["data"][33]["error"], data["data"][42]["error"], data["data"][51]["error"]]
# err_n150_pt05 = [data["data"][1]["error"], data["data"][10]["error"], data["data"][19]["error"], 
#                  data["data"][28]["error"], data["data"][37]["error"], data["data"][46]["error"]]
# err_n150_pt1 = [data["data"][4]["error"], data["data"][13]["error"], data["data"][22]["error"], 
#                 data["data"][31]["error"], data["data"][40]["error"], data["data"][49]["error"]]
# err_n150_pt2 = [data["data"][7]["error"], data["data"][16]["error"], data["data"][25]["error"], 
#                 data["data"][34]["error"], data["data"][43]["error"], data["data"][52]["error"]]
# err_n200_pt05 = [data["data"][2]["error"], data["data"][11]["error"], data["data"][20]["error"], 
#                  data["data"][29]["error"], data["data"][38]["error"], data["data"][47]["error"]]
# err_n200_pt1 = [data["data"][5]["error"], data["data"][14]["error"], data["data"][23]["error"], 
#                 data["data"][32]["error"], data["data"][41]["error"], data["data"][50]["error"]]
# err_n200_pt2 = [data["data"][8]["error"], data["data"][17]["error"], data["data"][26]["error"], 
#                 data["data"][35]["error"], data["data"][44]["error"], data["data"][53]["error"]]

# #Plot for individual ntrack, pt on x-axis, different mass lines
# fixed_n100_125 = [data["data"][0]["efficiency"], data["data"][3]["efficiency"], data["data"][6]["efficiency"]]
# fixed_n100_200 = [data["data"][9]["efficiency"], data["data"][12]["efficiency"], data["data"][15]["efficiency"]]
# fixed_n100_400 = [data["data"][18]["efficiency"], data["data"][21]["efficiency"], data["data"][24]["efficiency"]]
# fixed_n100_600 = [data["data"][27]["efficiency"], data["data"][30]["efficiency"], data["data"][33]["efficiency"]]
# fixed_n100_800 = [data["data"][36]["efficiency"], data["data"][39]["efficiency"], data["data"][42]["efficiency"]]
# fixed_n100_1000 = [data["data"][45]["efficiency"], data["data"][48]["efficiency"], data["data"][51]["efficiency"]]
# fixed_n150_125 = [data["data"][1]["efficiency"], data["data"][4]["efficiency"], data["data"][7]["efficiency"]]
# fixed_n150_200 = [data["data"][10]["efficiency"], data["data"][13]["efficiency"],data["data"][16]["efficiency"]]
# fixed_n150_400 = [data["data"][19]["efficiency"], data["data"][22]["efficiency"], data["data"][25]["efficiency"]]
# fixed_n150_600 = [data["data"][28]["efficiency"], data["data"][31]["efficiency"], data["data"][34]["efficiency"]]
# fixed_n150_800 = [data["data"][37]["efficiency"], data["data"][40]["efficiency"], data["data"][43]["efficiency"]]
# fixed_n150_1000 = [data["data"][46]["efficiency"], data["data"][49]["efficiency"], data["data"][52]["efficiency"]]
# fixed_n200_125 = [data["data"][2]["efficiency"], data["data"][5]["efficiency"], data["data"][8]["efficiency"]]
# fixed_n200_200 = [data["data"][11]["efficiency"], data["data"][14]["efficiency"], data["data"][17]["efficiency"]]
# fixed_n200_400 = [data["data"][20]["efficiency"], data["data"][23]["efficiency"], data["data"][26]["efficiency"]]
# fixed_n200_600 = [data["data"][29]["efficiency"], data["data"][32]["efficiency"], data["data"][35]["efficiency"]]
# fixed_n200_800 = [data["data"][38]["efficiency"], data["data"][41]["efficiency"], data["data"][44]["efficiency"]]
# fixed_n200_1000 = [data["data"][47]["efficiency"], data["data"][50]["efficiency"], data["data"][53]["efficiency"]]

# err_n100_125 = [data["data"][0]["error"], data["data"][3]["error"], data["data"][6]["error"]]
# err_n100_200 = [data["data"][9]["error"], data["data"][12]["error"], data["data"][15]["error"]]
# err_n100_400 = [data["data"][18]["error"], data["data"][21]["error"], data["data"][24]["error"]]
# err_n100_600 = [data["data"][27]["error"], data["data"][30]["error"], data["data"][33]["error"]]
# err_n100_800 = [data["data"][36]["error"], data["data"][39]["error"], data["data"][42]["error"]]
# err_n100_1000 = [data["data"][45]["error"], data["data"][48]["error"], data["data"][51]["error"]]
# err_n150_125 = [data["data"][1]["error"], data["data"][4]["error"], data["data"][7]["error"]]
# err_n150_200 = [data["data"][10]["error"], data["data"][13]["error"],data["data"][16]["error"]]
# err_n150_400 = [data["data"][19]["error"], data["data"][22]["error"], data["data"][25]["error"]]
# err_n150_600 = [data["data"][28]["error"], data["data"][31]["error"], data["data"][34]["error"]]
# err_n150_800 = [data["data"][37]["error"], data["data"][40]["error"], data["data"][43]["error"]]
# err_n150_1000 = [data["data"][46]["error"], data["data"][49]["error"], data["data"][52]["error"]]
# err_n200_125 = [data["data"][2]["error"], data["data"][5]["error"], data["data"][8]["error"]]
# err_n200_200 = [data["data"][11]["error"], data["data"][14]["error"], data["data"][17]["error"]]
# err_n200_400 = [data["data"][20]["error"], data["data"][23]["error"], data["data"][26]["error"]]
# err_n200_600 = [data["data"][29]["error"], data["data"][32]["error"], data["data"][35]["error"]]
# err_n200_800 = [data["data"][38]["error"], data["data"][41]["error"], data["data"][44]["error"]]
# err_n200_1000 = [data["data"][47]["error"], data["data"][50]["error"], data["data"][53]["error"]]

# #Plot for individual mass, ntrack on x-axis, different pt lines
# fixed_125_pt05 = [data["data"][0]["efficiency"], data["data"][1]["efficiency"], data["data"][2]["efficiency"]]
# fixed_125_pt1 = [data["data"][3]["efficiency"], data["data"][4]["efficiency"], data["data"][5]["efficiency"]]
# fixed_125_pt2 = [data["data"][6]["efficiency"], data["data"][7]["efficiency"], data["data"][8]["efficiency"]]
# fixed_200_pt05 = [data["data"][9]["efficiency"], data["data"][10]["efficiency"], data["data"][11]["efficiency"]]
# fixed_200_pt1 = [data["data"][12]["efficiency"], data["data"][13]["efficiency"], data["data"][14]["efficiency"]]
# fixed_200_pt2 = [data["data"][15]["efficiency"], data["data"][16]["efficiency"], data["data"][17]["efficiency"]]
# fixed_400_pt05 = [data["data"][18]["efficiency"], data["data"][19]["efficiency"], data["data"][20]["efficiency"]]
# fixed_400_pt1 = [data["data"][21]["efficiency"], data["data"][22]["efficiency"], data["data"][23]["efficiency"]]
# fixed_400_pt2 = [data["data"][24]["efficiency"], data["data"][25]["efficiency"], data["data"][26]["efficiency"]]
# fixed_600_pt05 = [data["data"][27]["efficiency"], data["data"][28]["efficiency"], data["data"][29]["efficiency"]]
# fixed_600_pt1 = [data["data"][30]["efficiency"], data["data"][31]["efficiency"], data["data"][32]["efficiency"]]
# fixed_600_pt2 = [data["data"][33]["efficiency"], data["data"][34]["efficiency"], data["data"][35]["efficiency"]]
# fixed_800_pt05 = [data["data"][36]["efficiency"], data["data"][37]["efficiency"], data["data"][38]["efficiency"]]
# fixed_800_pt1 = [data["data"][39]["efficiency"], data["data"][40]["efficiency"], data["data"][41]["efficiency"]]
# fixed_800_pt2 = [data["data"][42]["efficiency"], data["data"][43]["efficiency"], data["data"][44]["efficiency"]]
# fixed_1000_pt05 = [data["data"][45]["efficiency"], data["data"][46]["efficiency"], data["data"][47]["efficiency"]]
# fixed_1000_pt1 = [data["data"][48]["efficiency"], data["data"][49]["efficiency"], data["data"][50]["efficiency"]]
# fixed_1000_pt2 = [data["data"][51]["efficiency"], data["data"][52]["efficiency"], data["data"][53]["efficiency"]]

# err_125_pt05 = [data["data"][0]["error"], data["data"][1]["error"], data["data"][2]["error"]]
# err_125_pt1 = [data["data"][3]["error"], data["data"][4]["error"], data["data"][5]["error"]]
# err_125_pt2 = [data["data"][6]["error"], data["data"][7]["error"], data["data"][8]["error"]]
# err_200_pt05 = [data["data"][9]["error"], data["data"][10]["error"], data["data"][11]["error"]]
# err_200_pt1 = [data["data"][12]["error"], data["data"][13]["error"], data["data"][14]["error"]]
# err_200_pt2 = [data["data"][15]["error"], data["data"][16]["error"], data["data"][17]["error"]]
# err_400_pt05 = [data["data"][18]["error"], data["data"][19]["error"], data["data"][20]["error"]]
# err_400_pt1 = [data["data"][21]["error"], data["data"][22]["error"], data["data"][23]["error"]]
# err_400_pt2 = [data["data"][24]["error"], data["data"][25]["error"], data["data"][26]["error"]]
# err_600_pt05 = [data["data"][27]["error"], data["data"][28]["error"], data["data"][29]["error"]]
# err_600_pt1 = [data["data"][30]["error"], data["data"][31]["error"], data["data"][32]["error"]]
# err_600_pt2 = [data["data"][33]["error"], data["data"][34]["error"], data["data"][35]["error"]]
# err_800_pt05 = [data["data"][36]["error"], data["data"][37]["error"], data["data"][38]["error"]]
# err_800_pt1 = [data["data"][39]["error"], data["data"][40]["error"], data["data"][41]["error"]]
# err_800_pt2 = [data["data"][42]["error"], data["data"][43]["error"], data["data"][44]["error"]]
# err_1000_pt05 = [data["data"][45]["error"], data["data"][46]["error"], data["data"][47]["error"]]
# err_1000_pt1 = [data["data"][48]["error"], data["data"][49]["error"], data["data"][50]["error"]]
# err_1000_pt2 = [data["data"][51]["error"], data["data"][52]["error"], data["data"][53]["error"]]

# #Plot for individual mass, pt on x-axis, different ntrack lines
# fixed_125_n100 = [data["data"][0]["efficiency"], data["data"][3]["efficiency"], data["data"][6]["efficiency"]]
# fixed_125_n150 = [data["data"][1]["efficiency"], data["data"][4]["efficiency"], data["data"][7]["efficiency"]]
# fixed_125_n200 = [data["data"][2]["efficiency"], data["data"][5]["efficiency"], data["data"][8]["efficiency"]]
# fixed_200_n100 = [data["data"][9]["efficiency"], data["data"][12]["efficiency"], data["data"][15]["efficiency"]]
# fixed_200_n150 = [data["data"][10]["efficiency"], data["data"][13]["efficiency"], data["data"][16]["efficiency"]]
# fixed_200_n200 = [data["data"][11]["efficiency"], data["data"][14]["efficiency"], data["data"][17]["efficiency"]]
# fixed_400_n100 = [data["data"][18]["efficiency"], data["data"][21]["efficiency"], data["data"][24]["efficiency"]]
# fixed_400_n150 = [data["data"][19]["efficiency"], data["data"][22]["efficiency"], data["data"][25]["efficiency"]]
# fixed_400_n200 = [data["data"][20]["efficiency"], data["data"][23]["efficiency"], data["data"][26]["efficiency"]]
# fixed_600_n100 = [data["data"][27]["efficiency"], data["data"][30]["efficiency"], data["data"][33]["efficiency"]]
# fixed_600_n150 = [data["data"][28]["efficiency"], data["data"][31]["efficiency"], data["data"][34]["efficiency"]]
# fixed_600_n200 = [data["data"][29]["efficiency"], data["data"][32]["efficiency"], data["data"][35]["efficiency"]]
# fixed_800_n100 = [data["data"][36]["efficiency"], data["data"][39]["efficiency"], data["data"][42]["efficiency"]]
# fixed_800_n150 = [data["data"][37]["efficiency"], data["data"][40]["efficiency"], data["data"][43]["efficiency"]]
# fixed_800_n200 = [data["data"][38]["efficiency"], data["data"][41]["efficiency"], data["data"][44]["efficiency"]]
# fixed_1000_n100 = [data["data"][45]["efficiency"], data["data"][48]["efficiency"], data["data"][51]["efficiency"]]
# fixed_1000_n150 = [data["data"][46]["efficiency"], data["data"][49]["efficiency"], data["data"][52]["efficiency"]]
# fixed_1000_n200 = [data["data"][47]["efficiency"], data["data"][50]["efficiency"], data["data"][53]["efficiency"]]

# err_125_n100 = [data["data"][0]["error"], data["data"][3]["error"], data["data"][6]["error"]]
# err_125_n150 = [data["data"][1]["error"], data["data"][4]["error"], data["data"][7]["error"]]
# err_125_n200 = [data["data"][2]["error"], data["data"][5]["error"], data["data"][8]["error"]]
# err_200_n100 = [data["data"][9]["error"], data["data"][12]["error"], data["data"][15]["error"]]
# err_200_n150 = [data["data"][10]["error"], data["data"][13]["error"], data["data"][16]["error"]]
# err_200_n200 = [data["data"][11]["error"], data["data"][14]["error"], data["data"][17]["error"]]
# err_400_n100 = [data["data"][18]["error"], data["data"][21]["error"], data["data"][24]["error"]]
# err_400_n150 = [data["data"][19]["error"], data["data"][22]["error"], data["data"][25]["error"]]
# err_400_n200 = [data["data"][20]["error"], data["data"][23]["error"], data["data"][26]["error"]]
# err_600_n100 = [data["data"][27]["error"], data["data"][30]["error"], data["data"][33]["error"]]
# err_600_n150 = [data["data"][28]["error"], data["data"][31]["error"], data["data"][34]["error"]]
# err_600_n200 = [data["data"][29]["error"], data["data"][32]["error"], data["data"][35]["error"]]
# err_800_n100 = [data["data"][36]["error"], data["data"][39]["error"], data["data"][42]["error"]]
# err_800_n150 = [data["data"][37]["error"], data["data"][40]["error"], data["data"][43]["error"]]
# err_800_n200 = [data["data"][38]["error"], data["data"][41]["error"], data["data"][44]["error"]]
# err_1000_n100 = [data["data"][45]["error"], data["data"][48]["error"], data["data"][51]["error"]]
# err_1000_n150 = [data["data"][46]["error"], data["data"][49]["error"], data["data"][52]["error"]]
# err_1000_n200 = [data["data"][47]["error"], data["data"][50]["error"], data["data"][53]["error"]]

# #Plot for individual pt, ntrack on x-axis, different mass lines
# fixed_pt05_125 = [data["data"][0]["efficiency"], data["data"][1]["efficiency"], data["data"][2]["efficiency"]]
# fixed_pt05_200 = [data["data"][9]["efficiency"], data["data"][10]["efficiency"], data["data"][11]["efficiency"]]
# fixed_pt05_400 = [data["data"][18]["efficiency"], data["data"][19]["efficiency"], data["data"][20]["efficiency"]]
# fixed_pt05_600 = [data["data"][27]["efficiency"], data["data"][28]["efficiency"], data["data"][29]["efficiency"]]
# fixed_pt05_800 = [data["data"][36]["efficiency"], data["data"][37]["efficiency"], data["data"][38]["efficiency"]]
# fixed_pt05_1000 = [data["data"][45]["efficiency"], data["data"][46]["efficiency"], data["data"][47]["efficiency"]]
# fixed_pt1_125 = [data["data"][3]["efficiency"], data["data"][4]["efficiency"], data["data"][5]["efficiency"]]
# fixed_pt1_200 = [data["data"][12]["efficiency"], data["data"][13]["efficiency"], data["data"][14]["efficiency"]]
# fixed_pt1_400 = [data["data"][21]["efficiency"], data["data"][22]["efficiency"], data["data"][23]["efficiency"]]
# fixed_pt1_600 = [data["data"][30]["efficiency"], data["data"][31]["efficiency"], data["data"][32]["efficiency"]]
# fixed_pt1_800 = [data["data"][39]["efficiency"], data["data"][40]["efficiency"], data["data"][41]["efficiency"]]
# fixed_pt1_1000 = [data["data"][48]["efficiency"], data["data"][49]["efficiency"], data["data"][50]["efficiency"]]
# fixed_pt2_125 = [data["data"][6]["efficiency"], data["data"][7]["efficiency"], data["data"][8]["efficiency"]]
# fixed_pt2_200 = [data["data"][15]["efficiency"], data["data"][16]["efficiency"], data["data"][17]["efficiency"]]
# fixed_pt2_400 = [data["data"][24]["efficiency"], data["data"][25]["efficiency"], data["data"][26]["efficiency"]]
# fixed_pt2_600 = [data["data"][33]["efficiency"], data["data"][34]["efficiency"], data["data"][35]["efficiency"]]
# fixed_pt2_800 = [data["data"][42]["efficiency"], data["data"][43]["efficiency"], data["data"][44]["efficiency"]]
# fixed_pt2_1000 = [data["data"][51]["efficiency"], data["data"][52]["efficiency"], data["data"][53]["efficiency"]]

# err_pt05_125 = [data["data"][0]["error"], data["data"][1]["error"], data["data"][2]["error"]]
# err_pt05_200 = [data["data"][9]["error"], data["data"][10]["error"], data["data"][11]["error"]]
# err_pt05_400 = [data["data"][18]["error"], data["data"][19]["error"], data["data"][20]["error"]]
# err_pt05_600 = [data["data"][27]["error"], data["data"][28]["error"], data["data"][29]["error"]]
# err_pt05_800 = [data["data"][36]["error"], data["data"][37]["error"], data["data"][38]["error"]]
# err_pt05_1000 = [data["data"][45]["error"], data["data"][46]["error"], data["data"][47]["error"]]
# err_pt1_125 = [data["data"][3]["error"], data["data"][4]["error"], data["data"][5]["error"]]
# err_pt1_200 = [data["data"][12]["error"], data["data"][13]["error"], data["data"][14]["error"]]
# err_pt1_400 = [data["data"][21]["error"], data["data"][22]["error"], data["data"][23]["error"]]
# err_pt1_600 = [data["data"][30]["error"], data["data"][31]["error"], data["data"][32]["error"]]
# err_pt1_800 = [data["data"][39]["error"], data["data"][40]["error"], data["data"][41]["error"]]
# err_pt1_1000 = [data["data"][48]["error"], data["data"][49]["error"], data["data"][50]["error"]]
# err_pt2_125 = [data["data"][6]["error"], data["data"][7]["error"], data["data"][8]["error"]]
# err_pt2_200 = [data["data"][15]["error"], data["data"][16]["error"], data["data"][17]["error"]]
# err_pt2_400 = [data["data"][24]["error"], data["data"][25]["error"], data["data"][26]["error"]]
# err_pt2_600 = [data["data"][33]["error"], data["data"][34]["error"], data["data"][35]["error"]]
# err_pt2_800 = [data["data"][42]["error"], data["data"][43]["error"], data["data"][44]["error"]]
# err_pt2_1000 = [data["data"][51]["error"], data["data"][52]["error"], data["data"][53]["error"]]

# #Plot for individual pt, mass on x-axis, different ntrack lines
# fixed_pt05_n100 = [data["data"][0]["efficiency"], data["data"][9]["efficiency"], data["data"][18]["efficiency"],
#                    data["data"][27]["efficiency"], data["data"][36]["efficiency"], data["data"][45]["efficiency"]]
# fixed_pt05_n150 = [data["data"][1]["efficiency"], data["data"][10]["efficiency"], data["data"][19]["efficiency"],
#                    data["data"][28]["efficiency"], data["data"][37]["efficiency"], data["data"][46]["efficiency"]]
# fixed_pt05_n200 = [data["data"][2]["efficiency"], data["data"][11]["efficiency"], data["data"][20]["efficiency"],
#                    data["data"][29]["efficiency"], data["data"][38]["efficiency"], data["data"][47]["efficiency"]]
# fixed_pt1_n100 = [data["data"][3]["efficiency"], data["data"][12]["efficiency"], data["data"][21]["efficiency"],
#                   data["data"][30]["efficiency"], data["data"][39]["efficiency"], data["data"][48]["efficiency"]]
# fixed_pt1_n150 = [data["data"][4]["efficiency"], data["data"][13]["efficiency"], data["data"][22]["efficiency"],
#                   data["data"][31]["efficiency"], data["data"][40]["efficiency"], data["data"][49]["efficiency"]]
# fixed_pt1_n200 = [data["data"][5]["efficiency"], data["data"][14]["efficiency"], data["data"][23]["efficiency"],
#                   data["data"][32]["efficiency"], data["data"][41]["efficiency"], data["data"][50]["efficiency"]]
# fixed_pt2_n100 = [data["data"][6]["efficiency"], data["data"][15]["efficiency"], data["data"][24]["efficiency"],
#                   data["data"][33]["efficiency"], data["data"][42]["efficiency"], data["data"][51]["efficiency"]]
# fixed_pt2_n150 = [data["data"][7]["efficiency"], data["data"][16]["efficiency"], data["data"][25]["efficiency"],
#                   data["data"][34]["efficiency"], data["data"][43]["efficiency"], data["data"][52]["efficiency"]]
# fixed_pt2_n200 = [data["data"][8]["efficiency"], data["data"][17]["efficiency"], data["data"][26]["efficiency"],
#                   data["data"][35]["efficiency"], data["data"][44]["efficiency"], data["data"][53]["efficiency"]] 

# err_pt05_n100 = [data["data"][0]["error"], data["data"][9]["error"], data["data"][18]["error"],
#                  data["data"][27]["error"], data["data"][36]["error"], data["data"][45]["error"]]
# err_pt05_n150 = [data["data"][1]["error"], data["data"][10]["error"], data["data"][19]["error"],
#                  data["data"][28]["error"], data["data"][37]["error"], data["data"][46]["error"]]
# err_pt05_n200 = [data["data"][2]["error"], data["data"][11]["error"], data["data"][20]["error"],
#                  data["data"][29]["error"], data["data"][38]["error"], data["data"][47]["error"]]
# err_pt1_n100 = [data["data"][3]["error"], data["data"][12]["error"], data["data"][21]["error"],
#                 data["data"][30]["error"], data["data"][39]["error"], data["data"][48]["error"]]
# err_pt1_n150 = [data["data"][4]["error"], data["data"][13]["error"], data["data"][22]["error"],
#                 data["data"][31]["error"], data["data"][40]["error"], data["data"][49]["error"]]
# err_pt1_n200 = [data["data"][5]["error"], data["data"][14]["error"], data["data"][23]["error"],
#                 data["data"][32]["error"], data["data"][41]["error"], data["data"][50]["error"]]
# err_pt2_n100 = [data["data"][6]["error"], data["data"][15]["error"], data["data"][24]["error"],
#                 data["data"][33]["error"], data["data"][42]["error"], data["data"][51]["error"]]
# err_pt2_n150 = [data["data"][7]["error"], data["data"][16]["error"], data["data"][25]["error"],
#                 data["data"][34]["error"], data["data"][43]["error"], data["data"][52]["error"]]
# err_pt2_n200 = [data["data"][8]["error"], data["data"][17]["error"], data["data"][26]["error"],
#                 data["data"][35]["error"], data["data"][44]["error"], data["data"][53]["error"]] 


ht_125_05 = data["ht"][0]["ht_05"]
ht_125_1 = data["ht"][0]["ht_1"]
ht_125_2 = data["ht"][0]["ht_2"]

ht_200_05 = data["ht"][1]["ht_05"]
ht_200_1 = data["ht"][1]["ht_1"]
ht_200_2 = data["ht"][1]["ht_2"]

ht_400_05 = data["ht"][2]["ht_05"]
ht_400_1 = data["ht"][2]["ht_1"]
ht_400_2 = data["ht"][2]["ht_2"]

ht_600_05 = data["ht"][3]["ht_05"]
ht_600_1 = data["ht"][3]["ht_1"]
ht_600_2 = data["ht"][3]["ht_2"]

ht_800_05 = data["ht"][4]["ht_05"]
ht_800_1 = data["ht"][4]["ht_1"]
ht_800_2 = data["ht"][4]["ht_2"]

ht_1000_05 = data["ht"][5]["ht_05"]
ht_1000_1 = data["ht"][5]["ht_1"]
ht_1000_2 = data["ht"][5]["ht_2"]

f.close()




# #Fixed nTracks with mass on x-axis

# fig,axs = plt.subplots()
# axs.set_title("nTracks Cutoff: 100")
# axs.set_xlabel("Mass (GeV)")
# axs.set_ylabel("Efficiency")
# axs.errorbar(masses, fixed_n100_pt05, yerr = err_n100_pt05, label = "pT > 0.5 GeV", marker = "o", alpha = 0.5)
# axs.errorbar(masses, fixed_n100_pt1, yerr = err_n100_pt1, label = "pT > 1 GeV", marker = "o", alpha = 0.5)
# axs.errorbar(masses, fixed_n100_pt2, yerr = err_n100_pt2, label = "pT > 2 GeV", marker = "o", alpha = 0.5)
# axs.legend(fontsize = "small", frameon = False)
# fig.savefig('SUEPeff_n100_mass.svg', filetype = '.svg')

# fig,axs = plt.subplots()
# axs.set_title("nTracks Cutoff: 150")
# axs.set_xlabel("Mass (GeV)")
# axs.set_ylabel("Efficiency")
# axs.errorbar(masses, fixed_n150_pt05, yerr = err_n150_pt05, label = "pT > 0.5 GeV", marker = "o", alpha = 0.5)
# axs.errorbar(masses, fixed_n150_pt1, yerr = err_n150_pt1, label = "pT > 1 GeV", marker = "o", alpha = 0.5)
# axs.errorbar(masses, fixed_n150_pt2, yerr = err_n150_pt2, label = "pT > 2 GeV", marker = "o", alpha = 0.5)
# axs.legend(fontsize = "small", frameon = False)
# fig.savefig('SUEPeff_n150_mass.svg', filetype = '.svg')

# fig,axs = plt.subplots()
# axs.set_title("nTracks Cutoff: 200")
# axs.set_xlabel("Mass (GeV)")
# axs.set_ylabel("Efficiency")
# axs.errorbar(masses, fixed_n200_pt05, yerr = err_n200_pt05, label = "pT > 0.5 GeV", marker = "o", alpha = 0.5)
# axs.errorbar(masses, fixed_n200_pt1, yerr = err_n200_pt1, label = "pT > 1 GeV", marker = "o", alpha = 0.5)
# axs.errorbar(masses, fixed_n200_pt2, yerr = err_n200_pt2, label = "pT > 2 GeV", marker = "o", alpha = 0.5)
# axs.legend(fontsize = "small", frameon = False)
# fig.savefig('SUEPeff_n200_mass.svg', filetype = '.svg')



# #Fixed nTracks with pT on the x-axis

# fig,axs = plt.subplots()
# axs.set_title("nTracks Cutoff: 100")
# axs.set_xlabel("Transverse Momentum (GeV)")
# axs.set_ylabel("Efficiency")
# axs.errorbar(pts, fixed_n100_125, yerr = err_n100_125, label = "mass 125 GeV", marker = "o", alpha = 0.5)
# axs.errorbar(pts, fixed_n100_200, yerr = err_n100_200, label = "mass 200 GeV", marker = "o", alpha = 0.5)
# axs.errorbar(pts, fixed_n100_400, yerr = err_n100_400, label = "mass 400 GeV", marker = "o", alpha = 0.5)
# axs.errorbar(pts, fixed_n100_600, yerr = err_n100_600, label = "mass 600 GeV", marker = "o", alpha = 0.5)
# axs.errorbar(pts, fixed_n100_800, yerr = err_n100_800, label = "mass 800 GeV", marker = "o", alpha = 0.5)
# axs.errorbar(pts, fixed_n100_1000, yerr = err_n100_1000, label = "mass 1000 GeV", marker = "o", alpha = 0.5)
# axs.legend(fontsize = "small", frameon = False)
# fig.savefig('SUEPeff_n100_pt.svg', filetype = '.svg')

# fig,axs = plt.subplots()
# axs.set_title("nTracks Cutoff: 150")
# axs.set_xlabel("Transverse Momentum (GeV)")
# axs.set_ylabel("Efficiency")
# axs.errorbar(pts, fixed_n150_125, yerr = err_n150_125, label = "mass 125 GeV", marker = "o", alpha = 0.5)
# axs.errorbar(pts, fixed_n150_200, yerr = err_n150_200, label = "mass 200 GeV", marker = "o", alpha = 0.5)
# axs.errorbar(pts, fixed_n150_400, yerr = err_n150_400, label = "mass 400 GeV", marker = "o", alpha = 0.5)
# axs.errorbar(pts, fixed_n150_600, yerr = err_n150_600, label = "mass 600 GeV", marker = "o", alpha = 0.5)
# axs.errorbar(pts, fixed_n150_800, yerr = err_n150_800, label = "mass 800 GeV", marker = "o", alpha = 0.5)
# axs.errorbar(pts, fixed_n150_1000, yerr = err_n150_1000, label = "mass 1000 GeV", marker = "o", alpha = 0.5)
# axs.legend(fontsize = "small", frameon = False)
# fig.savefig('SUEPeff_n150_pt.svg', filetype = '.svg')

# fig,axs = plt.subplots()
# axs.set_title("nTracks Cutoff: 200")
# axs.set_xlabel("Transverse Momentum (GeV)")
# axs.set_ylabel("Efficiency")
# axs.errorbar(pts, fixed_n200_125, yerr = err_n200_125, label = "mass 125 GeV", marker = "o", alpha = 0.5)
# axs.errorbar(pts, fixed_n200_200, yerr = err_n200_200, label = "mass 200 GeV", marker = "o", alpha = 0.5)
# axs.errorbar(pts, fixed_n200_400, yerr = err_n200_400, label = "mass 400 GeV", marker = "o", alpha = 0.5)
# axs.errorbar(pts, fixed_n200_600, yerr = err_n200_600, label = "mass 600 GeV", marker = "o", alpha = 0.5)
# axs.errorbar(pts, fixed_n200_800, yerr = err_n200_800, label = "mass 800 GeV", marker = "o", alpha = 0.5)
# axs.errorbar(pts, fixed_n200_1000, yerr = err_n200_1000, label = "mass 1000 GeV", marker = "o", alpha = 0.5)
# axs.legend(fontsize = "small", frameon = False)
# fig.savefig('SUEPeff_n200_pt.svg', filetype = '.svg')



# #Fixed mass with ntracks on the x-axis

# fig,axs = plt.subplots()
# axs.set_title("mass: 125 GeV")
# axs.set_xlabel("nTracks")
# axs.set_ylabel("Efficiency")
# axs.errorbar(ntracks, fixed_125_pt05, yerr = err_125_pt05, label = "pt > 0.5 GeV", marker = "o", alpha = 0.5)
# axs.errorbar(ntracks, fixed_125_pt1, yerr = err_125_pt1, label = "pt > 1 GeV", marker = "o", alpha = 0.5)
# axs.errorbar(ntracks, fixed_125_pt2, yerr = err_125_pt2, label = "pt > 2 GeV", marker = "o", alpha =0.5)
# axs.legend(fontsize = "small", frameon = False)
# fig.savefig('SUEPeff_125_ntracks.svg', filetype = '.svg')

# fig,axs = plt.subplots()
# axs.set_title("mass: 200 GeV")
# axs.set_xlabel("nTracks")
# axs.set_ylabel("Efficiency")
# axs.errorbar(ntracks, fixed_200_pt05, yerr = err_200_pt05, label = "pt > 0.5 GeV", marker = "o", alpha = 0.5)
# axs.errorbar(ntracks, fixed_200_pt1, yerr = err_200_pt1, label = "pt > 1 GeV", marker = "o", alpha = 0.5)
# axs.errorbar(ntracks, fixed_200_pt2, yerr = err_200_pt2, label = "pt > 2 GeV", marker = "o", alpha = 0.5)
# axs.legend(fontsize = "small", frameon = False)
# fig.savefig('SUEPeff_200_ntracks.svg', filetype = '.svg')

# fig,axs = plt.subplots()
# axs.set_title("mass: 400 GeV")
# axs.set_xlabel("nTracks")
# axs.set_ylabel("Efficiency")
# axs.errorbar(ntracks, fixed_400_pt05, yerr = err_400_pt05, label = "pt > 0.5 GeV", marker = "o", alpha = 0.5)
# axs.errorbar(ntracks, fixed_400_pt1, yerr = err_400_pt1, label = "pt > 1 GeV", marker = "o", alpha = 0.5)
# axs.errorbar(ntracks, fixed_400_pt2, yerr = err_400_pt2, label = "pt > 2 GeV", marker = "o", alpha = 0.5)
# axs.legend(fontsize = "small", frameon = False)
# fig.savefig('SUEPeff_400_ntracks.svg', filetype = '.svg')

# fig,axs = plt.subplots()
# axs.set_title("mass: 600 GeV")
# axs.set_xlabel("nTracks")
# axs.set_ylabel("Efficiency")
# axs.errorbar(ntracks, fixed_600_pt05, yerr = err_600_pt05, label = "pt > 0.5 GeV", marker = "o", alpha = 0.5)
# axs.errorbar(ntracks, fixed_600_pt1, yerr = err_600_pt1, label = "pt > 1 GeV", marker = "o", alpha = 0.5)
# axs.errorbar(ntracks, fixed_600_pt2, yerr = err_600_pt2, label = "pt > 2 GeV", marker = "o", alpha = 0.5)
# axs.legend(fontsize = "small", frameon = False)
# fig.savefig('SUEPeff_600_ntracks.svg', filetype = '.svg')

# fig,axs = plt.subplots()
# axs.set_title("mass: 800 GeV")
# axs.set_xlabel("nTracks")
# axs.set_ylabel("Efficiency")
# axs.errorbar(ntracks, fixed_800_pt05, yerr = err_800_pt05, label = "pt > 0.5 GeV", marker = "o", alpha = 0.5)
# axs.errorbar(ntracks, fixed_800_pt1, yerr = err_800_pt1, label = "pt > 1 GeV", marker = "o", alpha = 0.5)
# axs.errorbar(ntracks, fixed_800_pt2, yerr = err_800_pt2, label = "pt > 2 GeV", marker = "o", alpha = 0.5)
# axs.legend(fontsize = "small", frameon = False)
# fig.savefig('SUEPeff_800_ntracks.svg', filetype = '.svg')

# fig,axs = plt.subplots()
# axs.set_title("mass: 1000 GeV")
# axs.set_xlabel("nTracks")
# axs.set_ylabel("Efficiency")
# axs.errorbar(ntracks, fixed_1000_pt05, yerr = err_1000_pt05, label = "pt > 0.5 GeV", marker = "o", alpha = 0.5)
# axs.errorbar(ntracks, fixed_1000_pt1, yerr = err_1000_pt1, label = "pt > 1 GeV", marker = "o", alpha = 0.5)
# axs.errorbar(ntracks, fixed_1000_pt2, yerr = err_1000_pt2, label = "pt > 2 GeV", marker = "o", alpha = 0.5)
# axs.legend(fontsize = "small", frameon = False)
# fig.savefig('SUEPeff_1000_ntracks.svg', filetype = '.svg')



# #Fixed mass with pT on the x-axis

# fig,axs = plt.subplots()
# axs.set_title("mass: 125 GeV")
# axs.set_xlabel("Transverse Momentum (GeV)")
# axs.set_ylabel("Efficiency")
# axs.errorbar(pts, fixed_125_n100, yerr = err_125_n100, label = "nTracks > 100", marker = "o", alpha = 0.5)
# axs.errorbar(pts, fixed_125_n150, yerr = err_125_n150, label = "nTracks > 150", marker = "o", alpha = 0.5)
# axs.errorbar(pts, fixed_125_n200, yerr = err_125_n200, label = "nTracks > 200", marker = "o", alpha = 0.5)
# axs.legend(fontsize = "small", frameon = False)
# fig.savefig('SUEPeff_125_pt.svg', filetype = '.svg')

# fig,axs = plt.subplots()
# axs.set_title("mass: 200 GeV")
# axs.set_xlabel("Transverse Momentum (GeV)")
# axs.set_ylabel("Efficiency")
# axs.errorbar(pts, fixed_200_n100, yerr = err_200_n100, label = "nTracks > 100", marker = "o", alpha = 0.5)
# axs.errorbar(pts, fixed_200_n150, yerr = err_200_n150, label = "nTracks > 150", marker = "o", alpha = 0.5)
# axs.errorbar(pts, fixed_200_n200, yerr = err_200_n200, label = "nTracks > 200", marker = "o", alpha = 0.5)
# axs.legend(fontsize = "small", frameon = False)
# fig.savefig('SUEPeff_200_pt.svg', filetype = '.svg')

# fig,axs = plt.subplots()
# axs.set_title("mass: 400 GeV")
# axs.set_xlabel("Transverse Momentum (GeV)")
# axs.set_ylabel("Efficiency")
# axs.errorbar(pts, fixed_400_n100, yerr = err_400_n100, label = "nTracks > 100", marker = "o", alpha = 0.5)
# axs.errorbar(pts, fixed_400_n150, yerr = err_400_n150, label = "nTracks > 150", marker = "o", alpha = 0.5)
# axs.errorbar(pts, fixed_400_n200, yerr = err_400_n200, label = "nTracks > 200", marker = "o", alpha = 0.5)
# axs.legend(fontsize = "small", frameon = False)
# fig.savefig('SUEPeff_400_pt.svg', filetype = '.svg')

# fig,axs = plt.subplots()
# axs.set_title("mass: 600 GeV")
# axs.set_xlabel("Transverse Momentum (GeV)")
# axs.set_ylabel("Efficiency")
# axs.errorbar(pts, fixed_600_n100, yerr = err_600_n100, label = "nTracks > 100", marker = "o", alpha = 0.5)
# axs.errorbar(pts, fixed_600_n150, yerr = err_600_n150, label = "nTracks > 150", marker = "o", alpha = 0.5)
# axs.errorbar(pts, fixed_600_n200, yerr = err_600_n200, label = "nTracks > 200", marker = "o", alpha = 0.5)
# axs.legend(fontsize = "small", frameon = False)
# fig.savefig('SUEPeff_600_pt.svg', filetype = '.svg')

# fig,axs = plt.subplots()
# axs.set_title("mass: 800 GeV")
# axs.set_xlabel("Transverse Momentum (GeV)")
# axs.set_ylabel("Efficiency")
# axs.errorbar(pts, fixed_800_n100, yerr = err_800_n100, label = "nTracks > 100", marker = "o", alpha = 0.5)
# axs.errorbar(pts, fixed_800_n150, yerr = err_800_n150, label = "nTracks > 150", marker = "o", alpha = 0.5)
# axs.errorbar(pts, fixed_800_n200, yerr = err_800_n200, label = "nTracks > 200", marker = "o", alpha = 0.5)
# axs.legend(fontsize = "small", frameon = False)
# fig.savefig('SUEPeff_800_pt.svg', filetype = '.svg')

# fig,axs = plt.subplots()
# axs.set_title("mass: 1000 GeV")
# axs.set_xlabel("Transverse Momentum (GeV)")
# axs.set_ylabel("Efficiency")
# axs.errorbar(pts, fixed_1000_n100, yerr = err_1000_n100, label = "nTracks > 100", marker = "o", alpha = 0.5)
# axs.errorbar(pts, fixed_1000_n150, yerr = err_1000_n150, label = "nTracks > 150", marker = "o", alpha = 0.5)
# axs.errorbar(pts, fixed_1000_n200, yerr = err_1000_n200, label = "nTracks > 200", marker = "o", alpha = 0.5)
# axs.legend(fontsize = "small", frameon = False)
# fig.savefig('SUEPeff_1000_pt.svg', filetype = '.svg')



# #Fixed pT with ntracks on the x-axis

# fig,axs = plt.subplots()
# axs.set_title("Transverse Momentum Cutoff: 0.5 GeV")
# axs.set_xlabel("nTracks")
# axs.set_ylabel("Efficiency")
# axs.errorbar(ntracks, fixed_pt05_125, yerr = err_pt05_125, label = "mass 125 GeV", marker = "o", alpha = 0.5)
# axs.errorbar(ntracks, fixed_pt05_200, yerr = err_pt05_200, label = "mass 200 GeV", marker = "o", alpha = 0.5)
# axs.errorbar(ntracks, fixed_pt05_400, yerr = err_pt05_400, label = "mass 400 GeV", marker = "o", alpha = 0.5)
# axs.errorbar(ntracks, fixed_pt05_600, yerr = err_pt05_600, label = "mass 600 GeV", marker = "o", alpha = 0.5)
# axs.errorbar(ntracks, fixed_pt05_800, yerr = err_pt05_800, label = "mass 800 GeV", marker = "o", alpha = 0.5)
# axs.errorbar(ntracks, fixed_pt05_1000, yerr = err_pt05_1000, label = "mass 1000 GeV", marker = "o", alpha = 0.5)
# axs.legend(fontsize = "small", frameon = False)
# fig.savefig('SUEPeff_pt05_ntracks.svg', filetype = '.svg')

# fig,axs = plt.subplots()
# axs.set_title("Transverse Momentum Cutoff: 1 GeV")
# axs.set_xlabel("nTracks")
# axs.set_ylabel("Efficiency")
# axs.errorbar(ntracks, fixed_pt1_125, yerr = err_pt1_125, label = "mass 125 GeV", marker = "o", alpha = 0.5)
# axs.errorbar(ntracks, fixed_pt1_200, yerr = err_pt1_200, label = "mass 200 GeV", marker = "o", alpha = 0.5)
# axs.errorbar(ntracks, fixed_pt1_400, yerr = err_pt1_400, label = "mass 400 GeV", marker = "o", alpha = 0.5)
# axs.errorbar(ntracks, fixed_pt1_600, yerr = err_pt1_600, label = "mass 600 GeV", marker = "o", alpha = 0.5)
# axs.errorbar(ntracks, fixed_pt1_800, yerr = err_pt1_800, label = "mass 800 GeV", marker = "o", alpha = 0.5)
# axs.errorbar(ntracks, fixed_pt1_1000, yerr = err_pt1_1000, label = "mass 1000 GeV", marker = "o", alpha = 0.5)
# axs.legend(fontsize = "small", frameon = False)
# fig.savefig('SUEPeff_pt1_ntracks.svg', filetype = '.svg')

# fig,axs = plt.subplots()
# axs.set_title("Transverse Momentum Cutoff: 2 GeV")
# axs.set_xlabel("nTracks")
# axs.set_ylabel("Efficiency")
# axs.errorbar(ntracks, fixed_pt2_125, yerr = err_pt2_125, label = "mass 125 GeV", marker = "o", alpha = 0.5)
# axs.errorbar(ntracks, fixed_pt2_200, yerr = err_pt2_200, label = "mass 200 GeV", marker = "o", alpha = 0.5)
# axs.errorbar(ntracks, fixed_pt2_400, yerr = err_pt2_400, label = "mass 400 GeV", marker = "o", alpha = 0.5)
# axs.errorbar(ntracks, fixed_pt2_600, yerr = err_pt2_600, label = "mass 600 GeV", marker = "o", alpha = 0.5)
# axs.errorbar(ntracks, fixed_pt2_800, yerr = err_pt2_800, label = "mass 800 GeV", marker = "o", alpha = 0.5)
# axs.errorbar(ntracks, fixed_pt2_1000, yerr = err_pt2_1000, label = "mass 1000 GeV", marker = "o", alpha = 0.5)
# axs.legend(fontsize = "small", frameon = False)
# fig.savefig('SUEPeff_pt2_ntracks.svg', filetype = '.svg')



# #Fixed pT with mass on the x-axis

# fig,axs = plt.subplots()
# axs.set_title("Transverse Momentum Cutoff: 0.5 GeV")
# axs.set_xlabel("Mass (GeV)")
# axs.set_ylabel("Efficiency")
# axs.errorbar(masses, fixed_pt05_n100, yerr = err_pt05_n100, label = "nTracks > 100", marker = "o", alpha = 0.5)
# axs.errorbar(masses, fixed_pt05_n150, yerr = err_pt05_n150, label = "nTracks > 150", marker = "o", alpha = 0.5)
# axs.errorbar(masses, fixed_pt05_n200, yerr = err_pt05_n200, label = "nTracks > 200", marker = "o", alpha = 0.5)
# axs.legend(fontsize = "small", frameon = False)
# fig.savefig('SUEPeff_pt05_mass.svg', filetype = '.svg')

# fig,axs = plt.subplots()
# axs.set_title("Transverse Momentum Cutoff: 1 GeV")
# axs.set_xlabel("Mass (GeV)")
# axs.set_ylabel("Efficiency")
# axs.errorbar(masses, fixed_pt1_n100, yerr = err_pt1_n100, label = "nTracks > 100", marker = "o", alpha = 0.5)
# axs.errorbar(masses, fixed_pt1_n150, yerr = err_pt1_n150, label = "nTracks > 150", marker = "o", alpha = 0.5)
# axs.errorbar(masses, fixed_pt1_n200, yerr = err_pt1_n200, label = "nTracks > 200", marker = "o", alpha = 0.5)
# axs.legend(fontsize = "small", frameon = False)
# fig.savefig('SUEPeff_pt1_mass.svg', filetype = '.svg')

# fig,axs = plt.subplots()
# axs.set_title("Transverse Momentum Cutoff: 2 GeV")
# axs.set_xlabel("Mass (GeV)")
# axs.set_ylabel("Efficiency")
# axs.errorbar(masses, fixed_pt2_n100, yerr = err_pt2_n100, label = "nTracks > 100", marker = "o", alpha = 0.5)
# axs.errorbar(masses, fixed_pt2_n150, yerr = err_pt2_n150, label = "nTracks > 150", marker = "o", alpha = 0.5)
# axs.errorbar(masses, fixed_pt2_n200, yerr = err_pt2_n200, label = "nTracks > 200", marker = "o", alpha = 0.5)
# axs.legend(fontsize = "small", frameon = False)
# fig.savefig('SUEPeff_pt2_mass.svg', filetype = '.svg')



bin_125_max = max(max(ht_125_05), max(ht_125_1), max(ht_125_2))
bin_200_max = max(max(ht_200_05), max(ht_200_1), max(ht_200_2))
bin_400_max = max(max(ht_400_05), max(ht_400_1), max(ht_400_2))
bin_600_max = max(max(ht_600_05), max(ht_600_1), max(ht_600_2))
bin_800_max = max(max(ht_800_05), max(ht_800_1), max(ht_800_2))
bin_1000_max = max(max(ht_1000_05), max(ht_1000_1), max(ht_1000_2))
bin_05_max = max(max(ht_125_05), max(ht_200_05), max(ht_400_05), max(ht_600_05), max(ht_800_05), max(ht_1000_05))
bin_1_max = max(max(ht_125_1), max(ht_200_1), max(ht_400_1), max(ht_600_1), max(ht_800_1), max(ht_1000_1)) 
bin_2_max = max(max(ht_125_2), max(ht_200_2), max(ht_400_2), max(ht_600_2), max(ht_800_2), max(ht_1000_2))

bin_list_125 = numpy.arange(0, 2000, 100)
bin_list_200 = numpy.arange(0, 2000, 100)
bin_list_400 = numpy.arange(0, 2000, 100)
bin_list_600 = numpy.arange(0, 2000, 100)
bin_list_800 = numpy.arange(0, 2000, 100)
bin_list_1000 = numpy.arange(0, 2000, 100)
bin_list_05 = numpy.arange(0, 3000, 100)
bin_list_1 = numpy.arange(0, 3000, 100)
bin_list_2 = numpy.arange(0, 3000, 100)

# #HT plots for fixed mass

# fig,axs = plt.subplots()
# axs.set_title("HT for 125 GeV Mass")
# axs.set_xlabel("HT (GeV)")
# axs.set_ylabel("Events")
# axs.hist(ht_125_05, histtype = "step", bins = bin_list_125, label = "pT > 0.5 GeV")
# axs.hist(ht_125_1, histtype = "step", bins = bin_list_125, label = "pT > 1 GeV")
# axs.hist(ht_125_2, histtype = "step", bins = bin_list_125, label = "pT > 2 GeV")
# axs.legend(fontsize = "small", frameon = False)
# fig.savefig('SUEP_ht_125.svg', filetype = '.svg')

# fig,axs = plt.subplots()
# axs.set_title("HT for 200 GeV Mass")
# axs.set_xlabel("HT (GeV)")
# axs.set_ylabel("Events")
# axs.hist(ht_200_05, histtype = "step", bins = bin_list_200, label = "pT > 0.5 GeV")
# axs.hist(ht_200_1, histtype = "step", bins = bin_list_200, label = "pT > 1 GeV")
# axs.hist(ht_200_2, histtype = "step", bins = bin_list_200, label = "pT > 2 GeV")
# axs.legend(fontsize = "small", frameon = False)
# fig.savefig('SUEP_ht_200.svg', filetype = '.svg')

# fig,axs = plt.subplots()
# axs.set_title("HT for 400 GeV Mass")
# axs.set_xlabel("HT (GeV)")
# axs.set_ylabel("Events")
# axs.hist(ht_400_05, histtype = "step", bins = bin_list_400, label = "pT > 0.5 GeV")
# axs.hist(ht_400_1, histtype = "step", bins = bin_list_400, label = "pT > 1 GeV")
# axs.hist(ht_400_2, histtype = "step", bins = bin_list_400, label = "pT > 2 GeV")
# axs.legend(fontsize = "small", frameon = False)
# fig.savefig('SUEP_ht_400.svg', filetype = '.svg')

# fig,axs = plt.subplots()
# axs.set_title("HT for 600 GeV Mass")
# axs.set_xlabel("HT (GeV)")
# axs.set_ylabel("Events")
# axs.hist(ht_600_05, histtype = "step", bins = bin_list_600, label = "pT > 0.5 GeV")
# axs.hist(ht_600_1, histtype = "step", bins = bin_list_600, label = "pT > 1 GeV")
# axs.hist(ht_600_2, histtype = "step", bins = bin_list_600, label = "pT > 2 GeV")
# axs.legend(fontsize = "small", frameon = False)
# fig.savefig('SUEP_ht_600.svg', filetype = '.svg')

# fig,axs = plt.subplots()
# axs.set_title("HT for 800 GeV Mass")
# axs.set_xlabel("HT (GeV)")
# axs.set_ylabel("Events")
# axs.hist(ht_800_05, histtype = "step", bins = bin_list_800, label = "pT > 0.5 GeV")
# axs.hist(ht_800_1, histtype = "step", bins = bin_list_800, label = "pT > 1 GeV")
# axs.hist(ht_800_2, histtype = "step", bins = bin_list_800, label = "pT > 2 GeV")
# axs.legend(fontsize = "small", frameon = False)
# fig.savefig('SUEP_ht_800.svg', filetype = '.svg')

# fig,axs = plt.subplots()
# axs.set_title("HT for 1000 GeV Mass")
# axs.set_xlabel("HT (GeV)")
# axs.set_ylabel("Events")
# axs.hist(ht_1000_05, histtype = "step", bins = bin_list_1000, label = "pT > 0.5 GeV")
# axs.hist(ht_1000_1, histtype = "step", bins = bin_list_1000, label = "pT > 1 GeV")
# axs.hist(ht_1000_2, histtype = "step", bins = bin_list_1000, label = "pT > 2 GeV")
# axs.legend(fontsize = "small", frameon = False)
# fig.savefig('SUEP_ht_1000.svg', filetype = '.svg')



# #HT plots for fixed pt cutoff

# fig,axs = plt.subplots()
# axs.set_title("HT for 0.5 GeV Transverse Momentum Cutoff")
# axs.set_xlabel("HT (GeV)")
# axs.set_ylabel("Events")
# axs.hist(ht_125_05, histtype = "step", bins = bin_list_05, label = "125 GeV")
# axs.hist(ht_200_05, histtype = "step", bins = bin_list_05, label = "200 GeV")
# axs.hist(ht_400_05, histtype = "step", bins = bin_list_05, label = "400 GeV")
# axs.hist(ht_600_05, histtype = "step", bins = bin_list_05, label = "600 GeV")
# axs.hist(ht_800_05, histtype = "step", bins = bin_list_05, label = "800 GeV")
# axs.hist(ht_1000_05, histtype = "step", bins = bin_list_05, label = "1000 GeV")
# axs.legend(fontsize = "small", frameon = False)
# fig.savefig('SUEP_ht_pt05.svg', filetype = '.svg')

fig,axs = plt.subplots()
axs.set_title("HT for 1 GeV Transverse Momentum Cutoff")
axs.set_xlabel("HT (GeV)")
axs.set_ylabel("Events")
axs.hist(ht_125_1, histtype = "step", bins = bin_list_1, label = "125 GeV")
axs.hist(ht_200_1, histtype = "step", bins = bin_list_1, label = "200 GeV")
axs.hist(ht_400_1, histtype = "step", bins = bin_list_1, label = "400 GeV")
axs.hist(ht_600_1, histtype = "step", bins = bin_list_1, label = "600 GeV")
axs.hist(ht_800_1, histtype = "step", bins = bin_list_1, label = "800 GeV")
axs.hist(ht_1000_1, histtype = "step", bins = bin_list_1, label = "1000 GeV")
axs.legend(fontsize = "small", frameon = False)
fig.savefig('SUEP_ht_pt1.svg', filetype = '.svg')

# fig,axs = plt.subplots()
# axs.set_title("HT for 2 GeV Transverse Momentum Cutoff")
# axs.set_xlabel("HT (GeV)")
# axs.set_ylabel("Events")
# axs.hist(ht_125_2, histtype = "step", bins = bin_list_2, label = "125 GeV")
# axs.hist(ht_200_2, histtype = "step", bins = bin_list_2, label = "200 GeV")
# axs.hist(ht_400_2, histtype = "step", bins = bin_list_2, label = "400 GeV")
# axs.hist(ht_600_2, histtype = "step", bins = bin_list_2, label = "600 GeV")
# axs.hist(ht_800_2, histtype = "step", bins = bin_list_2, label = "800 GeV")
# axs.hist(ht_1000_2, histtype = "step", bins = bin_list_2, label = "1000 GeV")
# axs.legend(fontsize = "small", frameon = False)
# fig.savefig('SUEP_ht_pt2.svg', filetype = '.svg')

