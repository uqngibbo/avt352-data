import os
import glob
import copy


import numpy as np
import matplotlib.pyplot as plt


INCH_TO_M = 2.54e-2
PSIA_TO_PASCAL = 6894.76
BTU_FT2_SEC_TO_W_M2 = 11356.538527
mm_to_m = 1e-3

length_dict = {'geom1': {'total':2852.2676 * mm_to_m,
                        'cone':2642.2604 * mm_to_m,
                        'flare': 210.0072 * mm_to_m,
                        'angle_cone': 6,
                        'angle_flare': 42  
                    },
                'geom2': {'total': 2504.186 * mm_to_m,
                        'cone': 2353.056 * mm_to_m,
                        'flare': 151.130 * mm_to_m,
                        'angle_cone': 7,
                        'angle_flare': 40  
                   } 
            }


exp_sep_onset_dict = {
                    'run4': 2.5743,
                    'run6': 2.5606,
                    'run45': 2.3464,
                    'run28': 2.3268,
                    'run34': 2.3271,
                    'run33':2.2996,
                    'run14': 2.2993,
                    'run41': 2.35, #2.3465 # or 2.3561 as looks not separated, so end of cone as location?
                    'run37': 2.3153
                }

cfd_sep_onset_bounds_dict = {
                    'run4': (2.441,2.628),
                    'run6': (2.51,2.539),
                    'run45': (2.284,2.35),
                    'run28': (2.277,2.354),
                    'run34': (2.293,2.349),
                    'run33': (2.242,2.309),
                    'run14': (2.278,2.353),
                    'run41': (2.305,2.349),
                    'run37': (2.27,2.349)
}

cfd_sep_onset_vals_dict = { 
                'geom1': {
                    'run4': [2.571,
 2.531,
 2.638,
 2.636,
 2.509,
 2.489,
 2.639,
 2.415,
 2.639,
 2.549,
 2.472,
 2.457,
 2.441,
 2.519,
 2.614,
 2.563],

                    'run6': [2.539, 2.51, 2.623, 2.565],
                }, 
                'geom2':{

                    'run45': [2.343,
 2.312,
 2.303,
 2.336,
 2.333,
 2.289,
 2.31,
 2.35,
 2.35,
 2.312,
 2.293,
 2.303,
 2.348,
 2.35,
 2.35,
 2.348,
 2.333,
 2.35,
 2.349,
 2.325,
 2.297,
 2.29,
 2.284,
 2.303,
 2.235],


                    'run28': [2.291, 2.292, 2.312, 2.277, 2.284, 2.318, 2.35],
                    'run34': [2.295, 2.293, 2.316, 2.352],
                    'run33': [2.259, 2.242, 2.251, 2.297, 2.347],
                    'run14': [2.278, 2.265, 2.279, 2.308, 2.35],
                    'run41': [2.305, 2.307, 2.345],
                    'run37': [2.284, 2.27, 2.288]
}
}


cfd_peak_pressure_locs_vals_dict = { 
                'geom1': {
                    'run4': [2.695,
 2.707,
 2.676,
 2.677,
 2.719,
 2.729,
 2.685,
 2.753,
 2.678,
 2.701,
 2.737,
 2.745,
 2.753,
 2.713,
 2.672,
 2.705],

                    'run6': [2.7, 2.713, 2.687, 2.701]
                }, 
                'geom2':{

                    'run45': [2.401,
 2.401,
 2.407,
 2.388,
 2.391,
 2.418,
 2.402,
 2.387,
 2.387,
 2.405,
 2.417,
 2.414,
 2.39,
 2.389,
 2.389,
 2.384,
 2.389,
 2.393,
 2.386,
 2.39,
 2.415,
 2.421,
 2.426,
 2.407,
 2.476],



                    'run28': [2.42, 2.427, 2.404, 2.438, 2.432, 2.402, 2.39], 
                    'run34':[2.408, 2.415, 2.406, 2.394], 
                    'run33': [2.426, 2.448, 2.445, 2.409, 2.392],
                    'run14': [2.41, 2.425, 2.422, 2.399, 2.394],
                    'run41':[2.394, 2.395, 2.409], 
                    'run37':  [2.403, 2.417, 2.415],
            }
}

cfd_peak_pressure_vals_dict = { 
                'geom1': {
                    'run4': [150.38,
 161.82,
 103.67,
 103.77,
 162.8,
 163.05,
 93.62,
 175.32,
 103.87,
 145.22,
 173.18,
 171.13,
 169.78,
 161.78,
 109.1,
 127.7],


                    'run6':  [220.09, 225.57, 138.09, 168.94]
                }, 
                'geom2':{

                    'run45': [274.17,
 284.88,
 287.65,
 262.44,
 254.48,
 293.22,
 278.06,
 251.57,
 251.7,
 268.66,
 278.02,
 263.58,
 246.17,
 245.12,
 244.98,
 250.89,
 255.86,
 243.66,
 246.71,
 259.35,
 294.16,
 294.6,
 292.94,
 287.37,
 323.71],



                    'run28':[221.89, 218.48, 204.51, 215.95, 216.6, 196.27, 189.39], 
                    'run34':[140.78, 140.49, 128.4, 113.8], 
                    'run33':[55.18, 54.7, 51.57, 50.76, 41.61], 
                    'run14':[75.24, 76.77, 70.17, 66.97, 54.72], 
                    'run41': [93.56, 95.24, 84.78],
                    'run37': [75.1, 77.98, 68.34], 
        }
}



cfd_peak_heatflux_locs_vals_dict = { 
                'geom1': {
                    'run4': [2.694,
 2.706,
 2.695,
 2.708,
 2.718,
 2.729,
 2.678,
 2.742,
 2.698,
 2.681,
 2.737,
 2.744,
 2.753,
 2.713,
 2.671,
 2.7],


                    'run6':  [2.7, 2.713, 2.665, 2.697]
                }, 
                'geom2':{

                    'run45': [2.391,
 2.401,
 2.407,
 2.387,
 2.389,
 2.416,
 2.398,
 2.483,
 2.483,
 2.409,
 2.415,
 2.422,
 2.386,
 2.389,
 2.388,
 2.43,
 2.387,
 2.388,
 2.423,
 2.406,
 2.414,
 2.421,
 2.425,
 2.407,
 2.475],

                    'run28':[2.379, 2.427, 2.405, 2.436, 2.431, 2.399, 2.359], 
                    'run34':[2.375, 2.414, 2.394, 2.386], 
                    'run33': [2.383, 2.445, 2.443, 2.407, 2.378],
                    'run14':[2.377, 2.425, 2.42, 2.398, 2.383], 
                    'run41': [2.371, 2.394, 2.393],
                    'run37': [2.403, 2.416, 2.407],
    }
}


