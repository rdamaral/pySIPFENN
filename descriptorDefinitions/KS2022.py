# Authors: Jonathan Siegel, Adam M. Krajewski
#
# Calculates the descriptor first introduced by Ward and Wolverton.
#
# Please Cite:
# L. Ward, R. Liu, A. Krishna, V. I. Hegde, A. Agrawal, A. Choudhary, and C. Wolverton,
# “Including crystal structure attributes in machine learning models of formation energies
# via Voronoi tessellations,” Physical Review B, vol. 96, no. 2, 7 2017.

import math
import time
import numpy as np
import os
from pymatgen.core import Structure, Element
from pymatgen.analysis.local_env import VoronoiNN
from pymatgen.symmetry.analyzer import SpacegroupAnalyzer
import json
from tqdm import tqdm
from collections import Counter

citation = 'L. Ward, R. Liu, A. Krishna, V. I. Hegde, A. Agrawal, A. Choudhary, and C. Wolverton, “Including crystal structure attributes in machine learning models of formation energies via Voronoi tessellations,” Physical Review B, vol. 96, no. 2, 7 2017.'

periodic_table_size = 112
attribute_matrix = np.loadtxt(os.path.join(os.path.dirname(__file__), 'Magpie_element_properties.csv'), delimiter=',')
attribute_matrix = np.nan_to_num(attribute_matrix)
# Only select attributes actually used in Magpie.
attribute_matrix = attribute_matrix[:,
                   [45, 33, 2, 32, 5, 48, 6, 10, 44, 42, 38, 40, 36, 43, 41, 37, 39, 35, 18, 13, 17]]


# A prototype function which computes a weighted average over neighbors,
# weighted by the area of the voronoi cell between them.
def local_env_function(local_env, site):
    local_attributes = np.zeros(attribute_matrix.shape[1])
    for key, value in site.species.get_el_amt_dict().items():
        local_attributes += value * attribute_matrix[Element(key).Z - 1, :]
    diff_attributes = np.zeros(attribute_matrix.shape[1])
    total_weight = 0
    volume = 0
    neighbor_list = [[value['site'], value['area']] for value in local_env.values()]
    for ind, neighbor_site in local_env.items():
        neighbor_attributes = np.zeros(attribute_matrix.shape[1])
        for key, value in neighbor_site['site'].species.get_el_amt_dict().items():
            neighbor_attributes += value * attribute_matrix[Element(key).Z - 1, :]
        diff_attributes += np.abs(local_attributes - neighbor_attributes) * neighbor_site['area']
        total_weight += neighbor_site['area']
        volume += neighbor_site['volume']
    elemental_properties_attributes = [diff_attributes / total_weight, local_attributes]
    # Calculate coordination number attribute
    average = 0
    variance = 0
    for neighbor_site in local_env.values():
        average += neighbor_site['area']
        variance += neighbor_site['area'] * neighbor_site['area']
    eff_coord_num = average * average / variance
    # Calculate Bond Length Attributes
    blen_average = 0
    for neighbor_site in local_env.values():
        blen_average += neighbor_site['area'] * 2 * neighbor_site['face_dist']
    blen_average /= total_weight
    blen_var = 0
    for neighbor_site in local_env.values():
        blen_var += neighbor_site['area'] * abs(2 * neighbor_site['face_dist'] - blen_average)
    blen_var /= total_weight * blen_average
    # Calculate Packing Efficiency info
    sphere_rad = min(neighbor_site['face_dist'] for neighbor_site in local_env.values())
    sphere_volume = (4.0 / 3.0) * math.pi * math.pow(sphere_rad, 3.0)
    return [np.concatenate(
        ([eff_coord_num, blen_average, blen_var, volume, sphere_volume], elemental_properties_attributes[0])),
            elemental_properties_attributes[1], neighbor_list]


# A wrapper class which contains an instance of an NN generator (the default is a VoronoiNN), a structure, and
# a function which computes the local environment attributes.
class LocalAttributeGenerator:
    def __init__(self, struct, local_env_func, nn_generator=VoronoiNN(compute_adj_neighbors=False, extra_nn_info=False)):
        self.generator = nn_generator
        self.struct = struct
        self.function = local_env_func

    def generate_local_attributes(self, n):
        local_env = self.generator.get_voronoi_polyhedra(self.struct, n)
        return self.function(local_env, self.struct[n])


