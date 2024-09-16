""" Plotting the data from Holden simu
"""

import os
import glob
import numpy as np
import matplotlib.pyplot as plt
from pyGCS import GCS

INCH_TO_M = 2.54e-2
PSIA_TO_PASCAL = 6894.76
BTU_FT2_SEC_TO_W_M2 = 11356.538527

def load_data_files(tgt_files, dict_keys, dtype = 'float', skiprows=1):
    """ load a set of data files and add them in a dictionary format
    """

    result = dict()
    for (key1, key2), filename in zip(keys, tgt_files):
        print("Loading filename ", filename)
        result.setdefault(key1, {}).update({key2: np.loadtxt(filename, skiprows=skiprows,delimiter = ",", dtype = dtype)})
    # data = [(dict_key, np.loadtxt(filename, skiprows=skiprows,delimiter = ",", dtype = dtype))
    #                 for dict_key, filename in zip(dict_keys,tgt_files)]

    return result

def evaluate_dictionary_key_from_filename(tgt_files):
    dict_keys = [filename.split('.')[0] if not "/" in filename else filename.split('/')[-1].split('.')[0]
                    for filename in tgt_files]
    dict_keys = [key.split('-')[0] for key in dict_keys]
    dict_keys = [tuple(key.split('_')[1:]) for key in dict_keys]

    return dict_keys

def sort_data_dict_based_on_column(data_dict, ref_col):
    # NOTE: make this stateless
    for key1 in data_dict.keys():
        for key2 in data_dict[key1].keys():
            ind = np.argsort(data_dict[key1][key2][:,ref_col])
            data_dict[key1][key2] = data_dict[key1][key2][ind]
    # return data_set[ind]