cfd_peak_heatflux_vals_dict = { 
                'geom1': {
                    'run4': [3.722,
 4.185,
 1.41,
 1.392,
 3.836,
 3.809,
 1.743,
 2.534,
 1.42,
 2.44,
 4.072,
 3.869,
 3.679,
 3.631,
 3.364,
 3.888],


                    'run6':  [6.642, 6.33, 4.011, 5.858]
                }, 
                'geom2':{

                    'run45': [4.368,
 5.546,
 5.23,
 5.619,
 5.846,
 5.573,
 6.273,
 2.872,
 2.907,
 5.176,
 5.054,
 4.689,
 3.735,
 3.9,
 3.805,
 2.944,
 4.712,
 3.795,
 3.073,
 3.928,
 5.568,
 5.386,
 5.243,
 5.002,
 4.896],
                    'run28': [3.314, 2.515, 2.396, 2.449, 2.425, 2.377, 1.925], 
                    'run34': [3.235, 2.248, 1.986, 1.529],
                    'run33': [0.244, 0.174, 0.189, 0.183, 0.134], 
                    'run14': [0.73, 0.651, 0.604, 0.592, 0.401], 
                    'run41':[4.992, 3.506, 2.005], 
                    'run37': [0.914, 0.9, 0.753],
    }
}



def get_experimental_separation():
    return exp_sep_onset_dict

def get_geometry_information():
    return length_dict

def get_cfd_separation_bounds():
    return cfd_sep_onset_bounds_dict

def get_cfd_separation_values():
    return cfd_sep_onset_vals_dict

def get_cfd_peak_vals_and_locs_values(param, param_type):
    assert param in ['heatflux', 'pressure']
    assert param_type in ['peak', 'location']

    if param == 'heatflux':
        if param_type == 'peak':
            return cfd_peak_heatflux_vals_dict
        return cfd_peak_heatflux_locs_vals_dict

    if param_type == 'peak':
        return cfd_peak_pressure_vals_dict

    return cfd_peak_pressure_locs_vals_dict



# import re
# # List of filenames
# filenames = [
#     "run4_wallHeatFlux_meshXX-SST.dat",
#     "run4_wallP_meshXX-SST.dat",
#     "RUN4_SU2_gridConv_coarse_pressure.dat",
#     "RUN4_SU2_gridConv_medium_heatFlux.dat",
#     "RUN4_SU2_schemeOrder_1st_heatFlux.dat"
# ]

# # Regex pattern
# # Regex pattern
# pattern = re.compile(r'^run\d+_[A-Za-z]+_mesh[A-Za-z0-9]+-[A-Za-z]+\.dat$', re.IGNORECASE)
# # Filter filenames
# matching_files = [filename for filename in filenames if pattern.match(filename)]



def filter_files_with_keyword(file_list):
    file_list = [filename for filename in file_list if filename.endswith('.dat')]
    return [tmp for tmp in file_list if ('wallHeatFlux' in tmp) or ('wallP' in tmp)]


def create_cfddatadict_for_solver(solvername, cfdfilenames):

    assert solvername in ['starccm', 'h3amr', 'ansys_inc','ansys_aselsan',
                            'eilmer', 'tau', 'cadence', 'gaspex', 'coda',
                            'SU2', 'tau2', 'overflow', 'vulcan']

    if solvername == 'SU2':
        cfdfilenames = filter_files_with_keyword(cfdfilenames)
        print(cfdfilenames)

    keys, turb_model_list = evaluate_dictionary_key_from_filename(cfdfilenames)
    if solvername == 'starccm':
        cfd_data_dict = load_data_files_ccm(cfdfilenames,
                                        keys,
                                        turb_model_list,
                                        dtype = 'float'
                                    )

    if solvername == 'h3amr':
        
        # cfd_data_dict = load_data_files_h3amr(cfdfilenames,
        #                                 keys,
        #                                 turb_model_list,
        #                                 dtype = 'float'
        #                             )
        cfd_data_dict = load_data_files_ccm(cfdfilenames,
                                        keys,
                                        turb_model_list,
                                        dtype = 'float',
                                        solver = solvername
                                    )

    if solvername in ['ansys_inc','ansys_aselsan']:
        cfd_data_dict = load_data_files_ccm(cfdfilenames,
                                        keys,
                                        turb_model_list,
                                        dtype = 'float',
                                        solver = solvername
                                    )

    if solvername == 'SU2':

        cfd_data_dict = load_data_files_ccm(cfdfilenames,
                                        keys,
                                        turb_model_list,
                                        dtype = 'float',
                                        solver = solvername
                                    )

    if solvername == 'eilmer':
        cfd_data_dict = load_data_files_eilmer(cfdfilenames,
                                        keys,
                                        turb_model_list,
                                        dtype = 'float'
                                    )

    if solvername in ['tau2','tau', 'coda', 'overflow']:
        cfd_data_dict = load_data_files_ccm(cfdfilenames,
                                        keys,
                                        turb_model_list,
                                        dtype = 'float',
                                        solver = solvername
                                    )

    if solvername == 'gaspex':
        cfd_data_dict = load_data_files_ccm(cfdfilenames,
                                        keys,
                                        turb_model_list,
                                        dtype = 'float',
                                        solver = 'gaspex'
                                    )

    if solvername == 'cadence':
        cfd_data_dict = load_data_files_ccm(cfdfilenames,
                                        keys,
                                        turb_model_list,
                                        dtype = 'float',
                                        solver = 'cadence'
                                    )


    if solvername == 'vulcan':
        cfd_data_dict = load_data_files_ccm(cfdfilenames,
                                        keys,
                                        turb_model_list,
                                        dtype = 'float',
                                        solver = 'vulcan'
                                    )



    return cfd_data_dict




