""" Comparing CFD data from Holden setups between participants
"""

import os
import glob
import numpy as np
import matplotlib.pyplot as plt
import helper_functions as helpfunc

solver_color_dict = {
            'starccm': 'black',
            'ansys_aselsan': 'blue',
            'eilmer': 'red',
            'cadence': 'green',
            'gaspex': 'indigo',
            'tau':'brown',
            'ansys_inc':'grey',
            'coda':'cyan',
            'SU2':'darkorange',
            'overflow': 'purple'
}

#-----------end helper functions------------------------------------------#
#-------------------------------------------------------------------------#

#-------------------------------------------------------------------------------#
#---------User selection zone-------------------------------#
ref_folder = "../refdata"
run_nb = 'run4'
geom_nb = "geom1"
solver_color = True
zoom_flag = False
# Defines the solvers selected, the grid and turbulence models
#   might look cumbersome at first but it's an elegant and simple solution to
#   work with all the existing code structure
parameter_matrix = {
                    # 'ansys': {  'mesh':'mesh2',
#                                 'turb_model_list': ['SST'],
#                                 'naming_dict': {'mesh': 
#                                                     {'mesh2':'Ansys Fluent'},
#                                                 'turb':
#                                                     {'SST': 'k-$\\omega$ SST'}
#                                             }
                            # },

            # for run4
                    'starccm':{ 'mesh':'mesh06',
                                'naming_dict': {'mesh':
                                                    {'mesh06': 'STAR-CCM+'},
                                                'turb':
                                                    {'SST': 'k-$\\omega$ SST'} 
                                            }
                                },
                    'eilmer':{ 'mesh':'mesh1',
                                'naming_dict': {'mesh':
                                                    {'mesh1': 'Eilmer'},
                                                'turb':
                                                    {'komega': 'Wilcox k-$\\omega$ 2006'} 
                                            }  
                                },
                    'ansys_aselsan':{ 'mesh':'mesh4',
                                'naming_dict': {'mesh':
                                                    {'mesh4': 'Ansys Fluent (Aselsan)'},
                                                'turb':
                                                    {'SST': 'k-$\\omega$ SST'} 
                                            }  
                                },
                    'SU2':{ 'mesh':'meshVeryFine',
                                'naming_dict': {'mesh':
                                                    {'meshVeryFine': 'SU2'},
                                                'turb':
                                                    {'SST': 'k-$\\omega$ SST'} 
                                            }  
                                },
                    'overflow':{ 'mesh':'meshXX',
                                'naming_dict': {'mesh':
                                                    {'meshXX': 'OVERFLOW'},
                                            }  
                                },
            # # for run 45
                    # 'starccm':{ 'mesh':'mesh08',
                    #             'naming_dict': {'mesh':
                    #                                 {'mesh08': 'STAR-CCM+'},
                    #                             'turb':
                    #                                 {'SST': 'k-$\\omega$ SST'} 
                    #                         }
                    #             },
                    # 'eilmer':{ 'mesh':'mesh1',
                    #             'naming_dict': {'mesh':
                    #                                 {'mesh1': 'Eilmer'},
                    #                             'turb':
                    #                                 {'komega': 'Wilcox k-$\\omega$ 2006'} 
                    #                         }  
                    #             },
                    # 'ansys_aselsan':{ 'mesh':'mesh2',
                    #             'naming_dict': {'mesh':
                    #                                 {'mesh2': 'Ansys Fluent (Aselsan)'},
                    #                             'turb':
                    #                                 {'SST': 'k-$\\omega$ SST'} 
                    #                         }  
                    #             },

                    # 'cadence':{ 'mesh':'meshXX',
                    #             'turb_model_list': ['SSCEARSM_Prt086Lemmon'],
                    #             'naming_dict': {'mesh':
                    #                                 {'meshXX': 'Fidelity Flow DBS'},
                    #                             'turb':
                    #                                 {'SSCEARSM_Prt086Lemmon': 'SSC-EARSM'} 
                    #                         }  
                    #             },
                    # ##--------second plot------------------------#
                    # 'tau':{ 'mesh':'meshXX',
                    #             'turb_model_list': ['Menter_SST', 'SAnegN=646308QCR=off'],
                    #             'naming_dict': {'mesh':
                    #                                 {'meshXX': 'TAU'},
                    #                             'turb':
                    #                                 {'Menter_SST': 'k-$\\omega$ SST',
                    #                                 'SAnegN=646308QCR=off': 'SA-neg'} 
                    #                         }  
                    #             },
                    # 'coda':{ 'mesh':'meshXX',
                    #             'naming_dict': {'mesh':
                    #                                 {'meshXX': 'HyperCODA'},
                    #                             'turb':
                    #                                 {'SAneg': 'SA-neg'} 
                    #                         }  
                    #             },
                    # # ##--------------------------------------------#
                    # 'ansys_inc':{ 'mesh':'meshXX',
                    #             'naming_dict': {'mesh':
                    #                                 {'meshXX': 'Ansys Fluent (Ansys Inc.)'},
                    #                             'turb':
                    #                                 {'GEKO': 'GEKO'} 
                    #                         }  
                    #             },
                    # # 'cadence':{ 'mesh':'meshXXX',
                    # #             'turb_model_list': ['SSTa10355_Prt086Lemmon','SBSLPrt086'],
                    # #             'naming_dict': {'mesh':
                    # #                                 {'meshXXX': ''},
                    # #                             'turb':
                    # #                                 {'SBSLPrt086': 'SBSL-EARSM',
                    # #                                 'SSTa10355_Prt086Lemmon': 'k-$\\omega$ SST'} 
                    # #                         }  
                    # #             },
                    # ##--------third plot------------------------#
                    # 'tau':{ 'mesh':'meshXX',
                    #             'turb_model_list': ['SSGLRRw'],
                    #             'naming_dict': {'mesh':
                    #                                 {'meshXX': 'TAU'},
                    #                             'turb':
                    #                                 {'SSGLRRw': 'SSG/LRR 2010',
                    #                                 } 
                    #                         }  
                    #             },
                    # 'cadence':{ 'mesh':'meshXX',
                    #             'turb_model_list': ['SSCEARSM_Prt086Lemmon'],
                    #             'naming_dict': {'mesh':
                    #                                 {'meshXX': 'Fidelity Flow DBS'},
                    #                             'turb':
                    #                                 {'SSCEARSM_Prt086Lemmon': 'SSC-EARSM',
                    #                                 } 
                    #                         }  
                    #             },
                    ##--------------------------------------------#
            # # run 14
            #         'gaspex':{ 'mesh':'mesh00',
            #             'naming_dict': {'mesh':
            #                                 {'mesh00': 'GASPex'},
            #                             'turb':
            #                                 {'komega06': 'Wilcox k-$\\omega$ 2006'} 
            #                         }  
            #                 },
            #         'eilmer':{ 'mesh':'mesh1',
            #                     'naming_dict': {'mesh':
            #                                         {'mesh1': 'Eilmer'},
            #                                     'turb':
            #                                         {'komega': 'Wilcox k-$\\omega$ 2006'},
            #                     }
            #             },

            #         'starccm':{ 'mesh':'mesh08',
            #                     'naming_dict': {'mesh':
            #                                         {'mesh08': 'STAR-CCM+'},
            #                                     'turb':
            #                                         {'SST': 'k-$\\omega$ SST'} 
            #                                 }
            #                     },
            #         'ansys_inc':{ 'mesh':'meshXX',
            #                     'naming_dict': {'mesh':
            #                                         {'meshXX': 'Ansys Fluent (Ansys Inc.)'},
            #                                     'turb':
            #                                         {'GEKO': 'GEKO'} 
            #                                 }
            #                     } ,
                    # 'SU2':{ 'mesh':'meshVeryFine',
                    #             'naming_dict': {'mesh':
                    #                                 {'meshVeryFine': 'SU2'},
                    #                             'turb':
                    #                                 {'SST': 'k-$\\omega$ SST'} 
                    #                         }
                    #             }  
                }


