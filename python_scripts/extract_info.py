""" Extract quantities of interest such as
    - integrated values along the wall
    - separation onset
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

ylim_up_dict = {'run14': {'wallHeatFlux':0.7e6, 'noseHeatFlux':0.1e6, 'wallP':5e3},
            'run28': {'wallHeatFlux':3e6, 'wallP':20e3, 'noseHeatFlux':0.5e6},
            'run33': {'wallHeatFlux':0.2e6,
                        'noseHeatFlux':0.025e6,
                        'wallP':4e3
                    },
            'run34': {'wallP':10e3, 'wallHeatFlux':2.4e6,  'noseHeatFlux':0.25e6},
            'run41': {'wallP':5e3, 'wallHeatFlux':3.6e6,  'noseHeatFlux':0.25e6},
            'run45': {'wallP':20e3, 'wallHeatFlux':5.2e6,  'noseHeatFlux':0.8e6},
            'run4': {'wallP':10e3, 'wallHeatFlux':4.0e6,  'noseHeatFlux':0.4e6},
            'run6': {'wallP':10e3, 'wallHeatFlux':7.5e6,  'noseHeatFlux':0.4e6},
            'run37': {'wallP':250e3, 'wallHeatFlux':1.0e6,  'noseHeatFlux':0.15e6},
    }

#   for the lower y limits
ylim_low_dict = {
            'run14':{'wallP':0},
            'run28':{'wallP':10e3},
            'run33': {'wallP':2e3},
            'run34': {'wallP':2e3},
            'run41': {'wallP':0e3},
            'run45': {'wallP':10e3},
            'run4': {'wallP':0e3},
            'run37': {'wallP':2e3},
            'run6': {'wallP':0e3},
    }

#-----------end helper functions------------------------------------------#
#-------------------------------------------------------------------------#

#-------------------------------------------------------------------------------#
#---------User selection zone-------------------------------#
ref_folder = "../refdata"
run_nb = 'run37'
geom_nb = "geom2"
solver_color = True



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
            # 'ansys_aselsan':{ 'mesh':'meshXX',
            #                 'turb_model_list': ['SST1T','SA1T'],

            #             'naming_dict': {'mesh':
            #                                 {'meshXX': 'Ansys Fluent (Aselsan)'},
            #                             'turb':
            #                                 {'SST1T': 'k-$\\omega$ SST',
            #                                 'SA1T': 'SA'} 
            #                         }
            #             },
            # 'SU2':{ 'mesh':'meshVeryFine',
            #             'naming_dict': {'mesh':
            #                                 {'meshVeryFine': 'SU2'},
            #                             'turb':
            #                                 {'SST': 'k-$\\omega$ SST'} 
            #                         }  
            #             },
            # 'overflow':{ 'mesh':'mesh2',
            #             'naming_dict': {'mesh':
            #                                 {'mesh2': 'OVERFLOW'},
            #                             'turb':
            #                                 {'SST': 'k-$\\omega$ SST'}
            #                         } 
            #             },
    # for run6
            # 'eilmer':{ 'mesh':'mesh1',
            #             'naming_dict': {'mesh':
            #                                 {'mesh1': 'Eilmer'},
            #                             'turb':
            #                                 {'komega': 'Wilcox k-$\\omega$ 2006'} 
            #                         }  
            #             },
            # 'ansys_aselsan':{ 'mesh':'mesh4',
            #                 # 'turb_model_list': ['SST','SA1T'],

            #             'naming_dict': {'mesh':
            #                                 {'mesh4': 'Ansys Fluent (Aselsan)'},
            #                             'turb':
            #                                 {'SST1T': 'k-$\\omega$ SST',
            #                                 'SA1T': 'SA',
            #                                  'SST':'k-$\\omega$ SST'} 
            #                         }
            #             },

            # for run 45
                    # 'starccm':{ 'mesh':'mesh09',
                    #             'naming_dict': {'mesh':
                    #                                 {'mesh09': 'STAR-CCM+'},
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
        # run 28
                # 'gaspex':{ 'mesh':'mesh00',
                #     'naming_dict': {'mesh':
                #                         {'mesh00': 'GASPex'},
                #                     'turb':
                #                         {'komega06': 'Wilcox k-$\\omega$ 2006'} 
                #                 }  
                #         },
                # 'eilmer':{ 'mesh':'mesh1',
                #             'naming_dict': {'mesh':
                #                                 {'mesh1': 'Eilmer'},
                #                             'turb':
                #                                 {'komega': 'Wilcox k-$\\omega$ 2006'},
                #             }
                #     },
                # 'starccm':{ 'mesh':'mesh09',
                #             'naming_dict': {'mesh':
                #                                 {'mesh09': 'STAR-CCM+'},
                #                             'turb':
                #                                 {'SST': 'k-$\\omega$ SST'} 
                #                         }
                #             },
                # 'ansys_aselsan':{ 'mesh':'mesh03',
                #                 'turb_model_list': ['SSTa1coeff031','SSTa1coeff0355'],
                #             'naming_dict': {'mesh':
                #                                 {'mesh03': 'Ansys Fluent (Aselsan)'},
                #                             'turb':
                #                                 {'SSTa1coeff031': 'k-$\\omega$ SST \n a1 = 0.31',
                #                                 'SSTa1coeff0355': 'k-$\\omega$ SST \n a1 = 0.355'} 
                #                         }
                #             } 
        # run 34
        # 'gaspex':{ 'mesh':'mesh00',
        #     'naming_dict': {'mesh':
        #                         {'mesh00': 'GASPex'},
        #                     'turb':
        #                         {'komega06': 'Wilcox k-$\\omega$ 2006'} 
        #                 }  
        #         },
        # 'eilmer':{ 'mesh':'mesh1',
        #             'naming_dict': {'mesh':
        #                                 {'mesh1': 'Eilmer'},
        #                             'turb':
        #                                 {'komega': 'Wilcox k-$\\omega$ 2006'},
        #             }
        #     },
        # 'starccm':{ 'mesh':'mesh09',
        #             'naming_dict': {'mesh':
        #                                 {'mesh09': 'STAR-CCM+'},
        #                             'turb':
        #                                 {'SST': 'k-$\\omega$ SST'} 
        #                         }
        #             },
        # run 33
        # 'gaspex':{ 'mesh':'mesh00',
        #     'naming_dict': {'mesh':
        #                         {'mesh00': 'GASPex'},
        #                     'turb':
        #                         {'komega06': 'Wilcox k-$\\omega$ 2006'} 
        #                 }  
        #         },
        # 'eilmer':{ 'mesh':'mesh1',
        #             'naming_dict': {'mesh':
        #                                 {'mesh1': 'Eilmer'},
        #                             'turb':
        #                                 {'komega': 'Wilcox k-$\\omega$ 2006'},
        #             }
        #     },
        # 'starccm':{ 'mesh':'mesh09',
        #             'naming_dict': {'mesh':
        #                                 {'mesh09': 'STAR-CCM+'},
        #                             'turb':
        #                                 {'SST': 'k-$\\omega$ SST'} 
        #                         }
        #             },
        # 'ansys_inc':{ 'mesh':'meshXX',
        #         'naming_dict': {'mesh':
        #                             {'meshXX': 'Ansys Fluent (Ansys Inc.)'},
        #                         'turb':
        #                             {'GEKO': 'GEKO'} 
        #                     }  
        #         },
            # # run 14
            # 'gaspex':{ 'mesh':'mesh00',
            #     'naming_dict': {'mesh':
            #                         {'mesh00': 'GASPex'},
            #                     'turb':
            #                         {'komega06': 'Wilcox k-$\\omega$ 2006'} 
            #                 }  
            #         },
            # 'eilmer':{ 'mesh':'mesh1',
            #             'naming_dict': {'mesh':
            #                                 {'mesh1': 'Eilmer'},
            #                             'turb':
            #                                 {'komega': 'Wilcox k-$\\omega$ 2006'},
            #             }
            #     },

            # 'starccm':{ 'mesh':'mesh09',
            #             'naming_dict': {'mesh':
            #                                 {'mesh09': 'STAR-CCM+'},
            #                             'turb':
            #                                 {'SST': 'k-$\\omega$ SST'} 
            #                         }
            #             },
            # 'ansys_inc':{ 'mesh':'meshXX',
            #             'naming_dict': {'mesh':
            #                                 {'meshXX': 'Ansys Fluent (Ansys Inc.)'},
            #                             'turb':
            #                                 {'GEKO': 'GEKO'} 
            #                         }
            #             } ,
            # 'SU2':{ 'mesh':'meshVeryFine',
            #             'naming_dict': {'mesh':
            #                                 {'meshVeryFine': 'SU2'},
            #                             'turb':
            #                                 {'SST': 'k-$\\omega$ SST'} 
            #                         }
            #             }  
        # run 41, 37
        'gaspex':{ 'mesh':'mesh00',
                },
        'eilmer':{ 'mesh':'mesh1',
            },
        'starccm':{ 'mesh':'mesh09',
                    },
        }


res_folder = "_".join(("comparison",run_nb))

work_dir = os.getcwd()

#-------------------------------------------------------------------------------#
#-------------------------------------------------------------------------------#

# Load all the data based on parameter_matrix dict into, only uses the first keys of the
#   nested dict, i.e. solvers info
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

# Reduce the global cfd data dict in accordance to the parameter matrix
#   NOTE: a unique mesh key should be present in the parameter matrix
reduced_dict = helpfunc.filter_global_dict_based_on_parameters(global_data_dict,
                                                        parameter_matrix,
                                                        geom_nb)


integrated_dict = helpfunc.compute_integral_quantities(reduced_dict)

# Get latex table, NOTE: print it and copy in latex
latex_table = helpfunc.create_latex_table_integrated(integrated_dict, run_nb)
print(latex_table)

#-- go back to orginal directory---#
os.chdir(work_dir)