def read_cadence_file(filename):
    tmp_data = np.unique(np.genfromtxt(filename,
                                        delimiter=' ',
                                        skip_header=1),
                        axis = 0)
    tmp_data = np.array([(val1, val2) for val1, val2
                                        in zip(tmp_data[:,2], tmp_data[:,3])])
    tmp_data = np.unique(tmp_data, axis = 0) # somehow need to do again in case
    return tmp_data


def number(thing):
    try:
        outnumber = int(thing)
    except(ValueError):
        try:
            outnumber = float(thing)
        except(ValueError):
            outnumber = complex(thing.replace('i','j')).real
    return outnumber

def read_loads_file_eilmer(filename):
    header = None
    body = []
    with open(filename) as fp:
        for line in fp:
            line = line.strip().split()
            if line[0].startswith('#'):
                header = line[1:]
            else:
                body.append(list(map(number,line)))
            
    assert header!=None
    header = [i.split(':')[-1] if ':' in i else i for i in header]
    cols = [np.array(col) for col in zip(*body)]
    data = dict(zip(header,cols))
    return data


def filter_cfd_data_filenames(file_list , ext_remove = ['.tar.gz', '.gz']):
    filenames = [filename for filename in file_list 
                                 for extension in ext_remove
                                    if not filename.endswith(extension)]
    filenames = list(set(filenames))
    return filenames

def load_data_files_eilmer(tgt_files, dict_keys, turb_models, dtype = 'float', skiprows=1):
    result = dict()
    match_dict = {'p': 'wallP', 'q_total': 'wallHeatFlux'}

    for (_, key2), key3, filename in zip(dict_keys, turb_models, tgt_files):
        tmp_data = read_loads_file_eilmer(filename)

        for _, val in enumerate(match_dict):
            result.setdefault(match_dict[val], {}).update({key2: {}})
            result[match_dict[val]][key2][key3] = np.array([(val1, val2) 
                            for val1, val2 in zip(tmp_data['pos.x'], tmp_data[val])])

    return result


def load_data_files_h3amr(tgt_files, dict_keys, turb_models, dtype = 'float', skiprows=1):
    result = dict()
    match_dict = {'p': 'wallP', 'q_wall': 'wallHeatFlux'}

    for (_, key2), key3, filename in zip(dict_keys, turb_models, tgt_files):
        tmp_data = np.loadtxt(filename,
                        skiprows=skiprows,
                        delimiter = ",",
                        dtype = dtype)
        header =  [val.strip().split(' ')[0] for val in np.loadtxt(filename,
                        max_rows=1,
                        delimiter = ",",
                        dtype = 'str')]

        for ind, val in enumerate(header[2:]):
            result.setdefault(match_dict[val], {}).update({key2: {}})
            result[match_dict[val]][key2][key3] = np.array([(val1, val2) 
                            for val1, val2 in zip(tmp_data[:,0], tmp_data[:,ind+2])])

    return result




def load_data_files_ccm(tgt_files, dict_keys, turb_models, dtype = 'float', skiprows=1,
                        solver = None, verbosity = 0):
    """ load a set of data files and add them in a dictionary format
        TODO: handle cadence files, should be just a filter
    """

    delim = ","
    multiplier = [1,1]
    if solver == 'ansys_aselsan':
        multiplier = [1e-3, 1]


    # if solver == 'su2':
    #     skiprows = 0
    #     delim = " "
    # if solver == 'gaspex':
    #     # need to scale x-axis in inches
    #     multiplier = [INCH_TO_M, 1]


    result = dict()
    for (key1, key2), key3, filename in zip(dict_keys, turb_models, tgt_files):

        if verbosity > 1:
            print("Reading filename", filename)
            print("Turb model", key3)
            print("Quantity of interest", key1)
            print("Mesh name", key2)

        if solver == 'gaspex':
            if 'wallP' in filename:
                multiplier = [INCH_TO_M, PSIA_TO_PASCAL]
            if 'wallHeatFlux' in filename:
                multiplier = [INCH_TO_M, BTU_FT2_SEC_TO_W_M2]

        if solver =='vulcan':
            if 'wallP' in filename:
                multiplier = [1, 1e3]
            if 'wallHeatFlux' in filename:
                multiplier = [1, 1e6]

        try:
            try:
                result[key1][key2]
            except KeyError:
                result.setdefault(key1, {}).update({key2: {}})
            if verbosity > 1:
                print(result[key1][key2].keys())

            if solver == 'cadence':
                result[key1][key2][key3] = read_cadence_file(filename)

            if solver == 'SU2':
                print("Reading data for solver ", solver)
                print(filename)
                result[key1][key2][key3] = np.loadtxt(filename)
            elif solver != 'cadence':
                result[key1][key2][key3] =  np.unique(np.loadtxt(
                                            filename,
                                            skiprows=skiprows,
                                            delimiter = delim,
                                            dtype = dtype
                                        ), axis = 0) * multiplier


            if verbosity > 1:
                print(result[key1][key2].keys())
                print()
        except ValueError as excep:
            if "'null'" in str(excep):
                try:
                    result[key1][key2]
                except KeyError:
                    result.setdefault(key1, {}).update({key2: {}})

                result[key1][key2][key3] =  read_ccm_file(filename)
            else:   raise ValueError(excep)

    # data = [(dict_key, np.loadtxt(filename, skiprows=skiprows,delimiter = ",", dtype = dtype))
    #                 for dict_key, filename in zip(dict_keys,tgt_files)]

    return result



def obtain_variations(data_dict, keys_of_interest = ['separation_loc','peak_p', 'peak_p_loc',
                                        'peak_q', 'peak_q_loc'], turb_model_list = None):
    variations_dict = {}

    for key in keys_of_interest:
        if turb_model_list is None:
            tmp = np.array([turb_data[key] for solver_data in data_dict.values()
                        for turb_data in solver_data.values()])
        else:
            tmp = np.array([turb_data[key] for solver_data in data_dict.values()
                        for turb_mod, turb_data in solver_data.items() 
                                if turb_mod in turb_model_list])

        variations_dict[key] = dict([('min', np.min(tmp)),
                                    ('max', np.max(tmp)),
                                    ('variation', np.max(tmp) - np.min(tmp)),
                                    ('nb_results', len(tmp))                                
                                ])
    return variations_dict