ref_pressure_file = '_'.join((run_nb,"pressure.csv"))
ref_heatflux_file = '_'.join((run_nb,"heatFlux.csv"))


res_folder = "_".join(("comparison",run_nb))
if zoom_flag:
    res_folder = res_folder.replace('comparison','comparison_nose')
work_dir = os.getcwd()

#-------------------------------------------------------------------------------#
#-------------------------------------------------------------------------------#

ref_pressure_data, ref_heatflux_data = helpfunc.load_experimental_data(ref_folder,
                                                ref_pressure_file,
                                                ref_heatflux_file
                                            )


# Load all the data based on parameter_matrix dict into 

global_data_dict = {}
for ind, key in enumerate(parameter_matrix.keys()):
    cfd_folder = os.path.join("..","cfddata", key, geom_nb,run_nb)
    cfd_data_filenames = helpfunc.filter_cfd_data_filenames(glob.glob(cfd_folder+"/*"))
    cfd_data_dict = helpfunc.create_cfddatadict_for_solver(key, cfd_data_filenames)
    helpfunc.sort_data_dict_based_on_column(cfd_data_dict,0)
    global_data_dict[key] = cfd_data_dict


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

#--------------------------------#

if ref_pressure_data is not None:
    # plt.plot(ref_pressure_data[:,0], ref_pressure_data[:,1], linestyle = 'none', marker = 'o')
    plt.errorbar(ref_pressure_data[:,0], ref_pressure_data[:,1],
                    fmt='o', linestyle = 'none',
                    yerr = ref_pressure_data[:,1]*3/100,  elinewidth=3,
                    label='ref')
    # plt.errorbar(x, y, yerr=dy, fmt='o', color='black',
    #              ecolor='lightgray', elinewidth=3, capsize=0);


