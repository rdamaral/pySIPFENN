import unittest
import csv
import os
from pymatgen.core import Structure
from tqdm import tqdm
import numpy as np
from natsort import natsorted
from importlib import resources

from pysipfenn.descriptorDefinitions import KS2022, KS2022_dilute

with resources.files('pysipfenn').\
        joinpath('descriptorDefinitions/labels_KS2022_dilute.csv').open('r', newline='') as f:
    reader = csv.reader(f)
    labels = [l[0] for l in list(reader)]

testMaterialsLabels = ['mp-13','mp-27','mp-165','mp-1211280']
matStrList = ['{"@module": "pymatgen.core.structure", "@class": "Structure", "charge": 0, "lattice": {"matrix": [[2.318956, 0.000185, -0.819712], [-1.159251, 2.008215, -0.819524], [2.5e-05, 0.000273, 2.459206]], "pbc": [true, true, true], "a": 2.4595700289085083, "b": 2.4593515311565364, "c": 2.4592060152801354, "alpha": 109.45958252256221, "beta": 109.46706290007663, "gamma": 109.46912204302215, "volume": 11.453776235839058}, "sites": [{"species": [{"element": "Fe", "occu": 1}], "abc": [0.0, 0.0, 0.0], "xyz": [0.0, 0.0, 0.0], "label": "Fe", "properties": {"magmom": 2.211}}], "@version": null}', '{"@module": "pymatgen.core.structure", "@class": "Structure", "charge": 0, "lattice": {"matrix": [[0.0, 1.934742, 1.934742], [1.934742, 0.0, 1.934742], [1.934742, 1.934742, 0.0]], "pbc": [true, true, true], "a": 2.7361383760928466, "b": 2.7361383760928466, "c": 2.7361383760928466, "alpha": 60.00000000000001, "beta": 60.00000000000001, "gamma": 60.00000000000001, "volume": 14.484355462473692}, "sites": [{"species": [{"element": "Si", "occu": 1}], "abc": [0.0, 0.0, 0.0], "xyz": [0.0, 0.0, 0.0], "label": "Si", "properties": {"magmom": -0.0}}], "@version": null}', '{"@module": "pymatgen.core.structure", "@class": "Structure", "charge": 0, "lattice": {"matrix": [[1.925241, -3.334615, 0.0], [1.925241, 3.334615, 0.0], [0.0, 0.0, 6.365686]], "pbc": [true, true, true], "a": 3.8504818018406475, "b": 3.8504818018406475, "c": 6.365686, "alpha": 90.0, "beta": 90.0, "gamma": 119.99999659520081, "volume": 81.73461274842057}, "sites": [{"species": [{"element": "Si", "occu": 1}], "abc": [0.333333, 0.666667, 0.062956], "xyz": [1.9252409999999998, 1.11154055641, 0.400758127816], "label": "Si", "properties": {"magmom": 0.0}}, {"species": [{"element": "Si", "occu": 1}], "abc": [0.666667, 0.333333, 0.562956], "xyz": [1.9252409999999998, -1.11154055641, 3.5836011278160003], "label": "Si", "properties": {"magmom": 0.0}}, {"species": [{"element": "Si", "occu": 1}], "abc": [0.333333, 0.666667, 0.437044], "xyz": [1.9252409999999998, 1.11154055641, 2.782084872184], "label": "Si", "properties": {"magmom": 0.0}}, {"species": [{"element": "Si", "occu": 1}], "abc": [0.666667, 0.333333, 0.937044], "xyz": [1.9252409999999998, -1.11154055641, 5.964927872184], "label": "Si", "properties": {"magmom": 0.0}}], "@version": null}', '{"@module": "pymatgen.core.structure", "@class": "Structure", "charge": 0, "lattice": {"matrix": [[-4.89682112, 0.0, 0.0], [0.0, 0.0, -12.78502184], [0.0, -15.51797977, 0.0]], "pbc": [true, true, true], "a": 4.89682112, "b": 12.78502184, "c": 15.51797977, "alpha": 90.0, "beta": 90.0, "gamma": 90.0, "volume": 971.5180978201984}, "sites": [{"species": [{"element": "Nb", "occu": 1}], "abc": [0.0, 0.97478069, 0.30478108], "xyz": [0.0, -4.7295866337187515, -12.462592410860271], "label": "Nb", "properties": {"magmom": 0.026}}, {"species": [{"element": "Nb", "occu": 1}], "abc": [0.5, 0.47478069, 0.69521892], "xyz": [-2.44841056, -10.788393136281249, -6.07008149086027], "label": "Nb", "properties": {"magmom": 0.026}}, {"species": [{"element": "Nb", "occu": 1}], "abc": [0.0, 0.29579212, 0.10069205], "xyz": [0.0, -1.5625371948998286, -3.781708714299901], "label": "Nb", "properties": {"magmom": -0.044}}, {"species": [{"element": "Nb", "occu": 1}], "abc": [0.5, 0.79579212, 0.89930795], "xyz": [-2.44841056, -13.955442575100172, -10.1742196342999], "label": "Nb", "properties": {"magmom": -0.044}}, {"species": [{"element": "Nb", "occu": 1}], "abc": [0.0, 0.76944669, 0.46134953], "xyz": [0.0, -7.159212673439009, -9.83739273636571], "label": "Nb", "properties": {"magmom": -0.021}}, {"species": [{"element": "Nb", "occu": 1}], "abc": [0.5, 0.26944669, 0.53865047], "xyz": [-2.44841056, -8.358767096560992, -3.44488181636571], "label": "Nb", "properties": {"magmom": -0.021}}, {"species": [{"element": "Nb", "occu": 1}], "abc": [0.0, 0.48356945, 0.97894996], "xyz": [0.0, -15.19132567512231, -6.182445979406788], "label": "Nb", "properties": {"magmom": -0.089}}, {"species": [{"element": "Nb", "occu": 1}], "abc": [0.5, 0.98356945, 0.02105004], "xyz": [-2.44841056, -0.3266540948776908, -12.574956899406788], "label": "Nb", "properties": {"magmom": -0.089}}, {"species": [{"element": "Nb", "occu": 1}], "abc": [0.0, 0.41237245, 0.5801905], "xyz": [0.0, -9.003384441746187, -5.272190779464308], "label": "Nb", "properties": {"magmom": -0.051}}, {"species": [{"element": "Nb", "occu": 1}], "abc": [0.5, 0.91237245, 0.4198095], "xyz": [-2.44841056, -6.514595328253815, -11.664701699464308], "label": "Nb", "properties": {"magmom": -0.051}}, {"species": [{"element": "Nb", "occu": 1}], "abc": [0.0, 0.79693267, 0.79114278], "xyz": [0.0, -12.27693765522156, -10.188801590959514], "label": "Nb", "properties": {"magmom": -0.01}}, {"species": [{"element": "Nb", "occu": 1}], "abc": [0.5, 0.29693267, 0.20885722], "xyz": [-2.44841056, -3.2410421147784394, -3.7962906709595132], "label": "Nb", "properties": {"magmom": -0.01}}, {"species": [{"element": "Nb", "occu": 1}], "abc": [0.0, 0.40858743, 0.80251763], "xyz": [0.0, -12.453452347408344, -5.223799216099471], "label": "Nb", "properties": {"magmom": 0.074}}, {"species": [{"element": "Nb", "occu": 1}], "abc": [0.5, 0.90858743, 0.19748237], "xyz": [-2.44841056, -3.064527422591655, -11.616310136099472], "label": "Nb", "properties": {"magmom": 0.074}}, {"species": [{"element": "Nb", "occu": 1}], "abc": [0.0, 0.11012415, 0.99274797], "xyz": [0.0, -15.405442915168567, -1.407939662861436], "label": "Nb", "properties": {"magmom": -0.106}}, {"species": [{"element": "Nb", "occu": 1}], "abc": [0.5, 0.61012415, 0.00725203], "xyz": [-2.44841056, -0.1125368548314331, -7.800450582861436], "label": "Nb", "properties": {"magmom": -0.106}}, {"species": [{"element": "Nb", "occu": 1}], "abc": [0.0, 0.13724645, 0.5962987], "xyz": [0.0, -9.253351163477298, -1.754698860712468], "label": "Nb", "properties": {"magmom": 0.03}}, {"species": [{"element": "Nb", "occu": 1}], "abc": [0.5, 0.63724645, 0.4037013], "xyz": [-2.44841056, -6.264628606522701, -8.147209780712469], "label": "Nb", "properties": {"magmom": 0.03}}, {"species": [{"element": "Nb", "occu": 1}], "abc": [0.0, 0.17851661, 0.81163442], "xyz": [0.0, -12.594926510195682, -2.2823387576527625], "label": "Nb", "properties": {"magmom": 0.02}}, {"species": [{"element": "Nb", "occu": 1}], "abc": [0.5, 0.67851661, 0.18836558], "xyz": [-2.44841056, -2.9230532598043166, -8.674849677652762], "label": "Nb", "properties": {"magmom": 0.02}}, {"species": [{"element": "Nb", "occu": 1}], "abc": [0.0, 0.20409406, 0.29225008], "xyz": [0.0, -4.535130829220882, -2.6093470145142703], "label": "Nb", "properties": {"magmom": -0.082}}, {"species": [{"element": "Nb", "occu": 1}], "abc": [0.5, 0.70409406, 0.70774992], "xyz": [-2.44841056, -10.98284894077912, -9.00185793451427], "label": "Nb", "properties": {"magmom": -0.082}}, {"species": [{"element": "Nb", "occu": 1}], "abc": [0.0, 0.60209736, 0.28731942], "xyz": [0.0, -4.458616947088133, -7.697827897406343], "label": "Nb", "properties": {"magmom": 0.033}}, {"species": [{"element": "Nb", "occu": 1}], "abc": [0.5, 0.10209736, 0.71268058], "xyz": [-2.44841056, -11.059362822911867, -1.3053169774063424], "label": "Nb", "properties": {"magmom": 0.033}}, {"species": [{"element": "Fe", "occu": 1}], "abc": [0.75053738, 0.61136775, 0.57156911], "xyz": [-3.675247293733466, -8.869597886136905, -7.81635003602166], "label": "Fe", "properties": {"magmom": 0.713}}, {"species": [{"element": "Fe", "occu": 1}], "abc": [0.74946262, 0.11136775, 0.42843089], "xyz": [-3.6699843862665342, -6.648381883863095, -1.4238391160216601], "label": "Fe", "properties": {"magmom": 0.713}}, {"species": [{"element": "Fe", "occu": 1}], "abc": [0.25053738, 0.11136775, 0.42843089], "xyz": [-1.2268367337334656, -6.648381883863095, -1.4238391160216601], "label": "Fe", "properties": {"magmom": 0.713}}, {"species": [{"element": "Fe", "occu": 1}], "abc": [0.24946262, 0.61136775, 0.57156911], "xyz": [-1.2215738262665345, -8.869597886136905, -7.81635003602166], "label": "Fe", "properties": {"magmom": 0.713}}, {"species": [{"element": "Fe", "occu": 1}], "abc": [0.74850271, 0.99123806, 0.8565342], "xyz": [-3.6652838787052353, -13.291680387913134, -12.673000245739232], "label": "Fe", "properties": {"magmom": 1.063}}, {"species": [{"element": "Fe", "occu": 1}], "abc": [0.75149729, 0.49123806, 0.1434658], "xyz": [-3.679947801294765, -2.226299382086866, -6.2804893257392305], "label": "Fe", "properties": {"magmom": 1.063}}, {"species": [{"element": "Fe", "occu": 1}], "abc": [0.24850271, 0.49123806, 0.1434658], "xyz": [-1.2168733187052352, -2.226299382086866, -6.2804893257392305], "label": "Fe", "properties": {"magmom": 1.063}}, {"species": [{"element": "Fe", "occu": 1}], "abc": [0.25149729, 0.99123806, 0.8565342], "xyz": [-1.2315372412947647, -13.291680387913134, -12.673000245739232], "label": "Fe", "properties": {"magmom": 1.063}}, {"species": [{"element": "Fe", "occu": 1}], "abc": [0.74735209, 0.91029293, 0.61139135], "xyz": [-3.659649498388141, -9.48755860085299, -11.638114990847592], "label": "Fe", "properties": {"magmom": 1.55}}, {"species": [{"element": "Fe", "occu": 1}], "abc": [0.75264791, 0.41029293, 0.38860865], "xyz": [-3.6855821816118595, -6.030421169147011, -5.245604070847591], "label": "Fe", "properties": {"magmom": 1.55}}, {"species": [{"element": "Fe", "occu": 1}], "abc": [0.24735209, 0.41029293, 0.38860865], "xyz": [-1.2112389383881408, -6.030421169147011, -5.245604070847591], "label": "Fe", "properties": {"magmom": 1.55}}, {"species": [{"element": "Fe", "occu": 1}], "abc": [0.25264791, 0.91029293, 0.61139135], "xyz": [-1.2371716216118591, -9.48755860085299, -11.638114990847592], "label": "Fe", "properties": {"magmom": 1.55}}, {"species": [{"element": "Fe", "occu": 1}], "abc": [0.75166938, 0.60817805, 0.83995675], "xyz": [-3.680790495241306, -13.034431854174947, -7.775569651858612], "label": "Fe", "properties": {"magmom": 1.528}}, {"species": [{"element": "Fe", "occu": 1}], "abc": [0.74833062, 0.10817805, 0.16004325], "xyz": [-3.664441184758694, -2.4835479158250524, -1.383058731858612], "label": "Fe", "properties": {"magmom": 1.528}}, {"species": [{"element": "Fe", "occu": 1}], "abc": [0.25166938, 0.10817805, 0.16004325], "xyz": [-1.2323799352413056, -2.4835479158250524, -1.383058731858612], "label": "Fe", "properties": {"magmom": 1.528}}, {"species": [{"element": "Fe", "occu": 1}], "abc": [0.24833062, 0.60817805, 0.83995675], "xyz": [-1.2160306247586945, -13.034431854174947, -7.775569651858612], "label": "Fe", "properties": {"magmom": 1.528}}, {"species": [{"element": "Fe", "occu": 1}], "abc": [0.0, 0.79440161, 0.19097721], "xyz": [0.0, -2.963580481311042, -10.156441933581164], "label": "Fe", "properties": {"magmom": 0.69}}, {"species": [{"element": "Fe", "occu": 1}], "abc": [0.5, 0.29440161, 0.80902279], "xyz": [-2.44841056, -12.554399288688959, -3.7639310135811623], "label": "Fe", "properties": {"magmom": 0.69}}, {"species": [{"element": "Fe", "occu": 1}], "abc": [0.76035911, 0.29748339, 0.9400256], "xyz": [-3.723342548632403, -14.587298244082113, -3.803331638187238], "label": "Fe", "properties": {"magmom": 1.539}}, {"species": [{"element": "Fe", "occu": 1}], "abc": [0.73964089, 0.79748339, 0.0599744], "xyz": [-3.621889131367597, -0.930681525917888, -10.195842558187238], "label": "Fe", "properties": {"magmom": 1.539}}, {"species": [{"element": "Fe", "occu": 1}], "abc": [0.26035911, 0.79748339, 0.0599744], "xyz": [-1.2749319886324033, -0.930681525917888, -10.195842558187238], "label": "Fe", "properties": {"magmom": 1.539}}, {"species": [{"element": "Fe", "occu": 1}], "abc": [0.23964089, 0.29748339, 0.9400256], "xyz": [-1.1734785713675968, -14.587298244082113, -3.803331638187238], "label": "Fe", "properties": {"magmom": 1.539}}, {"species": [{"element": "Fe", "occu": 1}], "abc": [0.0, 0.70069204, 0.95071104], "xyz": [0.0, -14.75311468583566, -8.958363034514154], "label": "Fe", "properties": {"magmom": 1.435}}, {"species": [{"element": "Fe", "occu": 1}], "abc": [0.5, 0.20069204, 0.04928896], "xyz": [-2.44841056, -0.7648650841643392, -2.5658521145141537], "label": "Fe", "properties": {"magmom": 1.435}}, {"species": [{"element": "Si", "occu": 1}], "abc": [0.74764183, 0.78530911, 0.31308635], "xyz": [-3.6610683033394498, -4.85846764556314, -10.040194122500964], "label": "Si", "properties": {"magmom": -0.007}}, {"species": [{"element": "Si", "occu": 1}], "abc": [0.75235817, 0.28530911, 0.68691365], "xyz": [-3.6841633766605506, -10.659512124436862, -3.6476832025009625], "label": "Si", "properties": {"magmom": -0.007}}, {"species": [{"element": "Si", "occu": 1}], "abc": [0.24764183, 0.28530911, 0.68691365], "xyz": [-1.2126577433394496, -10.659512124436862, -3.6476832025009625], "label": "Si", "properties": {"magmom": -0.007}}, {"species": [{"element": "Si", "occu": 1}], "abc": [0.25235817, 0.78530911, 0.31308635], "xyz": [-1.2357528166605505, -4.85846764556314, -10.040194122500964], "label": "Si", "properties": {"magmom": -0.007}}, {"species": [{"element": "Si", "occu": 1}], "abc": [0.0, 0.64146766, 0.10364917], "xyz": [0.0, -1.608425723237291, -8.201178042753694], "label": "Si", "properties": {"magmom": -0.022}}, {"species": [{"element": "Si", "occu": 1}], "abc": [0.5, 0.14146766, 0.89635083], "xyz": [-2.44841056, -13.90955404676271, -1.8086671227536943], "label": "Si", "properties": {"magmom": -0.022}}, {"species": [{"element": "Si", "occu": 1}], "abc": [0.0, 0.5557357, 0.45184833], "xyz": [0.0, -7.0117732440482845, -7.105093061767689], "label": "Si", "properties": {"magmom": -0.019}}, {"species": [{"element": "Si", "occu": 1}], "abc": [0.5, 0.0557357, 0.54815167], "xyz": [-2.44841056, -8.506206525951717, -0.712582141767688], "label": "Si", "properties": {"magmom": -0.019}}, {"species": [{"element": "Si", "occu": 1}], "abc": [0.0, 0.57889046, 0.7045276], "xyz": [0.0, -10.932845044206653, -7.401127174067646], "label": "Si", "properties": {"magmom": -0.009}}, {"species": [{"element": "Si", "occu": 1}], "abc": [0.5, 0.07889046, 0.2954724], "xyz": [-2.44841056, -4.585134725793348, -1.0086162540676464], "label": "Si", "properties": {"magmom": -0.009}}, {"species": [{"element": "Si", "occu": 1}], "abc": [0.0, 0.89184192, 0.95303339], "xyz": [0.0, -14.78915286615452, -11.402218425027533], "label": "Si", "properties": {"magmom": -0.021}}, {"species": [{"element": "Si", "occu": 1}], "abc": [0.5, 0.39184192, 0.04696661], "xyz": [-2.44841056, -0.7288269038454797, -5.009707505027533], "label": "Si", "properties": {"magmom": -0.021}}, {"species": [{"element": "Si", "occu": 1}], "abc": [0.0, 0.97365256, 0.48471181], "xyz": [0.0, -7.521748061860084, -12.448169244171911], "label": "Si", "properties": {"magmom": -0.021}}, {"species": [{"element": "Si", "occu": 1}], "abc": [0.5, 0.47365256, 0.51528819], "xyz": [-2.44841056, -7.996231708139917, -6.055658324171911], "label": "Si", "properties": {"magmom": -0.021}}, {"species": [{"element": "Si", "occu": 1}], "abc": [0.0, 0.39983905, 0.24978334], "xyz": [0.0, -3.8761328170030316, -5.111950986734852], "label": "Si", "properties": {"magmom": -0.025}}, {"species": [{"element": "Si", "occu": 1}], "abc": [0.5, 0.89983905, 0.75021666], "xyz": [-2.44841056, -11.641846952996968, -11.504461906734852], "label": "Si", "properties": {"magmom": -0.025}}, {"species": [{"element": "Si", "occu": 1}], "abc": [0.0, 0.26618948, 0.45840468], "xyz": [0.0, -7.113514550713324, -3.403238315378243], "label": "Si", "properties": {"magmom": -0.022}}, {"species": [{"element": "Si", "occu": 1}], "abc": [0.5, 0.76618948, 0.54159532], "xyz": [-2.44841056, -8.404465219286676, -9.795749235378244], "label": "Si", "properties": {"magmom": -0.022}}, {"species": [{"element": "Si", "occu": 1}], "abc": [0.0, 0.95570093, 0.11855176], "xyz": [0.0, -1.8396838133778952, -12.218657262558311], "label": "Si", "properties": {"magmom": -0.021}}, {"species": [{"element": "Si", "occu": 1}], "abc": [0.5, 0.45570093, 0.88144824], "xyz": [-2.44841056, -13.678295956622105, -5.826146342558312], "label": "Si", "properties": {"magmom": -0.021}}, {"species": [{"element": "Si", "occu": 1}], "abc": [0.0, 0.75095771, 0.62925705], "xyz": [0.0, -9.764798172029879, -9.601010723266388], "label": "Si", "properties": {"magmom": -0.02}}, {"species": [{"element": "Si", "occu": 1}], "abc": [0.5, 0.25095771, 0.37074295], "xyz": [-2.44841056, -5.753181597970122, -3.2084998032663865], "label": "Si", "properties": {"magmom": -0.02}}, {"species": [{"element": "Si", "occu": 1}], "abc": [0.0, 0.99883217, 0.72483758], "xyz": [0.0, -11.248014902975756, -12.770091107944594], "label": "Si", "properties": {"magmom": -0.022}}, {"species": [{"element": "Si", "occu": 1}], "abc": [0.5, 0.49883217, 0.27516242], "xyz": [-2.44841056, -4.269964867024243, -6.377580187944593], "label": "Si", "properties": {"magmom": -0.022}}], "@version": null}']