def evaluate_dictionary_key_from_filename(tgt_files):
    dict_keys = [filename.split('.')[0] 
                        if not "/" in filename
                        else filename.split('/')[-1].split('.')[0]
                            for filename in tgt_files
                    ]


    turb_model_list = [model.split("-")[-1] for model in dict_keys] 
    tmp_keys = [tuple(key.split('_')[1:]) for key in dict_keys]

    if len(turb_model_list) > 0:
        tmp_keys = [tuple(key.split('-')[0].split('_')[1:]) for key in dict_keys]
    else:
        # return a default name for the turbulence model
        turb_model_list = ["TurbModel"]*len(dict_keys)

    return tmp_keys, turb_model_list

def sort_data_dict_based_on_column(data_dict, ref_col):

    for key1 in data_dict.keys():
        for key2 in data_dict[key1].keys():
            for key3 in data_dict[key1][key2].keys():
                ind = np.argsort(data_dict[key1][key2][key3][:,ref_col])
                data_dict[key1][key2][key3] = data_dict[key1][key2][key3][ind]
    # return data_set[ind]


def read_ccm_file(filename):
    """ StarCCM writes csv files based on boundaries, so it could potentially
        have multiple columns. This script reduces the number of columns to two,
        which assumes that there are only two relevant scalars in the file.
    """

    data = np.loadtxt(filename, dtype = str, delimiter = ',', skiprows=1)
    col1 = []
    col2 = []
    for ind in np.arange(0,len(data[0]),2):
        col1.append(data[:,ind])
        col2.append(data[:,ind+1])

    col1 = np.array(col1).reshape((1,-1))
    col2 = np.array(col2).reshape((1,-1))

    col1 = [float(val) for val in col1[0] if val != 'null']
    col2 = [float(val) for val in col2[0] if val != 'null']

    res = np.array([(val1, val2) for val1, val2 in zip(col1, col2)])
    return res




def plot_loop_turbulence_models(data_dict, tgt_mesh, tgt_turb_list = None,
                                naming_dict={}, user_color = None,
                                scale_fac = 1,
                                scale_fac_dict = {'wallP':1, 'wallHeatFlux':1}
                            ):
    linestyles_list = ['-','--','dashdot', 'dotted']
    color_backup_list = ['darkkhaki', 'bisque', 'lightsteelblue']
    # color_list = [
    #     np.array([1, 0, 0]),
    #     np.array([0, 0, 1]),
    #     np.array([0, 1, 0]),
    #     np.array([0.8916548 , 0.45756748, 0.77818808]),
    #     np.array([0.26706377, 0.99610621, 0.54009489]),
    #     np.array([0.53752161, 0.40099938, 0.70540579]),
    #     np.array([0.40518559, 0.94999075, 0.03075388]),
    #     np.array([0.13602495, 0.08297726, 0.42352224]),
    #     np.array([0.23449723, 0.74743526, 0.65177865]),
    #     np.array([0.68998682, 0.16413419, 0.87642114]),
    #     np.array([0.44733314, 0.57871104, 0.52377835]),
    #     np.array([0.62689056, 0.34869427, 0.26209748]),
    #     np.array([0.07498055, 0.1794057 , 0.82999425])]
    color_list = ['red', 'blue','green', 'black', 'yellow', 'brown', 'cyan',
                 'grey','magenta']*3



    mesh_label = tgt_mesh 
    try:
        mesh_label = naming_dict['mesh'][tgt_mesh]
    except KeyError:
        pass
    # prng = np.random.RandomState(1234567890)
    
    linestyle_counter = 0
    color_counter = 0
    for ind, turb_model in enumerate(sorted(data_dict[tgt_mesh].keys())):
        turb_label = turb_model
        try:
            turb_label = naming_dict['turb'][turb_model]
        except KeyError:
            pass

        labelname = " ".join((mesh_label, turb_label))

        # color = prng.rand(3,)
        color = color_list[ind]
        if user_color is not None:
            color = user_color
            if (linestyle_counter > 0) & (np.mod(linestyle_counter,3) == 0):
                color_counter +=1
                color = color_backup_list[color_counter-1]
                linestyle_counter = 0
            if color_counter > 0:
                color = color_backup_list[color_counter-1]
        # probably a better way to do this but will do for now 
        if tgt_turb_list is None:
            plt.plot(data_dict[tgt_mesh][turb_model][:-2,0],
                    data_dict[tgt_mesh][turb_model][:-2,1] * scale_fac,
                    color = color,
                    label = labelname,
                    linestyle= linestyles_list[linestyle_counter],
                    linewidth = 2.0)
            linestyle_counter +=1
        else:
            if turb_model in tgt_turb_list:
                if user_color is None:
                    color = color_list[color_counter] 
                    # use counter for color if not assigned by used
                    color_counter +=1
                plt.plot(data_dict[tgt_mesh][turb_model][:-2,0],
                        data_dict[tgt_mesh][turb_model][:-2,1]* scale_fac,
                        color = color,
                        label = labelname,
                        linestyle= linestyles_list[linestyle_counter],
                        linewidth = 2.0)
                linestyle_counter +=1

def apply_axes_limits(run_nb, geom_nb):
    if run_nb in ["run28", "run34"]:
        plt.xlim([88*INCH_TO_M, 96*INCH_TO_M])
    elif run_nb in ["run33"]:
        plt.xlim([85*INCH_TO_M, 98*INCH_TO_M])
    elif run_nb in ["run14"]:
        plt.xlim([88*INCH_TO_M, 98.5*INCH_TO_M])
    elif run_nb in ["run45"]:
        plt.xlim([88*INCH_TO_M, 97.8*INCH_TO_M])

    else:
        plt.xlim([91.5*INCH_TO_M, 96*INCH_TO_M])
    if geom_nb == "geom1":
        plt.xlim([85*INCH_TO_M, 115*INCH_TO_M])
    
    if run_nb == 'run4':
        plt.xlim([92*INCH_TO_M, 115*INCH_TO_M])
    plt.xlabel('x (m)')