for ind, cfdcode in enumerate(parameter_matrix.keys()):

    tgt_turb_list = None
    try:
        tgt_turb_list = parameter_matrix[cfdcode]['turb_model_list']
    except KeyError:
        pass

    naming_dict = {}
    try:
        naming_dict = parameter_matrix[cfdcode]['naming_dict']
    except KeyError:
        pass

    # NOTE: currently assumes single mesh for results, if different mesh for different
    #           turbulence model we'll need to handle -> loop through grids then! in list
    solver_specific_color = solver_color_dict[cfdcode]
    if not solver_color:
        solver_specific_color = None
    helpfunc.plot_loop_turbulence_models(global_data_dict[cfdcode][key_select],
                            parameter_matrix[cfdcode]['mesh'],
                            tgt_turb_list = tgt_turb_list,
                            naming_dict = naming_dict,
                            user_color = solver_specific_color
                            )

# plt.yscale('log')

# apply pre-defined, run and geometry dependent x-axis limit
helpfunc.apply_axes_limits(run_nb, geom_nb)
# plt.xlim([2.4,2.88])

if zoom_flag:
    plt.xlim([0,2])
    plt.ylim(top=1.8e4)
    plt.ylim(bottom=1.4e4)

plt.ylabel('Pressure (Pa)')
plt.tight_layout()
plt.legend(fontsize = 8,loc = 'upper left')
plt.savefig('wall_pressure.png', dpi = 300)
plt.show()
plt.close()




#-------------------------------------------------------#
#--------------------------------------------------------------------#
#------Plot heatflux data for single mesh of interest----------------#
key_select = 'wallHeatFlux'


#------------------------------------------------------------#
if ref_heatflux_data is not None:
    plt.errorbar(ref_heatflux_data[:,0], ref_heatflux_data[:,1], fmt='o', linestyle = 'none',
                        yerr=ref_heatflux_data[:,1]*5/100,  elinewidth=3,
                label='ref')

for ind, cfdcode in enumerate(parameter_matrix.keys()):

    tgt_turb_list = None
    try:
        tgt_turb_list = parameter_matrix[cfdcode]['turb_model_list']
    except KeyError:
        pass

    naming_dict = {}
    try:
        naming_dict = parameter_matrix[cfdcode]['naming_dict']
    except KeyError:
        pass

    # NOTE: currently assumes single mesh for results, if different mesh for different
    #           turbulence model we'll need to handle -> loop through grids then! in list
    solver_specific_color = solver_color_dict[cfdcode]
    if not solver_color:
        solver_specific_color = None

    helpfunc.plot_loop_turbulence_models(global_data_dict[cfdcode][key_select],
                            parameter_matrix[cfdcode]['mesh'],
                            tgt_turb_list = tgt_turb_list,
                            naming_dict = naming_dict,
                            user_color = solver_specific_color)


# plt.yscale('log')

# apply pre-defined, run and geometry dependent x-axis limit
helpfunc.apply_axes_limits(run_nb, geom_nb)
if run_nb == 'run14':
    plt.ylim(top = 1e6)
if run_nb == 'run45':
    plt.ylim(top = 6.5e6)
if run_nb == 'run4':
    plt.ylim(top = 5e6)
    plt.ylim(bottom = -1e3)

if zoom_flag:
    plt.xlim([0,2])
    plt.ylim(top = 1e6)
    plt.ylim(bottom = 0e6)
plt.ylabel('Heat Flux (W / $m^2$)')

plt.tight_layout()

plt.legend(fontsize = 8,loc = 'upper left')
if zoom_flag:
    plt.legend(fontsize = 8,loc = 'upper right')

plt.savefig('wall_heatflux.png', dpi = 300)
plt.close()




#-- go back to orginal directory---#
os.chdir(work_dir)