testStructures = [Structure.from_str(matStr,fmt='json') for matStr in matStrList]
[s.make_supercell([2,2,2]) for s in testStructures]
baseStructures = [s.copy() for s in testStructures]
[s.replace(0, 'Al') for s in testStructures]
testStructures = [s.copy() for s in testStructures]

testReferenceData = [KS2022.generate_descriptor(s).tolist() for s in tqdm(testStructures)]

functionOutput_assumePure = [KS2022_dilute.generate_descriptor(s, baseStruct='pure').tolist()
                             for s in tqdm(testStructures[:3])]
functionOutput_explicitBase = [KS2022_dilute.generate_descriptor(s, baseStruct=bs).tolist()
                             for s, bs in tqdm(zip(testStructures, baseStructures))]

with resources.files('pysipfenn').joinpath('tests/KS2022_dilute_TestResult.csv').open('w+', newline='') as f:
    f.writelines([f'{name},{trd},{fo1},{fo2}\n' for fo2, fo1, trd, name in zip(functionOutput_explicitBase[0], functionOutput_assumePure[0], testReferenceData[0], labels)])

class TestKS2022(unittest.TestCase):
    def test_resutls_assumePure(self):
        for fo, trd, name in zip(functionOutput_assumePure, testReferenceData, testMaterialsLabels):
            for p_fo, p_trd, l in zip(fo, trd, labels):
                if p_trd>0.01 and p_fo>0.01:
                    p_fo_relative = p_fo/p_trd
                    with self.subTest(msg=f'{name:<16} diff in {l}'):
                        self.assertAlmostEqual(p_fo_relative, 1, places=2)
                else:
                    with self.subTest(msg=f'{name:<16} diff in {l}'):
                        self.assertAlmostEqual(p_fo, p_trd, places=6)

    def test_resutls_explicitBase(self):
        for fo, trd, name in zip(functionOutput_explicitBase, testReferenceData, testMaterialsLabels):
            for p_fo, p_trd, l in zip(fo, trd, labels):
                if p_trd>0.01 and p_fo>0.01:
                    p_fo_relative = p_fo/p_trd
                    with self.subTest(msg=f'{name:<16} diff in {l}'):
                        self.assertAlmostEqual(p_fo_relative, 1, places=2)
                else:
                    with self.subTest(msg=f'{name:<16} diff in {l}'):
                        self.assertAlmostEqual(p_fo, p_trd, places=6)


if __name__ == '__main__':
    unittest.main()