def generate_voronoi_attributes(struct, local_funct=local_env_function):
    local_generator = LocalAttributeGenerator(struct, local_funct)
    attribute_list = list()
    equivalentSitesMultiplicities = get_equivalentSitesMultiplicities(struct)
    for siteN in equivalentSitesMultiplicities:
        localAttributes = [local_generator.generate_local_attributes(siteN)]
        attribute_list += localAttributes*equivalentSitesMultiplicities[siteN]
    return np.array([value[0] for value in attribute_list]), np.array([value[1] for value in attribute_list])

# Calculates the attributes corresponding to the most common elements.
def magpie_mode(attribute_properties, axis=0):
    scores = np.unique(np.ravel(attribute_properties[:, 0]))  # get all unique atomic numbers
    max_occurrence = 0
    top_elements = []
    for score in scores:
        template = (attribute_properties[:, 0] == score)
        count = np.expand_dims(np.sum(template, axis), axis)[0]
        if count > max_occurrence:
            top_elements.clear()
            top_elements.append(score)
            max_occurrence = count
        elif count == max_occurrence:
            top_elements.append(score)
    output = np.zeros_like(attribute_properties[0, :])
    for elem in top_elements:
        output += attribute_matrix[int(elem) - 1, :]
    return output / len(top_elements)

def get_equivalentSitesMultiplicities(struct: Structure):
    spgA = SpacegroupAnalyzer(s, angle_tolerance=1, symprec=0.1)
    return dict(Counter(list(spgA.get_symmetry_dataset()['equivalent_atoms'])))


def generate_descriptor(struct: Structure, include_WC=True):
    diff_properties, attribute_properties = generate_voronoi_attributes(struct)
    properties = np.concatenate(
        (np.stack(
            (np.mean(diff_properties, axis=0),
             np.mean(np.abs(diff_properties - np.mean(diff_properties, axis=0)), axis=0),
             np.min(diff_properties, axis=0),
             np.max(diff_properties, axis=0),
             np.max(diff_properties, axis=0) - np.min(diff_properties, axis=0)), axis=-1).reshape((-1)),
        np.stack(
            (np.mean(attribute_properties, axis=0),
             np.max(attribute_properties, axis=0) - np.min(attribute_properties, axis=0),
             np.mean(np.abs(attribute_properties - np.mean(attribute_properties, axis=0)), axis=0),
             np.max(attribute_properties, axis=0),
             np.min(attribute_properties, axis=0),
             magpie_mode(attribute_properties)), axis=-1).reshape((-1))))
    # Normalize Bond Length properties.
    properties[6] /= properties[5]
    properties[7] /= properties[5]
    properties[8] /= properties[5]
    # Normalize the Cell Volume Deviation.
    properties[16] /= properties[15]
    # Remove properties not in magpie.
    properties = np.delete(properties, [4, 5, 9, 14, 15, 17, 18, 19, 21, 22, 23, 24])
    # Renormalize the packing efficiency.
    properties[12] *= len(attribute_properties) / struct.volume
    # Calculate and insert stoichiometry attributes.
    element_dict = {}
    for composition in struct.species_and_occu:
        for key, value in composition.get_el_amt_dict().items():
            if key in element_dict:
                element_dict[key] += value / len(struct.species_and_occu)
            else:
                element_dict[key] = value / len(struct.species_and_occu)
    position = 121
    for p in [10, 7, 5, 3, 2]:
        properties = np.insert(properties, position,
                               math.pow(sum(math.pow(value, p) for value in element_dict.values()), 1.0 / p))
    properties = np.insert(properties, position, len(element_dict))
    # Calculate Valence Electron Statistics
    electron_occupation_dict = {'s': 0, 'p': 0, 'd': 0, 'f': 0}
    total_valence_factor = 0
    for key, value in element_dict.items():
        electron_occupation_dict['s'] += value * attribute_matrix[Element(key).Z - 1][8]
        electron_occupation_dict['p'] += value * attribute_matrix[Element(key).Z - 1][9]
        electron_occupation_dict['d'] += value * attribute_matrix[Element(key).Z - 1][10]
        electron_occupation_dict['f'] += value * attribute_matrix[Element(key).Z - 1][11]
    total_valence_factor = sum([val for (key, val) in electron_occupation_dict.items()])
    for orb in ['s', 'p', 'd', 'f']:
        properties = np.append(properties, electron_occupation_dict[orb] / total_valence_factor)
    # Calculate ionic compound attributes.
    max_ionic_char = 0
    av_ionic_char = 0
    has_anions = False
    has_cations = True
    for el in struct.composition.add_charges_from_oxi_state_guesses().elements:
        if el.oxi_state > 0:
            has_anions = True
        if el.oxi_state < 0:
            has_cations = True
    for key1, value1 in element_dict.items():
        for key2, value2 in element_dict.items():
            ionic_char = 1.0 - math.exp(-0.25 * (Element(key1).X - Element(key2).X) ** 2)
            if ionic_char > max_ionic_char:
                max_ionic_char = ionic_char
            av_ionic_char += ionic_char * value1 * value2
    properties = np.append(properties, (float)(has_anions and has_cations))
    properties = np.append(properties, max_ionic_char)
    properties = np.append(properties, av_ionic_char)
    return properties

