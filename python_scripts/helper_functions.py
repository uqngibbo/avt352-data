import os
import glob
import numpy as np
import matplotlib.pyplot as plt


INCH_TO_M = 2.54e-2
PSIA_TO_PASCAL = 6894.76
BTU_FT2_SEC_TO_W_M2 = 11356.538527


def create_cfddatadict_for_solver(solvername, cfdfilenames):

    assert solvername in ['starccm', 'h3amr', 'ansys_inc','ansys_aselsan',
                            'eilmer', 'tau', 'cadence', 'gaspex', 'coda',
                            'SU2', 'tau2', 'overflow']

    keys, turb_model_list = evaluate_dictionary_key_from_filename(cfdfilenames)
    if solvername == 'starccm':
        cfd_data_dict = load_data_files_ccm(cfdfilenames,
                                        keys,
                                        turb_model_list,
                                        dtype = 'float'
                                    )

    if solvername == 'h3amr':
        cfd_data_dict = load_data_files_h3amr(cfdfilenames,
                                        keys,
                                        turb_model_list,
                                        dtype = 'float'
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




    return cfd_data_dict


def read_cadence_file(filename):
    tmp_data = np.unique(np.genfromtxt(filename,
                                        delimiter=' ',
                                        skip_header=1),
                        axis = 0)
    
    tmp_data = np.array([(val1, val2) for val1, val2
                                        in zip(tmp_data[:,2], tmp_data[:,3])])
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
                result[key1][key2][key3] = np.loadtxt(filename)
            elif solver != 'cadence':
                result[key1][key2][key3] =  np.loadtxt(
                                            filename,
                                            skiprows=skiprows,
                                            delimiter = delim,
                                            dtype = dtype
                                        ) * multiplier


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
                                scale_fac = 1):
    linestyles_list = ['-','--','dashdot']
    mesh_label = tgt_mesh 
    try:
        mesh_label = naming_dict['mesh'][tgt_mesh]
    except KeyError:
        pass
    prng = np.random.RandomState(1234567890)
    
    linestyle_counter = 0
    for turb_model in data_dict[tgt_mesh].keys():

        turb_label = turb_model
        try:
            turb_label = naming_dict['turb'][turb_model]
        except KeyError:
            pass

        labelname = " ".join((mesh_label, turb_label))

        
        color = prng.rand(3,)
        if user_color is not None:
            color = user_color
        # probably a better way to do this but will do for now 
        if tgt_turb_list is None:
            plt.plot(data_dict[tgt_mesh][turb_model][:-2,0],
                    data_dict[tgt_mesh][turb_model][:-2,1] * scale_fac,
                    color = color,
                    label = labelname)
        else:
            if turb_model in tgt_turb_list:
                plt.plot(data_dict[tgt_mesh][turb_model][:-2,0],
                        data_dict[tgt_mesh][turb_model][:-2,1]* scale_fac,
                        color = color,
                        label = labelname,
                        linestyle= linestyles_list[linestyle_counter])
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
        print(gradpx_max)
        ind_gradpx_max, = np.where(gradpx[indx_select] == gradpx_max)
        res_list[ind] = xvals[indx_select][ind_gradpx_max[0]]
        
    return res_list, mesh_list

