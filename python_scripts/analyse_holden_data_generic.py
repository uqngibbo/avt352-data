""" Plotting the data from Holden simu
"""

import os
import glob
import numpy as np
import matplotlib.pyplot as plt
import helper_functions as helpfunc
import matplotlib.ticker as ticker

#-----------end helper functions------------------------------------------#
#-------------------------------------------------------------------------#

#-------------------------------------------------------------------------------#
#---------User selection zone-------------------------------#
ref_folder = "../refdata"
run_nb = 'run37'
geom_nb = "geom2"
code_cfd = "starccm"
ref_pressure_file = '_'.join((run_nb,"pressure.csv"))
ref_heatflux_file = '_'.join((run_nb,"heatFlux.csv"))

cfd_folder = os.path.join("..","cfddata",code_cfd,geom_nb,run_nb)

res_folder = "_".join((code_cfd,"comparison",run_nb))
work_dir = os.getcwd()



naming_dict = {}

# This dictionary is used to map internal mesh naming or turbulence naming
#       which is found in the filename. If you don't wish to use, just define it as
#       and empty dictionary
naming_dict = {
                'mesh':
                    {'mesh0':'',
                    'mesh1': 'mesh0',
                    'mesh2': '',
                    'mesh3': '',
                    'mesh4': '',
                    'mesh5': '',
                    'meshXX':'',
                    'mesh06':'mesh 1',
                    'mesh07':'mesh 2',
                    'mesh08':'mesh 3',
                    'mesh09':'mesh 4'
                    },
                'turb':
                    {'SST': 'k-$\\omega$ SST',
                    'komega06': 'k-$\\omega$ 2006'}    
            }


scaling_dict = {'wallP':1e-3,
                'wallYPlus':1,
                'skinFrictionCoeff':1,
                'wallHeatFlux':1e-6}


ylim_up_dict = {'run14': {'wallHeatFlux':0.7e6, 'noseHeatFlux':0.1e6, 'wallP':5e3},
            'run28': {'wallHeatFlux':3e6, 'wallP':20, 'noseHeatFlux':0.5e6},
            'run33': {'wallHeatFlux':0.2e6,
                        'noseHeatFlux':0.025e6,
                        'wallP':4e3
                    },
            'run34': {'wallP':10e3, 'wallHeatFlux':2.2e6,  'noseHeatFlux':0.25e6},
            'run41': {'wallP':5e3, 'wallHeatFlux':2.8e6,  'noseHeatFlux':0.25e6},
            'run45': {'wallP':20e3, 'wallHeatFlux':5.2e6,  'noseHeatFlux':0.8e6},
            'run4': {'wallP':10e3, 'wallHeatFlux':4.0e6,  'noseHeatFlux':0.2e6},
            'run37': {'wallP':3e3, 'wallHeatFlux':1.0e6,  'noseHeatFlux':0.25e6},
    }

ylim_low_dict = {
            'run14':{'wallP':0},
            'run28':{'wallP':10},
            'run33': {'wallP':2e3},
            'run34': {'wallP':2e3},
            'run41': {'wallP':0e3},
            'run45': {'wallP':10e3},
            'run4': {'wallP':0e3},
            'run37': {'wallP':2e3},
    }

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
    plt.errorbar(ref_pressure_data[:,0], ref_pressure_data[:,1]*scaling_dict[key_select],
                    fmt='o', linestyle = 'none',
                    yerr = ref_pressure_data[:,1]*3/100*scaling_dict[key_select],  elinewidth=3,
                    label='ref')
    # plt.errorbar(x, y, yerr=dy, fmt='o', color='black',
    #              ecolor='lightgray', elinewidth=3, capsize=0);


helpfunc.plot_loop_turbulence_models(cfd_data_dict[key_select], tgt_mesh,
                        naming_dict = naming_dict,
                        scale_fac = scaling_dict[key_select])

# plt.yscale('log')

# apply pre-defined, run and geometry dependent x-axis limit
helpfunc.apply_axes_limits(run_nb, geom_nb)
if geom_nb == 'geom1':
    plt.xlim([2.4,2.9])
else:
    plt.xlim([2.15,2.53])
plt.ylabel('Pressure (kPa)')
plt.legend(loc= 'upper left')
plt.tight_layout()
plt.savefig('wall_pressure.png', dpi = 600)

plt.xlim([0,1])
plt.ylim(top=ylim_up_dict[run_nb][key_select] * scaling_dict[key_select])
plt.ylim(bottom=ylim_low_dict[run_nb][key_select] * scaling_dict[key_select])
plt.savefig('wall_pressure_nose.png', dpi = 600)

# plt.show()
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
                        naming_dict = naming_dict,
                        scaling_dict = scaling_dict
                        )

# scale_y = 1e3
# ticks_y = ticker.FuncFormatter(lambda x, pos: '{0:g}'.format(x/scale_y))
# plt.axes().yaxis.set_major_formatter(ticks_y)


# ticks = plt.axes().get_yticks()/1e3
# plt.axes().set_yticklabels(ticks)