def plot_mesh_loop(cfd_data_dict, key_select, tgt_mesh_list = None, tgt_turb_list = None,
                        naming_dict = {}, scaling_dict = {'wallP':1,
                                                'wallYPlus':1,
                                                'skinFrictionCoeff':1,
                                                'wallHeatFlux':1}):

    mesh_colors = ['blue','red','green','black','brown', 'violet']
    for ind, mesh in enumerate(sorted(cfd_data_dict[key_select].keys())):
        # Sorted is required to order the grids
        print("Scaling quantity", key_select, " by ", scaling_dict[key_select])
        if tgt_mesh_list is None:
            plot_loop_turbulence_models(cfd_data_dict[key_select], mesh,
                                            tgt_turb_list = tgt_turb_list,
                                            naming_dict = naming_dict,
                                            user_color=mesh_colors[ind],
                                            scale_fac = scaling_dict[key_select])
        else:
            if mesh in tgt_mesh_list:
                plot_loop_turbulence_models(cfd_data_dict[key_select], mesh,
                                tgt_turb_list = tgt_turb_list,
                                naming_dict = naming_dict)



def load_experimental_data(ref_folder, ref_pressure_file, ref_heatflux_file):
    try:
        ref_pressure_data = np.loadtxt(os.path.join(ref_folder, ref_pressure_file),
                                        delimiter = ',', skiprows = 1, dtype=np.float64)
        if not "run6" in ref_pressure_file:
            ref_pressure_data[:,1] *= PSIA_TO_PASCAL

            ref_pressure_data[:,0] *= INCH_TO_M

            # sys.exit()
        else:
            ref_pressure_data[:,0] *= 1e-3

        if "run4_" in ref_pressure_file:
            # Experimental data x-positions taken in direction of cone -> Xc
            # If wish to compare data at axial location along symmetry we must transform
            # the experimental data
            ref_pressure_data[:,0] *= np.cos(np.deg2rad(6))
            print("Experimental data is transformed from ramp direction to axial distance")
        if "run6_" in ref_pressure_file:
            # Experimental data x-positions taken in direction of cone -> Xc
            # If wish to compare data at axial location along symmetry we must transform
            # the experimental data
            ref_pressure_data[:,0] *= np.cos(np.deg2rad(6))
            print("Experimental data is transformed from ramp direction to axial distance")
        # if "run14" in ref_pressure_file:
        #     # Experimental data x-positions taken in direction of cone -> Xc
        #     # Does not seem the same for Geom2 data, looks like x correct, 
        #       see also Alviani thesis
        #     ref_pressure_data[:,0] *= np.cos(np.deg2rad(7))

    except FileNotFoundError:
        ref_pressure_data = None

    try:
        ref_heatflux_data = np.loadtxt(os.path.join(ref_folder, ref_heatflux_file),
                                        delimiter = ',', skiprows = 1)
        if not "run6" in ref_heatflux_file:
            ref_heatflux_data[:,1] *= BTU_FT2_SEC_TO_W_M2
            ref_heatflux_data[:,0] *= INCH_TO_M
        else:
            ref_heatflux_data[:,0] *= 1e-3


        if "run4_" in ref_heatflux_file:
            # Experimental data x-positions taken in direction of cone -> Xc
            # If wish to compare data at axial location along symmetry we must transform
            # the experimental data
            ref_heatflux_data[:,0] *= np.cos(np.deg2rad(6))

        if "run6_" in ref_heatflux_file:
            # Experimental data x-positions taken in direction of cone -> Xc
            # If wish to compare data at axial location along symmetry we must transform
            # the experimental data
            ref_heatflux_data[:,0] *= np.cos(np.deg2rad(6))
        # if "run14" in ref_heatflux_file:
        #     ref_pressure_data[:,0] *= np.cos(np.deg2rad(7))
    except FileNotFoundError:
        ref_heatflux_data = None

    return np.array(ref_pressure_data, dtype = np.float64), np.array(ref_heatflux_data)




def find_separation_onset_gradpx(data_dict, xbounds, tgt_mesh = None, turb_model = None):
    """ Function will compute the gradient of pressure at the wall and find the onset
        of separation as the maximum value in a user defined window.
        Current implementation only for single turbulence model if an extra nested level.

        Args:
            data_dict (dict): containing the wall pressure data and associated meshes
            xbounds (list): min and max value to limit the search window for maximum
            tgt_mesh (str): name of mesh to consider in case we wish to limit to single mesh,
                            default = None
            turb_model (str): name of turb model to consider in case we have a turb model nesting
                            default = None
        
        Returns:
            res_list, mesh_list (np.array, list): resulting xlocation of separation onset, keys of meshes
    """

    key_select = 'wallP' # a default

    xmin, xmax = xbounds
    mesh_list = sorted(list(data_dict[key_select].keys()))

    if tgt_mesh is not None:
        mesh_list = list(tgt_mesh)

    res_list = np.zeros(len(mesh_list))

    # NOTE: function will actually work if the input dict does not contain the
    #          'mesh' key and we directly have a number of turbulence models

    for ind, mesh_key in enumerate(mesh_list):
        if isinstance(data_dict[key_select][mesh_key], dict):
            assert turb_model is not None
            gradpx = np.gradient(data_dict[key_select][mesh_key][turb_model][:,1], data_dict[key_select][mesh_key][turb_model][:,0])
            xvals = data_dict[key_select][mesh_key][turb_model][:,0]

        else:
            gradpx = np.gradient(data_dict[key_select][mesh_key][:,1], data_dict[key_select][mesh_key][:,0])
            xvals = data_dict[key_select][mesh_key][:,0]

        gradpx = np.nan_to_num(gradpx) # if mesh very fine and two similar coords we get a nan
                                        # replace them by 0 and we neglect in evaluation
        indx_select, = np.where((xvals > xmin) & (xvals < xmax))
        gradpx_max = np.max(gradpx[indx_select])
        # print(gradpx_max)
        ind_gradpx_max, = np.where(gradpx[indx_select] == gradpx_max)
        res_list[ind] = xvals[indx_select][ind_gradpx_max[0]]
        
    return res_list, mesh_list



def find_indices_between_vals(array, minval, maxval):
    inds, = np.where((array > minval) & (array < maxval))
    return inds


