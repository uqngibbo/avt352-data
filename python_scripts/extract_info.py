""" Extract quantities of interest such as
    - integrated values along the wall
    - separation onset
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
run_nb = 'run4'
geom_nb = "geom1"




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
    #for run4
            'starccm':{ 'mesh':'mesh08',
                    },
            'eilmer':{ 'mesh':'mesh1',
                        },
            'ansys_aselsan':{ 'mesh':'meshXX',
                        },
            'SU2':{ 'mesh':'meshVeryFine',
                        },
            'overflow':{ 'mesh':'mesh2',
                        },
    # for run6
        # 'eilmer':{ 'mesh':'mesh1',
        #             },
        # 'ansys_aselsan':{ 'mesh':'mesh4',
        #             },

        # for run 45
        # 'starccm':{ 'mesh':'mesh09',
        #             },
        # 'eilmer':{ 'mesh':'mesh1',
        #             },
        # 'ansys_aselsan':{ 'mesh':'mesh2',
        #             },
        # 'cadence':{ 'mesh':'meshXX',
        #             },
        # 'tau':{ 'mesh':'meshXX',
        #     },
        # 'coda':{ 'mesh':'meshXX',
        #         },
        # 'ansys_inc':{ 'mesh':'meshXX',
        #             },
        # # run 28
        # 'gaspex':{ 'mesh':'mesh00',
        #         },
        # 'eilmer':{ 'mesh':'mesh1',
        #     },
        # 'starccm':{ 'mesh':'mesh09',
        #             },
        # 'ansys_aselsan':{ 'mesh':'mesh03',
        #             } 
        # run 33
        # 'gaspex':{ 'mesh':'mesh00',
        #         },
        # 'eilmer':{ 'mesh':'mesh1',
        #     },
        # 'starccm':{ 'mesh':'mesh09',
        #             },
        # 'ansys_inc':{ 'mesh':'meshXX',
        #         },
        # run 14
        # 'gaspex':{ 'mesh':'mesh00',
        #         },
        # 'eilmer':{ 'mesh':'mesh1',
        #     },

        # 'starccm':{ 'mesh':'mesh09',
        #             },
        # 'ansys_inc':{ 'mesh':'meshXX',

        #             } ,
        # 'SU2':{ 'mesh':'meshVeryFine',
        #             }  

        # run 41, 37, 34
        # 'gaspex':{ 'mesh':'mesh00',
        #         },
        # 'eilmer':{ 'mesh':'mesh1',
        #     },
        # 'starccm':{ 'mesh':'mesh09',
        #             },

    #-------------------------------------------------_#
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