# plt.yscale('log')
# apply pre-defined, run and geometry dependent x-axis limit
helpfunc.apply_axes_limits(run_nb, geom_nb)
# #plt.xlim([2.4,2.85])
# plt.xlim(left=2.1)

# if geom_nb == 'geom1':
#     plt.xlim([2.4,2.9])
# else:
if geom_nb == 'geom2':
    plt.xlim(right=2.51)
    plt.xlim(left=2.25)
    # plt.xlim([2.15,2.53])



plt.ylabel('Pressure (kPa)')
plt.legend()
plt.tight_layout()
plt.savefig('wall_pressure_meshes.png', dpi = 600)


plt.xlim([0,1])
plt.ylim(top=ylim_up_dict[run_nb][key_select] * scaling_dict[key_select])
plt.ylim(bottom=ylim_low_dict[run_nb][key_select] * scaling_dict[key_select])

plt.savefig('wall_pressure_meshes_nose.png', dpi = 600)

plt.close()




#-------------------------------------------------------#
#--------------------------------------------------------------------#
#------Plot heatflux data for single mesh of interest----------------#
key_select = 'wallHeatFlux'
tgt_mesh = sorted(list(cfd_data_dict[key_select].keys()))[-1]
tgt_turb_list = None


#------------------------------------------------------------#
if ref_heatflux_data is not None:
    plt.errorbar(ref_heatflux_data[:,0],
                ref_heatflux_data[:,1]*scaling_dict[key_select], fmt='o', linestyle = 'none',
                        yerr=ref_heatflux_data[:,1]*5/100 *scaling_dict[key_select],
                        elinewidth=3,
                label='ref')


helpfunc.plot_loop_turbulence_models(cfd_data_dict[key_select], tgt_mesh,
                                        naming_dict = naming_dict,
                                        scale_fac = scaling_dict[key_select])


# plt.yscale('log')

# apply pre-defined, run and geometry dependent x-axis limit
helpfunc.apply_axes_limits(run_nb, geom_nb)
if geom_nb == 'geom1':
    plt.xlim([2.4,2.9])
else:
    plt.xlim([2.15,2.53])
plt.ylim(top=ylim_up_dict[run_nb][key_select] * scaling_dict[key_select])
plt.ylim(bottom=0)
plt.ylabel('Heat Flux (MW / $m^2$)')
plt.legend(loc= 'upper left')
plt.tight_layout()
plt.savefig('wall_heatflux.png', dpi = 600)

plt.xlim([0,1])
plt.ylim(top=ylim_up_dict[run_nb]['noseHeatFlux'] * scaling_dict[key_select])
plt.savefig('wall_heatflux_nose.png', dpi = 600)

plt.xlim([0,2.2])
plt.ylim(top=ylim_up_dict[run_nb]['noseHeatFlux'] * scaling_dict[key_select])
plt.savefig('wall_heatflux_nose_range2.png', dpi = 600)

plt.xlim([0,2.4])
plt.ylim(top=ylim_up_dict[run_nb]['noseHeatFlux'] * scaling_dict[key_select])
plt.savefig('wall_heatflux_nose_range3.png', dpi = 600)

plt.close()


#-------------------------------------------------------#
#--------------------------------------------------------------------#
#------Plot heatflux data for all meshes of interest----------------#
#-----------user def zone------------#
tgt_mesh_list = None
tgt_turb_list = ['SST']
key_select = 'wallHeatFlux'
#------end user def zone------------#


helpfunc.plot_mesh_loop(cfd_data_dict, key_select,
                        tgt_mesh_list, tgt_turb_list = tgt_turb_list,
                        naming_dict = naming_dict,
                        scaling_dict = scaling_dict
                    )

# apply pre-defined, run and geometry dependent x-axis limit
# helpfunc.apply_axes_limits(run_nb, geom_nb)
# plt.xlim([2.2,2.5])
# plt.yscale('log')
helpfunc.apply_axes_limits(run_nb, geom_nb)
# #plt.xlim([2.4,2.85])
# plt.xlim(left=2.1)
if geom_nb == 'geom2':
    plt.xlim(right=2.51)
    plt.xlim(left=2.25)

plt.ylim(top=ylim_up_dict[run_nb][key_select] * scaling_dict[key_select])
# plt.ylim([0, 6.5e6])
plt.ylabel('Heat Flux (MW / $m^2$)')
plt.tight_layout()
plt.legend(loc='upper left')
plt.savefig('wall_heatflux_meshes.png', dpi = 600)

plt.xlim([0,1])
plt.ylim(top=ylim_up_dict[run_nb]['noseHeatFlux'] * scaling_dict[key_select])
plt.ylim(bottom=0)
plt.legend(loc='upper left')
plt.savefig('wall_heatflux_meshes_nose.png', dpi = 600)

plt.close()


#-------------------------------------------------------#
#--------------------------------------------------------------------#
#------Plot yplus data for all meshes of interest----------------#
flag_activate = True

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