def filter_data_based_on_axial_position(turb_dict, geom_nb, xmin = None, xmax = None):
    """ This functions reads in a dictionary of numpy arrays corresponding to the
        turbulence models selected and filters the values based on the
        streamwise / axial position
    """

    # define bounds to consider
    if xmin is None:
        xmin = 0
    if xmax is None:
        xmax = length_dict[geom_nb]['total']
    
    tmp_dict = copy.deepcopy(turb_dict)
    for key, vals in turb_dict.items():
        tmp_dict[key] = vals[find_indices_between_vals(vals[:,0], xmin, xmax)]

    return tmp_dict


def filter_global_dict_based_on_parameters(cfd_dict,
                                            param_dict,
                                            geom_nb,
                                            keys_list = ['wallP', 'wallHeatFlux']):
    """ Functions reduces the global cfd data dict by selecting only the
        results set by paramater dict. On top of that only the data
        along the cone-flare geometry is selected based on the length of the
        cone-flare set by geom_nb
    """

    res_dict = {}
    for _, cfdcode in enumerate(param_dict.keys()):
        res_dict[cfdcode] = {}
        for variable in keys_list:
            turb_model_list = None
            turb_dict = cfd_dict[cfdcode][variable][param_dict[cfdcode]['mesh']]

            # Filter on selected turb model if valid for solver in param matrix
            if 'turb_model_list' in param_dict[cfdcode].keys():
                turb_model_list = param_dict[cfdcode]['turb_model_list']
                tmp_dict = copy.deepcopy(turb_dict)
                for turbmod in turb_dict.keys():
                    if turbmod not in turb_model_list:
                        del tmp_dict[turbmod]
                turb_dict = tmp_dict



            tmp_dict = filter_data_based_on_axial_position(turb_dict, geom_nb)

            res_dict[cfdcode][variable] = tmp_dict
    return res_dict


def find_nearest(array, value): # from stackoverflow, 
                                # https://stackoverflow.com/questions/2566412/find-nearest-value-in-numpy-array
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return idx #array[idx]
    
def find_peak_value(data_dict, tgt_mesh = None, key_select = None, start_xcoord = None,
                    end_xcoord = None):
    start_xind = 0
    end_xind = -1
    mesh_list = sorted(list(data_dict[key_select].keys()))

    if tgt_mesh is not None:
        mesh_list = list(tgt_mesh)
    print('mesh list', mesh_list)
    xres_list = np.zeros(len(mesh_list))
    pres_list = np.zeros(len(mesh_list))


    for ind, mesh_key in enumerate(mesh_list):

        if start_xcoord is not None:
            start_xind = find_nearest(data_dict[key_select][mesh_key][:,0], start_xcoord)

        if end_xcoord is not None:
            end_xind = find_nearest(data_dict[key_select][mesh_key][:,0], end_xcoord)

        xvals = data_dict[key_select][mesh_key][start_xind:end_xind,0]
        pdata = data_dict[key_select][mesh_key][start_xind:end_xind,1]
        p_max = np.max(pdata)
        ind_p_max, = np.where(pdata == p_max)
        xres_list[ind] = xvals[ind_p_max[0]]
        pres_list[ind] = p_max

    return xres_list, pres_list,  mesh_list


def compute_integral_quantities(cfd_dict, start_xcoord = None,
                                end_xcoord = None,
                                keys_list = ['wallP', 'wallHeatFlux'],
                                scale_by_integral_x = False):
    scaling_dict = {'wallP':1e-3, 'wallHeatFlux': 1e-6}
    round_dict = {'wallP':2, 'wallHeatFlux': 3}
    res_dict = {}

    if start_xcoord is not None:
        print('Setting user defined min xbound ', start_xcoord)
    if end_xcoord is not None:
        print('Setting user defined max xbound ', end_xcoord)
        
    for cfdcode in cfd_dict.keys():
        res_dict[cfdcode] = {}
        for variable in keys_list:
            for _, (turb_mod, vals) in enumerate(cfd_dict[cfdcode][variable].items()):
                if (variable == keys_list[0]):
                    res_dict[cfdcode][turb_mod] = {}

                start_xind = 0
                end_xind = -1
                if start_xcoord is not None:
                    start_xind = find_nearest(vals[:,0], start_xcoord)

                if end_xcoord is not None:
                    end_xind = find_nearest(vals[:,0], end_xcoord)

                int_val = int(np.trapz(vals[start_xind:end_xind,1],
                                            vals[start_xind:end_xind,0]
                                            )
                                        ) * scaling_dict[variable]
                
                if scale_by_integral_x:
                    int_val /= np.trapz(np.ones(len(vals[start_xind:end_xind,0])),
                                            vals[start_xind:end_xind,0]
                                            )
                    print("integrated length for scaling = ",
                            np.trapz(np.ones(len(vals[start_xind:end_xind,0])),
                                            vals[start_xind:end_xind,0]
                                            ))
                int_val = round(int_val,round_dict[variable])
                # print(variable)

                res_dict[cfdcode][turb_mod]['integrated_'+variable] = int_val
            # Sort per CFD code
            res_dict[cfdcode]= dict(sorted(res_dict[cfdcode].items()))
    return res_dict


def compute_separation_onsets_solvers(data_dict, xbounds, xbounds_dict = None):
    tmp_dict = {}
    
    for cfdcode in data_dict.keys():
        tmp_xbounds = xbounds
        if xbounds_dict is not None:
            if cfdcode in xbounds_dict.keys():
                tmp_xbounds = xbounds_dict[cfdcode]
        res_sep, turb = find_separation_onset_gradpx(data_dict[cfdcode], tmp_xbounds)
        tmp_dict[cfdcode] =  dict([(turb, round(val,3)) 
                                    for val, turb in zip(res_sep, turb)])
    return tmp_dict


def compute_peak_values_solvers(data_dict, tgt_var, start_xcoord = None,
                                                    end_xcoord = None):
    scaling_dict = {'wallP':1e-3, 'wallHeatFlux': 1e-6}
    round_dict = {'wallP':2, 'wallHeatFlux': 3}
    tmp_dict = {}
    for cfdcode in data_dict.keys():
        tmp_dict[cfdcode] = {}
        res_loc, res_peak, turb = find_peak_value(data_dict[cfdcode],
                                                key_select = tgt_var,
                                                start_xcoord= start_xcoord,
                                                end_xcoord = end_xcoord)
        tmp_dict[cfdcode]['peak'] =  dict([(turb, round(val*scaling_dict[tgt_var],
                                                        round_dict[tgt_var])) 
                                                for val, turb in zip(res_peak, turb)])
        tmp_dict[cfdcode]['peak_loc'] =  dict([(turb, round(val,3)) for val, turb in zip(res_loc, turb)])
    return tmp_dict