def cite():
    return citation

if __name__ == "__main__":
    print('Profiling/testing task. Will calculate a descriptor for Li2 Zr1 Te1 O6 (JVASP-10001)')
    matStr = '{"@module": "pymatgen.core.structure", "@class": "Structure", "charge": null, "lattice": {"matrix": [[4.599305652662459, 0.0098015076998823, 3.1052612865443736], [1.6553257726204653, 4.291108475854712, 3.1052602938979565], [0.0142541214919749, 0.0098025099996131, 5.549419141866351]], "a": 5.549446478152326, "b": 5.549446536179343, "c": 5.549446105810423, "alpha": 55.82714459985832, "beta": 55.82714014289371, "gamma": 55.82713972779092, "volume": 109.15484625642743}, "sites": [{"species": [{"element": "Li", "occu": 1.0}], "abc": [0.2738784872669924, 0.2738784872670407, 0.2738784872673032], "xyz": [1.7169128904007063, 1.1806114167777613, 3.220794775377278], "label": "Li", "properties": {}}, {"species": [{"element": "Li", "occu": 1.0}], "abc": [0.7852272010728069, 0.7852272010728856, 0.785227201073315], "xyz": [4.922499451739965, 3.3848887059434927, 9.234225338163633], "label": "Li", "properties": {}}, {"species": [{"element": "O", "occu": 1.0}], "abc": [0.8669964454661124, 0.604089882092114, 0.241821769873143], "xyz": [4.990994160164061, 2.603083545876856, 5.910077181137658], "label": "O", "properties": {}}, {"species": [{"element": "O", "occu": 1.0}], "abc": [0.717840894529788, 0.1213675889628683, 0.393537009186973], "xyz": [3.508082106234713, 0.531695063215412, 4.789863306469278], "label": "O", "properties": {}}, {"species": [{"element": "O", "occu": 1.0}], "abc": [0.1213675889638402, 0.3935370091873943, 0.7178408945283384], "xyz": [1.2198707830817896, 1.6969362235910317, 5.58251292516964], "label": "O", "properties": {}}, {"species": [{"element": "O", "occu": 1.0}], "abc": [0.3935370091861915, 0.7178408945293856, 0.1213675889634014], "xyz": [2.999987512595622, 3.085380109860344, 4.124637687962297], "label": "O", "properties": {}}, {"species": [{"element": "O", "occu": 1.0}], "abc": [0.2418217698721573, 0.8669964454671221, 0.6040898820921513], "xyz": [2.555984564633329, 3.728667610729149, 6.795517372377343], "label": "O", "properties": {}}, {"species": [{"element": "O", "occu": 1.0}], "abc": [0.6040898820933115, 0.2418217698723637, 0.8669964454664059], "xyz": [3.191046090145173, 1.0521031793025595, 7.4381031350436535], "label": "O", "properties": {}}, {"species": [{"element": "Te", "occu": 1.0}], "abc": [0.4965905610507353, 0.4965905610507355, 0.4965905610507361], "xyz": [3.113069390835793, 2.1406591357024984, 5.8398755612146624], "label": "Te", "properties": {}}, {"species": [{"element": "Zr", "occu": 1.0}], "abc": [0.0006501604980668, 0.0006501604980928, 0.0006501604982344], "xyz": [0.00407578174946036, 0.002802654981945192, 0.007645848918263076], "label": "Zr", "properties": {}}]}'
    s10 = [Structure.from_dict(json.loads(matStr))]*10
    for s in tqdm(s10):
        d = generate_descriptor(SpacegroupAnalyzer(s).get_symmetrized_structure())
    with open('KS2022_TestResult.csv', 'w+') as f:
        f.writelines([f'{v}\n' for v in d])
    print('Done!')
    print(d)