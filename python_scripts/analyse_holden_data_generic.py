""" Plotting the data from Holden simu
"""

import os
import glob
import numpy as np
import matplotlib.pyplot as plt
import helper_functions as helpfunc


#-----------end helper functions------------------------------------------#
#-------------------------------------------------------------------------#

#-------------------------------------------------------------------------------#
#---------User selection zone-------------------------------#
ref_folder = "../refdata"
run_nb = 'run6'
geom_nb = "geom1"
code_cfd = "ansys"
ref_pressure_file = '_'.join((run_nb,"pressure.csv"))
ref_heatflux_file = '_'.join((run_nb,"heatFlux.csv"))

cfd_folder = os.path.join("..","cfddata",code_cfd,geom_nb,run_nb)

res_folder = "_".join((code_cfd,"comparison",run_nb))
work_dir = os.getcwd()

# This dictionary is used to map internal mesh naming or turbulence naming
#       which is found in the filename. If you don't wish to use, just define it as
#       and empty dictionary
# naming_dict = {'mesh':
#                     {'mesh06': 'mesh0',
#                     'mesh07': 'mesh1',
#                     'mesh08': 'mesh2',
#                     'mesh09': 'mesh3'
#                     },
#                 'turb':
#                     {'SST': 'k-$\\omega$ SST'}    
#             }
naming_dict = {}
#-------------------------------------------------------------------------------#
#-------------------------------------------------------------------------------#

ref_pressure_data, ref_heatflux_data = helpfunc.load_experimental_data(ref_folder,
                                                ref_pressure_file,
                                                ref_heatflux_file
                                            )

cfd_data_filenames = glob.glob(cfd_folder+"/*")

cfd_data_dict = helpfunc.create_cfddatadict_for_solver(code_cfd, cfd_data_filenames)
helpfunc.sort_data_dict_based_on_column(cfd_data_dict,0)


#-------------------------------------------------------------------------------#

assert len(cfd_data_filenames) > 0

if not os.path.isdir(res_folder):
    os.mkdir(res_folder)
os.chdir(res_folder)


#--------------------------------------------------------------------#
#------Plot pressure data for single mesh of interest----------------#
#       By default this mesh is the latest one
#User define zone
key_select = 'wallP'
tgt_mesh = sorted(list(cfd_data_dict[key_select].keys()))[-1]
tgt_turb_list = None
#--------------------------------#

if ref_pressure_data is not None:
    # plt.plot(ref_pressure_data[:,0], ref_pressure_data[:,1], linestyle = 'none', marker = 'o')
    plt.errorbar(ref_pressure_data[:,0], ref_pressure_data[:,1],
                    fmt='o', linestyle = 'none',
                    yerr = ref_pressure_data[:,1]*3/100,  elinewidth=3,
                    label='ref')
    # plt.errorbar(x, y, yerr=dy, fmt='o', color='black',
    #              ecolor='lightgray', elinewidth=3, capsize=0);


helpfunc.plot_loop_turbulence_models(cfd_data_dict[key_select], tgt_mesh,
                        naming_dict = naming_dict)

# plt.yscale('log')

# apply pre-defined, run and geometry dependent x-axis limit
helpfunc.apply_axes_limits(run_nb, geom_nb)

plt.ylabel('Pressure (Pa)')
plt.legend()
plt.tight_layout()
plt.savefig('wall_pressure.png')
plt.show()
plt.close()

#-------------------------------------------------------#
#--------------------------------------------------------------------#
#------Plot pressure data for all meshes of interest----------------#
#       No comparison with experimental data in here

#-----------user def zone------------#
tgt_mesh_list = None
tgt_turb_list = ['SST']
key_select = 'wallP'
#------end user def zone------------#

helpfunc.plot_mesh_loop(cfd_data_dict, key_select,
                        tgt_mesh_list, tgt_turb_list = tgt_turb_list,
                        naming_dict = naming_dict)

plt.yscale('log')
# apply pre-defined, run and geometry dependent x-axis limit
helpfunc.apply_axes_limits(run_nb, geom_nb)

plt.ylabel('Pressure (Pa)')
plt.legend()
plt.tight_layout()
plt.savefig('wall_pressure_meshes.png', dpi = 600 )
plt.close()




#-------------------------------------------------------#
#--------------------------------------------------------------------#
#------Plot heatflux data for single mesh of interest----------------#
key_select = 'wallHeatFlux'
tgt_mesh = sorted(list(cfd_data_dict[key_select].keys()))[-1]
tgt_turb_list = None

#------------------------------------------------------------#
if ref_heatflux_data is not None:
    plt.errorbar(ref_heatflux_data[:,0], ref_heatflux_data[:,1], fmt='o', linestyle = 'none',
                        yerr=ref_heatflux_data[:,1]*5/100,  elinewidth=3,
                label='ref')

helpfunc.plot_loop_turbulence_models(cfd_data_dict[key_select], tgt_mesh,
                                        naming_dict = naming_dict)


# plt.yscale('log')

# apply pre-defined, run and geometry dependent x-axis limit
helpfunc.apply_axes_limits(run_nb, geom_nb)

plt.ylabel('Heat Flux (W / $m^2$)')
plt.legend()
plt.tight_layout()
plt.savefig('wall_heatflux.png')
plt.close()


#-------------------------------------------------------#
#--------------------------------------------------------------------#
#------Plot heatflux data for all meshes of interest----------------#
#-----------user def zone------------#
tgt_mesh_list = None
tgt_turb_list = None
key_select = 'wallHeatFlux'
#------end user def zone------------#


helpfunc.plot_mesh_loop(cfd_data_dict, key_select,
                        tgt_mesh_list, tgt_turb_list = tgt_turb_list,
                        naming_dict = naming_dict)

# apply pre-defined, run and geometry dependent x-axis limit
helpfunc.apply_axes_limits(run_nb, geom_nb)

plt.yscale('log')

plt.ylabel('Heat Flux (W / $m^2$)')
plt.tight_layout()
plt.legend()
plt.savefig('wall_heatflux_meshes.png')
plt.close()


#-------------------------------------------------------#
#--------------------------------------------------------------------#
#------Plot yplus data for all meshes of interest----------------#
flag_activate = False

#-----------user def zone------------#
tgt_mesh_list = None
tgt_turb_list = None
key_select = 'wallYPlus'
#------end user def zone------------#
if flag_activate:
    helpfunc.plot_mesh_loop(cfd_data_dict, key_select,
                            tgt_mesh_list, tgt_turb_list = tgt_turb_list,
                            naming_dict = naming_dict)


    # apply pre-defined, run and geometry dependent x-axis limit
    helpfunc.apply_axes_limits(run_nb, geom_nb)

    plt.ylabel('y$^+$ (-)')
    plt.legend()
    plt.tight_layout()
    plt.savefig('wall_yplus_meshes.png', dpi = 600)
    plt.close()


#-- go back to orginal directory---#
os.chdir(work_dir)