def compute_data_bounds(data_dict, key_data_select = 'wallP'):
    tmp_dict = {}
    largest_min = 0
    smallest_max = 100
    for cfdcode in data_dict.keys():
        tmp_dict[cfdcode] = {}
        print(cfdcode)
        tmp_info_min = {}
        tmp_info_max = {}
        print(data_dict[cfdcode].keys())
        for turb_mod in data_dict[cfdcode][key_data_select]:
            tmp_info_min[turb_mod] = round(np.min(data_dict[cfdcode][key_data_select][turb_mod][:,0]),
                                                    5)
            tmp_info_max[turb_mod] = round(np.max(data_dict[cfdcode][key_data_select][turb_mod][:,0]),
                                                5)
            if tmp_info_min[turb_mod] > largest_min:
                largest_min = tmp_info_min[turb_mod]
            if tmp_info_max[turb_mod] < smallest_max:
                smallest_max = tmp_info_max[turb_mod]
            
        # xmin, xmax = find_peak_value(data_dict[cfdcode],
        #                                         key_select = tgt_var,
        #                                         start_xcoord= start_xcoord,
        #                                         end_xcoord = end_xcoord)

        tmp_dict[cfdcode]['xmin'] = tmp_info_min
        tmp_dict[cfdcode]['xmax'] = tmp_info_max
    tmp_dict['largest_min'] = largest_min
    tmp_dict['smallest_max'] = smallest_max
    print(largest_min, smallest_max)
    return tmp_dict


def obtain_mapping_dict():
    mapping_dict = {
        'gaspex': 'GASPex',
        'eilmer': 'Eilmer',
        'cadence': 'Cadence Fidelity',
        'ansys_aselsan': 'Ansys Fluent (Aselsan)',
        'ansys_inc': 'Ansys Fluent (Ansys Inc)',
        'tau': 'TAU',
        'coda':'HyperCODA',
        'overflow': 'OVERFLOW',
        'vulcan': 'VULCAN',
        'starccm': 'STAR-CCM+',
        'komega06': 'k-$\\omega$ 2006',
        'komega': 'k-$\\omega$ 2006',
        'SST': 'k-$\\omega$ SST',
        'SSCEARSM_Prt086Lemmon': 'SSC-EARSM',
        'SSTa10355_Prt086Lemmon_LDFSS': 'k-$\\omega$ SST a1=0.355',
        'SSTa10355': 'k-$\\omega$ SST',
        'SSTa10355_Prt086Lemmon': 'k-$\\omega$ SST',
        'SAnegN=646308QCR=off': 'SA-neg',
        'Menter_SST': 'k-$\\omega$ SST',
        'SSGLRRw': 'SSG/LRR-$\\omega$ 2010',
        'GEKO': 'GEKO',
        'SAneg': 'SA-neg',
        'SBSLPrt086': 'SBSL EARSM',
        'SST1T': 'k-$\\omega$ SST',
        'SA1T':'SA',
        'SST2T': 'k-$\\omega$ SST 2-T model',
        'SA2T':'SA 2-T model',
        'SSTa1coeff0355': 'k-$\\omega$ SST a1=0.355',
        'SSTa1coeff031': 'k-$\\omega$ SST a1=0.31',
        'SST2Ta1coeff031': 'k-$\\omega$ SST 2T a1=0.31',
        'SSTV': 'k-$\\omega$ SST-V',
        'SSTVnorhok': 'k-$\\omega$ SST-V no 2/3 rho*k',
        'SSTKL': 'k-$\\omega$ SST-KL',
        'SAQCRV': 'SA 2013 QCR-V',
        'SSCEARSM_Prt086Lemmon_LDFSS': 'SSC-EARSM',
        'SSTa10355_Prt086Lemmon_LDFSS':  'k-$\\omega$ SST a1=0.355',
        'SAO':'SA-noft2',
        'EARSMWJ3DTNT': 'EARSM WJ3D+TNT',
        'EARSMWJHellsten': 'EARSM WJ+Hellsten',
        'SSGLRRw2010':'SSG/LRR-$\\omega$ 2010',
        'SST2003': 'k-$\\omega$ SST 2003',
        'komegaMenterBSL': 'Menter BSL',
        'komegaWilcox': 'Wilcox k-$\\omega$ 1988',
        'wilcox+SST': 'Wilcox k-$\\omega$ + SST',
        'WilcoxRSM2010':'Wilcox RSM 2010'


    }

    return mapping_dict

def create_latex_table_integrated(nested_dict, run_nb, mapping_dict = None,
            resizebox = False):
    table_caption = f"Integrated wall quantities for run {run_nb.replace('run','')} ."
    table_caption += " Values are scaled by $\int$dx."
    table_label = f"res_comparison_integrated_{run_nb}"

    # Mapping of old names to new names
    if mapping_dict is None:
        mapping_dict = obtain_mapping_dict()

    # Function to get the new name from the mapping
    def get_new_name(old_name):
        return mapping_dict.get(old_name, old_name)
        
    # Start creating the LaTeX table
    latex_table = """
    \\begin{table}[ht]
    \\centering
    \\begin{tabular}{llll}
    \\hline
    \\textbf{Solver} & \\textbf{Turbulence Model} & \\textbf{pressure (kPa)} & \\textbf{heat flux (MW/($m^2$))} \\\\
    \\hline
    \\hline
    """

    # Iterate through the nested dictionary to fill in the table
    for main_key, sub_dict in nested_dict.items():
        new_main_key = get_new_name(main_key) # replace solver name
        first_entry = True
        for sub_key, values in sub_dict.items():
            new_sub_key = get_new_name(sub_key) # turb model naming
            if first_entry:
                latex_table += f"{new_main_key} & {new_sub_key} & {values['integrated_wallP']} & {values['integrated_wallHeatFlux']} \\\\\n"
                first_entry = False
            else:
                latex_table += f" & {new_sub_key} & {values['integrated_wallP']} & {values['integrated_wallHeatFlux']} \\\\\n"
        latex_table += "\\hline\n"

    # End the table
    latex_table += f"""
    \\end{{tabular}}
    \\caption{{{table_caption}}}
    \\label{{tab:{table_label}}}
    \\end{{table}}
    """
    if resizebox:
        latex_table = latex_table.replace("\\centering", "\\resizebox{\columnwidth}{!}{%")
        latex_table = latex_table.replace("\\end{tabular}", "\\end{tabular} \n\t}")
    return latex_table