def find_separation_onset_gradpx(data_dict, xbounds, tgt_mesh = None):
    """ Function will compute the gradient of pressure at the wall and find the onset
        of separation as the maximum value in a user defined window

        Args:
            data_dict (dict): containing the wall pressure data and associated meshes
            xbounds (list): min and max value to limit the search window for maximum
            tgt_mesh (str): name of mesh to consider in case we wish to limit to single mesh,
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
        gradpx = np.gradient(data_dict[key_select][mesh_key][:,1], data_dict[key_select][mesh_key][:,0])

        xvals = data_dict[key_select][mesh_key][:,0]
        indx_select, = np.where((xvals > xmin) & (xvals < xmax))
        gradpx_max = np.max(gradpx[indx_select])
        ind_gradpx_max, = np.where(gradpx[indx_select] == gradpx_max)
        res_list[ind] = xvals[indx_select][ind_gradpx_max[0]]
        
    return res_list, mesh_list


def find_peak_value(data_dict, tgt_mesh = None, key_select = 'wallP', start_xcoord = None,
                    end_xcoord = None):
    start_xind = 0
    end_xind = -1
    mesh_list = sorted(list(data_dict[key_select].keys()))

    if tgt_mesh is not None:
        mesh_list = list(tgt_mesh)

    xres_list = np.zeros(len(mesh_list))
    pres_list = np.zeros(len(mesh_list))

    def find_nearest(array, value): # from stackoverflow, 
                                    # https://stackoverflow.com/questions/2566412/find-nearest-value-in-numpy-array
        array = np.asarray(array)
        idx = (np.abs(array - value)).argmin()
        return idx #array[idx]

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

def write_info_to_file(res_sep, res_peak_p, res_peak_q, run_nb):
    with open("separation_peak_"+run_nb+".txt", 'w') as fout:
        fout.write("variable," + ','.join(res_sep[1]) + "\n")
        fout.write("ncells," + ','.join(np.array(list(mesh_info.values())).astype(str)) + "\n")
        fout.write("xloc_separation," + ','.join(res_sep[0].astype(str))  + "\n")
        fout.write("xloc_peak_pressure," + ','.join(res_peak_p[0].astype(str))  + "\n")
        fout.write("peak_pressure," + ','.join(res_peak_p[1].astype(str))  + "\n")
        fout.write("xloc_peak_heatflux," + ','.join(res_peak_p[0].astype(str))  + "\n")
        fout.write("peak_heatflux," + ','.join(res_peak_p[1].astype(str))  + "\n")



mesh_info = {}
mesh_info['run14'] = {"mesh06":492910, "mesh07":716372, "mesh08":852289, "mesh09":1021124}
mesh_info['run34'] = {"mesh06":492910, "mesh07":714584, "mesh08":851164, "mesh09":1021091}
mesh_info['run45'] = {"mesh06":492910, "mesh07":714584, "mesh08":852289, "mesh09":1021124}
mesh_info['run28'] = {"mesh06":492910, "mesh07":714584, "mesh08":852289, "mesh09":1021124}
mesh_info['run33'] = {"mesh06":492910, "mesh07":714584, "mesh08":852289, "mesh09":1021124}
mesh_info['run37'] = {"mesh06":476712, "mesh07":714584, "mesh08":841415, "mesh09":1012032}
mesh_info['run41'] = {"mesh06":458834, "mesh07":716372, "mesh08":850474, "mesh09":1018451}
mesh_info['run4'] = {"mesh06":549950, "mesh07":808436, "mesh08":1148417}


#-------------------------------------------------------------------------------#
run_nb = 'run4'
geom_nb = "geom1"
solver = 'starccm'
cfd_folder = "../cfddata/"+solver+"/"+geom_nb+"/"+run_nb

res_folder = "comparison_separation_"+solver+"_"+run_nb


#-------------------------------------------------------------------------------#
work_dir = os.getcwd()

cfd_data_filenames = glob.glob(cfd_folder+"/*")

keys = evaluate_dictionary_key_from_filename(cfd_data_filenames)
cfd_data_dict = load_data_files(cfd_data_filenames, keys, dtype = 'float')
sort_data_dict_based_on_column(cfd_data_dict,0)
#-------------------------------------------------------------------------------#

if not os.path.isdir(res_folder):
    os.mkdir(res_folder)
os.chdir(res_folder)

# if ref_pressure_data is not None:
#     # plt.plot(ref_pressure_data[:,0], ref_pressure_data[:,1], linestyle = 'none', marker = 'o')
#     plt.errorbar(ref_pressure_data[:,0], ref_pressure_data[:,1], fmt='o', linestyle = 'none',
#                         yerr=ref_pressure_data[:,1]*3/100,  elinewidth=3,
#                 label='ref')
#     # plt.errorbar(x, y, yerr=dy, fmt='o', color='black',
#     #              ecolor='lightgray', elinewidth=3, capsize=0);

key_select = 'wallP'
tgt_mesh = sorted(list(cfd_data_dict[key_select].keys()))[-1]

gradPx = np.gradient(cfd_data_dict[key_select][tgt_mesh][:,1], cfd_data_dict[key_select][tgt_mesh][:,0])
plt.plot(cfd_data_dict[key_select][tgt_mesh][:,0],
            gradPx
            )
# plt.plot(cfd_data_dict[key_select][tgt_mesh][1:,0],
#             np.diff(cfd_data_dict[key_select][tgt_mesh][:,1]) / np.diff(cfd_data_dict[key_select][tgt_mesh][:,0])
# )
# plt.savefig('temp.png')

# plt.plot(
#             np.gradient(cfd_data_dict[key_select][tgt_mesh][:,1], cfd_data_dict[key_select][tgt_mesh][:,0])
#             )
plt.xlim([2.25,2.4])
plt.savefig('pGrad.png')
plt.close()

if "14" in run_nb:
    xbounds = [1.0,2.33]  # for run 14
elif "28" in run_nb:
    xbounds = [1.0,2.37]  # for run 28
elif "33" in run_nb:
    xbounds = [1.0,2.35] 
elif "34" in run_nb:
    xbounds = [1.0,2.35]
elif "37" in run_nb:
    xbounds = [1.0,2.35] 
elif "41" in run_nb:
    xbounds = [1.0,2.35]  
elif "45" in run_nb:
    xbounds = [1.0,2.35] 
elif "4" in run_nb:
    xbounds = [1.0,2.6] 

# actually could make this dependent on the geom1 or geom2 as separation before second ramp
#  2.37 should be good for both geometries
res_sep = find_separation_onset_gradpx(cfd_data_dict, xbounds)
res_peak_p = find_peak_value(cfd_data_dict)

res_peak_q = find_peak_value(cfd_data_dict, key_select = 'wallHeatFlux', start_xcoord= 1)



#---------------------------------------------------------#

def compute_plot_bounds(vals, deltas = 1):
    bounds_delta = np.max(vals) - np.min(vals)
    return [np.min(vals) - deltas * bounds_delta, np.max(vals) + deltas * bounds_delta]


plt.plot(mesh_info[run_nb].values(), res_sep[0], linestyle = 'none', marker = 's', label = 'separation onset')
plt.plot(mesh_info[run_nb].values(), res_peak_p[0], linestyle = 'none', marker = 'o', label = 'peak')
plt.xlabel("N cells")
plt.ylabel('x (m)')
plt.legend()
# bounds = compute_plot_bounds(np.concatenate([res_sep[0], res_peak_p[0]]))
# plt.ylim(bounds)
plt.tight_layout()
plt.savefig('xloc_separation_peak_pressure.png', dpi=300)
plt.close()



# plt.plot(cfd_data_dict['wallHeatFlux']['mesh08'][:,0]/ INCH_TO_M,
#                 cfd_data_dict['wallHeatFlux']['mesh08'][:,1] / BTU_FT2_SEC_TO_W_M2,
#                                     linestyle = '-', marker = 'o')
# plt.xlim([90,93])
# plt.ylim([0,20])
# # plt.xlabel("N cells")
# # plt.ylabel('x (m)')
# plt.legend()
# plt.tight_layout()
# plt.savefig('heatflux.png', dpi=300)
# plt.close()


ncells_list = np.array(list(mesh_info[run_nb].values()))
ncell_ratios = ncells_list[1:] / ncells_list[:-1]

plt.plot(mesh_info[run_nb].values(), res_peak_q[0], linestyle = 'none', marker = 'o', label = 'peak')
plt.xlabel("N cells")
plt.ylabel('x (m)')
plt.legend()
plt.tight_layout()
plt.savefig('xloc_peak_heatflux.png', dpi=300)
plt.close()

plt.plot(mesh_info[run_nb].values(), res_peak_p[1], linestyle = 'none', marker = 'o', label = 'peak')
plt.xlabel("N cells")
plt.ylabel('P (Pa)')
plt.legend()
plt.tight_layout()
plt.savefig('peak_pressure_meshes.png', dpi=300)
plt.close()

plt.plot(mesh_info[run_nb].values(), res_peak_q[1],
            linestyle = 'none', marker = 'o', label = 'peak')
plt.xlabel("N cells")
plt.ylabel('Q (W/m2)')
plt.legend()
plt.tight_layout()
plt.savefig('peak_heatflux_meshes.png', dpi=300)
plt.close()

# asign = np.sign(gradPx[indx_select])
# signchange = ((np.roll(asign, 1) - asign) != 0).astype(int)
# ind = np.where(signchange == 1)


gcs = GCS(dimension=2,
            simulation_order=3, # Used MUSCL third order scheme
            volume=9.422427e-01,
            oberkampf_correction = True,
            cells= list(ncells_list[[0,1,3]][::-1]),
            solution=list(res_peak_q[1][[0,1,3]][::-1]))

# output information to Markdown-formated table
gcs.print_table(output_type='markdown', output_path='.', )
os.rename("table.md","table_heatflux_mesh06-07-09_oberkampf.md")

gcs = GCS(dimension=2,
            simulation_order=3, # Used MUSCL third order scheme
            volume=9.422427e-01,
            oberkampf_correction = False,
            cells= list(ncells_list[[0,1,3]][::-1]),
            solution=list(res_peak_q[1][[0,1,3]][::-1]))

# output information to Markdown-formated table
gcs.print_table(output_type='markdown', output_path='.', )
os.rename("table.md","table_heatflux_mesh06-07-09_Nooberkampf.md")



gcs.get('gci')
gcs.get('asymptotic_gci')
gcs.get('refinement_ratio')
gcs.get('apparent_order') # order of simulation somehow computed from initial guess, simulation order


gcs = GCS(dimension=2,
            simulation_order=3, # Used MUSCL third order scheme
            volume=9.422427e-01,
            oberkampf_correction = False,
            cells= list(ncells_list[1:][::-1]),
            solution=list(res_peak_q[1][1:][::-1]))

# output information to Markdown-formated table
gcs.print_table(output_type='markdown', output_path='.', )
os.rename("table.md","table_heatflux_mesh07-08-09.md")

gcs = GCS(dimension=2,
            simulation_order=3, # Used MUSCL third order scheme
            volume=9.422427e-01,
            oberkampf_correction = True,
            cells= list(ncells_list[1:][::-1]),
            solution=list(res_peak_q[1][1:][::-1]))

# output information to Markdown-formated table
gcs.print_table(output_type='markdown', output_path='.', )
os.rename("table.md","table_heatflux_mesh07-08-09_oberkampf.md")


gcs = GCS(dimension=2,
            simulation_order=3, # Used MUSCL third order scheme
            volume=9.422427e-01,
            oberkampf_correction = False,
            cells= list(ncells_list[[0,1,3]][::-1]),
            solution=list(res_peak_q[0][[0,1,3]][::-1]))

# output information to Markdown-formated table
gcs.print_table(output_type='markdown', output_path='.', )
os.rename("table.md","table_xloc_peak_heatflux_mesh06-07-09_noOberkampf.md")


gcs = GCS(dimension=2,
            simulation_order=3, # Used MUSCL third order scheme
            volume=9.422427e-01,
            oberkampf_correction = True,
            cells= list(ncells_list[[0,1,3]][::-1]),
            solution=list(res_peak_q[0][[0,1,3]][::-1]))

# output information to Markdown-formated table
gcs.print_table(output_type='markdown', output_path='.', )
os.rename("table.md","table_xloc_peak_heatflux_mesh06-07-09_oberkampf.md")



gcs = GCS(dimension=2,
            simulation_order=3, # Used MUSCL third order scheme
            volume=9.422427e-01,
            oberkampf_correction = True,
            cells= list(ncells_list[1:][::-1]),
            solution=list(res_peak_q[0][1:][::-1]))

# output information to Markdown-formated table
gcs.print_table(output_type='markdown', output_path='.', )
os.rename("table.md","table_xloc_peak_heatflux_mesh07-08-09.md")



gcs = GCS(dimension=2,
            simulation_order=3, # Used MUSCL third order scheme
            volume=9.422427e-01,
            oberkampf_correction = True,
            cells= list(ncells_list[[0,1,3]][::-1]),
            solution=list(res_sep[0][[0,1,3]][::-1]))

# output information to Markdown-formated table
gcs.print_table(output_type='markdown', output_path='.', )
os.rename("table.md","table_xloc_sep_pressure_mesh06-07-09.md")

gcs = GCS(dimension=2,
            simulation_order=3, # Used MUSCL third order scheme
            volume=9.422427e-01,
            oberkampf_correction = True,
            cells= list(ncells_list[[0,1,3]][::-1]),
            solution=list(res_peak_p[0][[0,1,3]][::-1]))

# output information to Markdown-formated table
gcs.print_table(output_type='markdown', output_path='.', )
os.rename("table.md","table_xloc_peak_pressure_mesh06-07-09.md")


os.chdir(work_dir)