def create_latex_table_separation(nested_dict, run_nb, mapping_dict = None,
                                    resizebox = False):
    table_caption = f"Separation, peak values and associated location for run {run_nb.replace('run','')}"
    table_label = f"res_comparison_separation_{run_nb}"

    # Mapping of old names to new names
    if mapping_dict is None:
        mapping_dict = obtain_mapping_dict()

    # Function to get the new name from the mapping
    def get_new_name(old_name):
        return mapping_dict.get(old_name, old_name)

 
    # Start creating the LaTeX table
    latex_table = """
    \\begin{table}[ht]
    \\centering
    \\begin{tabular}{p{1.8cm}p{2.6cm}p{1.1cm}p{1.3cm}p{1.4cm}p{1.8cm}p{1.4cm}}
    \\hline
    \\textbf{Solver} & \\textbf{Turbulence Model} & \\textbf{x$_{sep}$ (m)} &  \\textbf{p$_{peak}$ (kPa)} & \\textbf{p$_{peak,loc}$ (m)} &  \\textbf{q$_{peak}$ (MW/($m^2$))} &  \\textbf{q$_{peak,loc}$ (m)} \\\\
    \\hline
    \\hline
    """

    # Iterate through the nested dictionary to fill in the table
    for main_key, sub_dict in nested_dict.items():
        new_main_key = get_new_name(main_key)
        first_entry = True
        for sub_key, values in sub_dict.items():
            new_sub_key = get_new_name(sub_key)
            if first_entry:
                latex_table += f"{new_main_key} & {new_sub_key} & {values['separation_loc']} & {values['peak_p']} & {values['peak_p_loc']} & {values['peak_q']} & {values['peak_q_loc']}\\\\\n"
                first_entry = False
            else:
                latex_table += f" & {new_sub_key} & {values['separation_loc']} & {values['peak_p']} & {values['peak_p_loc']} & {values['peak_q']} & {values['peak_q_loc']} \\\\\n"
        latex_table += "\\hline\n"

    # End the table
    latex_table += f"""
    \\end{{tabular}}
    \\caption{{{table_caption}}}
    \\label{{tab:{table_label}}}
    \\end{{table}}
    """
    if resizebox:
        latex_table = latex_table.replace("\\centering", "\\resizebox{\columnwidth}{!}{%")
        latex_table = latex_table.replace("\\end{tabular}", "\\end{tabular} \n\t}")
    return latex_table


    return latex_table


def create_latex_table_variations(nested_dict, run_nb):
    table_caption = f"Absolute variations in predictions of separation, peak values and associated location for run {run_nb.replace('run','')}"
    table_label = f"res_comparison_variation_{run_nb}"


    # Start creating the LaTeX table
    latex_table = """
    \\begin{table}[ht]
    \\center
    \\begin{tabular}{p{1.8cm}p{1.8cm}p{1.8cm}p{1.8cm}p{1.8cm}}
    \\hline
    \\ $\Delta$ Separation onset (cm) & $\Delta$ Peak pressure location (cm) & $\Delta$ Peak pressure (kPa) & $\Delta$ Peak heat flux location (cm) & $\Delta$ Peak heat flux (MW/m$^2$) \\\\
    \\hline
    \\hline
    """

    # Iterate through the nested dictionary to fill in the table

    # for subkey in nested_dict.keys():
    #     # if first_entry:
    #     #     latex_table += f"{new_main_key} & {new_sub_key} & {values['separation_loc']} & {values['peak_p']} & {values['peak_p_loc']} & {values['peak_q']} & {values['peak_q_loc']}\\\\\n"
    #     #     first_entry = False
    #     # else:
    latex_table += f"{round(nested_dict['separation_loc']['variation']*100,2)}"
    # & {nested_dict['peak_p']['variation']} & {nested_dict['peak_p_loc']['variation']} & {nested_dict['peak_q']['variation']} &  {nested_dict['peak_q_loc']['variation']} \\\\\n"
    latex_table += f"& {round(nested_dict['peak_p_loc']['variation']*100,2)}"
    latex_table += f"& {round(nested_dict['peak_p']['variation'],2)}"
    latex_table += f"& {round(nested_dict['peak_q_loc']['variation']*100,2)}"
    latex_table += f"& {round(nested_dict['peak_q']['variation'],3)}\\\\\n"

    latex_table += "\\hline\n"

    # End the table
    latex_table += f"""
    \\end{{tabular}}
    \\caption{{{table_caption}}}
    \\label{{tab:{table_label}}}
    \\end{{table}}
    """
    return latex_table


def join_separation_dicts(sep_dict, pres_dict, heat_dict):
    tmp_dict = {}
    for cfdsolver in sep_dict.keys():
        tmp_dict[cfdsolver] = {}
        for turb_model in sep_dict[cfdsolver].keys():
            tmp_dict[cfdsolver][turb_model] = {}
            tmp_dict[cfdsolver][turb_model]['separation_loc'] = sep_dict[cfdsolver][turb_model]
            tmp_dict[cfdsolver][turb_model]['peak_p'] = pres_dict[cfdsolver]['peak'][turb_model]
            tmp_dict[cfdsolver][turb_model]['peak_p_loc'] = pres_dict[cfdsolver]['peak_loc'][turb_model]
            tmp_dict[cfdsolver][turb_model]['peak_q'] = heat_dict[cfdsolver]['peak'][turb_model]
            tmp_dict[cfdsolver][turb_model]['peak_q_loc'] = heat_dict[cfdsolver]['peak_loc'][turb_model]

    return tmp_dict
