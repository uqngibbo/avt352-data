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
            'overflow': 'violet',
            'vulcan': 'gold',
            'h3amr': 'hotpink'
}


ylim_up_dict = {'run14': {'wallHeatFlux':0.7e6, 'noseHeatFlux':0.1e6, 'wallP':5e3},
            'run28': {'wallHeatFlux':3e6, 'wallP':20e3, 'noseHeatFlux':0.5e6},
            'run33': {'wallHeatFlux':0.2e6,
                        'noseHeatFlux':0.025e6,
                        'wallP':4e3
                    },
            'run34': {'wallP':10e3, 'wallHeatFlux':2.4e6,  'noseHeatFlux':0.35e6},
            'run41': {'wallP':5e3, 'wallHeatFlux':3.6e6,  'noseHeatFlux':0.25e6},
            'run45': {'wallP':20e3, 'wallHeatFlux':5.2e6,  'noseHeatFlux':0.9e6},
            'run4': {'wallP':10e3, 'wallHeatFlux':4.5e6,  'noseHeatFlux':0.4e6},
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
run_nb = 'run45'
geom_nb = "geom2"
solver_color = True
zoom_flag = False # If true, focus on nose cone region
with_frame_legend = False

extra_folder_name = None
# extra_folder_name = #'aselsan'
legend_fontsize = 9
plt.rcParams.update({'font.size': 16})

scale_fac_dict = {'wallP': 1e-3, 'wallHeatFlux':1e-6, 'noseHeatFlux':1e-6}

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
            #                 # 'turb_model_list': ['SST1T','SA1T'],
            #                 'turb_model_list': ['SST1T','SA1T', 'SST2T','SA2T'],
            #             'naming_dict': {'mesh':
            #                                 {'meshXX': 'Ansys Fluent (Aselsan)'},
            #                             # 'turb':
            #                             #     {'SST1T': 'k-$\\omega$ SST 1-T',
            #                             #     'SA1T': 'SA 1-T',
            #                             #     'SST2T': 'k-$\\omega$ SST 2-T',
            #                             #     'SA2T': 'SA 2-T'
            #                             #     } 
            #                         }
            #             },
            # 'SU2':{ 'mesh':'meshXX',
            #             'turb_model_list': ['SST'],
            #             'naming_dict': {'mesh':
            #                                 {'meshXX': 'SU2',
            #                                 'mesh05': 'SU2',
            #                                 'mesh04': 'SU2'},
            #                             'turb':
            #                                 {'SST': 'k-$\\omega$ SST'} 
            #                         }  
            #             },
            # 'overflow':{ 'mesh':'mesh3',
            #             'turb_model_list': ['SST'],
            #             'naming_dict': {'mesh':
            #                                 {'mesh2': 'OVERFLOW',
            #                                 'mesh3': 'OVERFLOW'},
            #                             'turb':
            #                                 {'SST': 'k-$\\omega$ SST'}
            #                         } 
            #             },
            # 'vulcan':{ 'mesh':'meshXX',
            #             'turb_model_list': #['SST','SSTKL', 'SSTV'],
            #                             # ['SSTV','SSTVnorhok'],
            #                             ['SSTV','SA'],
            #                             # ['SA', 'SAQCRV'],
            #             'naming_dict': {'mesh':
            #                                 {'meshXX': 'VULCAN'},
            #                             'turb':
            #                                 {'SST': 'Menter-SST',
            #                                 # 'SAQCRV': 'SA 2013 QCR-V',
            #                                 'SSTKL':'Menter-SST-KL',
            #                                 'SSTV':'Menter-SST-V',
            #                                 'SSTVnorhok':'Menter-SST-V (no 2/3 $\\rho k$)',
            #                                 'SA':'SA-noft2',
            #                                 'SAQCRV': 'SA-noft2-QCR-V',
            #                                 } 
            #                         }  
            #             },
            # 'cadence':{ 'mesh':'meshXX',
            #             # 'turb_model_list': ['SSCEARSM_Prt086Lemmon'],
            #             'naming_dict': {'mesh':
            #                                 {'meshXX': 'Fidelity Flow DBS'},
            #                             'turb':
            #                                 {'SSCEARSM_Prt086Lemmon_LDFSS': 'SSC-EARSM',
            #                                 'SSTa10355_Prt086Lemmon': 'k-$\\omega$ SST',
            #                                 'SSTa10355_Prt086Lemmon_LDFSS':'k-$\\omega$ SST a1=0.355'} 
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
            # 'cadence':{ 'mesh':'meshXX',
            #             # 'turb_model_list': ['SSCEARSM_Prt086Lemmon'],
            #             'naming_dict': {'mesh':
            #                                 {'meshXX': 'Fidelity Flow DBS'},
            #                             'turb':
            #                                 {'SSCEARSM_Prt086Lemmon_LDFSS': 'SSC-EARSM',
            #                                 'SSTa10355_Prt086Lemmon_LDFSS': 'k-$\\omega$ SST $a_1$=0.355'} 
            #                         }  
            #             },
            # # for run 45
                        # 'vulcan':{ 'mesh':'meshXX',
                        # 'turb_model_list': 
                        #                 ['SST','SSTKL', 'SSTV'],
                        #                 # ['SSTV','SSTVnorhok'],
                        #                 # ['SA', 'SAQCRV'],
                        # 'naming_dict': {'mesh':
                        #                     {'meshXX': ''},
                        #                 'turb':
                        #                     {'SST': 'Menter-SST',
                        #                     # 'SAQCRV': 'SA 2013 QCR-V',
                        #                     'SSTKL':'Menter-SST-KL',
                        #                     'SSTV':'Menter-SST-V',
                        #                     'SSTVnorhok':'Menter-SST-V (no 2/3 $\\rho k)$',
                        #                     'SA':'SA-noft2',
                        #                     'SAQCRV': 'SA-noft2-QCR-V',
                        #                     } 
                        #             }  
                        # },
            #         'starccm':{ 'mesh':'mesh09',
            #                     'naming_dict': {'mesh':
            #                                         {'mesh09': 'STAR-CCM+'},
            #                                     'turb':
            #                                         {'SST': 'k-$\\omega$ SST'} 
            #                                 }
            #                     },
            #         'eilmer':{ 'mesh':'mesh1',
            #                     'naming_dict': {'mesh':
            #                                         {'mesh1': 'Eilmer'},
            #                                     'turb':
            #                                         {'komega': 'Wilcox k-$\\omega$ 2006'} 
            #                                 }  
            #                     },
            #         'ansys_aselsan':{ 'mesh':'mesh2',
            #                     'naming_dict': {'mesh':
            #                                         {'mesh2': 'Ansys Fluent (Aselsan)'},
            #                                     'turb':
            #                                         {'SST': 'k-$\\omega$ SST'} 
            #                                 }  
            #                     },
            #         'vulcan':{ 'mesh':'meshXX',
            #                     # 'turb_model_list': ['SST'],
            #                     'turb_model_list': ['SST', 'SAQCRV'],
            #                     'naming_dict': {'mesh':
            #                                         {'meshXX': 'VULCAN'},
            #                                     'turb':
            #                                         {'SST': 'k-$\\omega$ SST',
            #                                         'SAQCRV': 'SA 2013 QCR-V'} 
            #                                 }  
            #                     },

            #         'cadence':{ 'mesh':'meshXX',
            #                     # 'turb_model_list': ['SSCEARSM_Prt086Lemmon'],
            #                     'naming_dict': {'mesh':
            #                                         {'meshXX': 'Fidelity Flow DBS'},
            #                                     'turb':
            #                                         {'SSCEARSM_Prt086Lemmon_LDFSS': 'SSC-EARSM',
            #                                 'SSTa10355_Prt086Lemmon': 'k-$\\omega$ SST',
            #                                 'SSTa10355_Prt086Lemmon_LDFSS':'k-$\\omega$ SST a1=0.355',
            #                                 'SSTa10355': 'k-$\\omega$ SST a1=0.355'}  
            #                                 }  
            #                     },
            #         'SU2':{ 'mesh':'meshXX',
            #             'naming_dict': {'mesh':
            #                                 {'meshXX': 'SU2',
            #                                 'mesh05': 'SU2',
            #                                 'mesh03': 'SU2'},
            #                             'turb':
            #                                 {'SST': 'k-$\\omega$ SST'} 
            #                         }
            #             },
            #         'overflow':{ 'mesh':'meshXX',
            #                     'turb_model_list': ['SST'],
            #                     'naming_dict': {'mesh':
            #                                         {'mesh2': 'OVERFLOW',
            #                                         'meshXX': 'OVERFLOW'},
            #                                     'turb':
            #                                         {'SST': 'k-$\\omega$ SST'}
            #                                 } 
            #                     },
            # # #         # # ##--------second plot------------------------#
            #         'tau':{ 'mesh':'meshXX',
            #                     'turb_model_list': ['SST2003', 'SAneg','SSGLRRw2010'],
            #                     'naming_dict': {'mesh':
            #                                         {'meshXX': 'TAU'},
            #                                     'turb':
            #                                         {'SST2003': 'k-$\\omega$ SST',
            #                                         'SAneg': 'SA-neg',
            #                                         'SSGLRRw2010':helpfunc.obtain_mapping_dict()['SSGLRRw2010']} 
            #                                 }  
            #                     },
            #         'coda':{ 'mesh':'meshXX',
            #                     'naming_dict': {'mesh':
            #                                         {'meshXX': 'HyperCODA'},
            #                                     'turb':
            #                                         {'SAneg': 'SA-neg'} 
            #                                 }  
            #                     },
            # # #         # # # ##--------------------------------------------#
            #         'ansys_inc':{ 'mesh':'meshXX',
            #                     'naming_dict': {'mesh':
            #                                         {'meshXX': 'Ansys Fluent (Ansys Inc.)'},
            #                                     'turb':
            #                                         {'GEKO': 'GEKO'} 
            #                                 }  
            #                     },
                    ##---------SA only plots--------------------------#
                        # 'vulcan':{ 'mesh':'meshXX',
                        #     'turb_model_list': 
                        #                     ['SA', 'SAQCRV'],
                        #     'naming_dict': {'mesh':
                        #                         {'meshXX': 'VULCAN\n'},
                        #                     'turb':
                        #                         {'SST': 'Menter-SST',
                        #                         # 'SAQCRV': 'SA 2013 QCR-V',
                        #                         'SSTKL':'Menter-SST-KL',
                        #                         'SSTV':'Menter-SST-V',
                        #                         'SSTVnorhok':'Menter-SST-V (no 2/3 $\\rho k)$',
                        #                         'SA':'SA-noft2',
                        #                         'SAQCRV': 'SA-noft2-QCR-V',
                        #                         } 
                        #                 }  
                        # },
                        # 'tau':{ 'mesh':'meshXX',
                        #     'turb_model_list': ['SAneg','SAO'],
                        #     'naming_dict': {'mesh':
                        #                         {'meshXX': 'TAU\n'},
                        #                     'turb':
                        #                         {'SST2003': 'k-$\\omega$ SST',
                        #                         'SAneg': 'SA-neg',
                        #                         'SSGLRRw2010':helpfunc.obtain_mapping_dict()['SSGLRRw2010'],
                        #                         'SAO':helpfunc.obtain_mapping_dict()['SAO']
                        #                     } 
                        #                 }  
                        # },
                        # 'coda':{ 'mesh':'meshXX',
                        #         'naming_dict': {'mesh':
                        #                            {'meshXX': 'HyperCODA\n'},
                        #                         'turb':
                        #                             {'SAneg': 'SA-neg'} 
                        #                     }  
                        #         },
                        # 'overflow':{ 'mesh':'meshXX',
                        #             'turb_model_list': ['SA'],
                        #             'naming_dict': {'mesh':
                        #                                 {'mesh2': 'OVERFLOW',
                        #                                 'meshXX': 'OVERFLOW'},
                        #                             'turb':
                        #                                 {'SST': 'k-$\\omega$ SST'}
                        #                         } 
                        #             },
                    #  ##---------2-eq only plots--------------------------#
                    #  'starccm':{ 'mesh':'mesh09',
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
                    #                                 {'mesh2': 'Ansys Fluent (Aselsan)\n'},
                    #                             'turb':
                    #                                 {'SST': 'k-$\\omega$ SST'} 
                    #                         }  
                    #             },
                    # 'vulcan':{ 'mesh':'meshXX',
                    #             # 'turb_model_list': ['SST'],
                    #             'turb_model_list': ['SST'],
                    #             'naming_dict': {'mesh':
                    #                                 {'meshXX': 'VULCAN'},
                    #                             'turb':
                    #                                 {'SST': 'k-$\\omega$ SST',
                    #                                 'SAQCRV': 'SA 2013 QCR-V'} 
                    #                         }  
                    #             },
                    # 'ansys_inc':{ 'mesh':'meshXX',
                    #             'naming_dict': {'mesh':
                    #                                 {'meshXX': 'Ansys Fluent (Ansys Inc.)\n'},
                    #                             'turb':
                    #                                 {'GEKO': 'GEKO'} 
                    #                         }  
                    #             },
                    # 'cadence':{ 'mesh':'meshXX',
                    #             'turb_model_list': ['SSTa10355'],
                    #             'naming_dict': {'mesh':
                    #                                 {'meshXX': 'Fidelity Flow DBS \n'},
                    #                             'turb':
                    #                                 {'SSCEARSM_Prt086Lemmon': 'SSC-EARSM',
                    #                                 'SSCEARSM_Prt086Lemmon_LDFSS': 'SSC-EARSM',
                    #                                 'SSTa10355': 'k-$\\omega$ SST $a_1$=0.355' 
                    #                                 } 
                    #                         }  
                    #             },
                    # 'SU2':{ 'mesh':'meshXX',
                    #     'naming_dict': {'mesh':
                    #                         {'meshXX': 'SU2',
                    #                         'mesh05': 'SU2',
                    #                         'mesh03': 'SU2'},
                    #                     'turb':
                    #                         {'SST': 'k-$\\omega$ SST'} 
                    #                 }
                    #     },
                    # 'overflow':{ 'mesh':'meshXX',
                    #             'turb_model_list': ['SST'],
                    #             'naming_dict': {'mesh':
                    #                                 {'mesh2': 'OVERFLOW',
                    #                                 'meshXX': 'OVERFLOW'},
                    #                             'turb':
                    #                                 {'SST': 'k-$\\omega$ SST'}
                    #                         } 
                    #             },
                    #     'tau':{ 'mesh':'meshXX',
                    #         'turb_model_list': ['SST2003'],
                    #         'naming_dict': {'mesh':
                    #                             {'meshXX': 'TAU'},
                    #                         'turb':
                    #                             {'SST2003': 'k-$\\omega$ SST',
                    #                             'SAneg': 'SA-neg',
                    #                             'SSGLRRw2010':helpfunc.obtain_mapping_dict()['SSGLRRw2010']} 
                    #                     }  
                    #     },     
                    ##---------TAU only 1eq , 2 eq--------------------------#  
                        'tau':{ 'mesh':'meshXX',
                            'turb_model_list': ['wilcox+SST', 'SAO', 'SST2003', 
                                            'komegaMenterBSL', 'SAneg', 'komegaWilcox'],
                            'naming_dict': {'mesh':
                                                {'meshXX': ''},
                                            'turb':
                                                {'SST2003': 'k-$\\omega$ SST',
                                                'SAneg': 'SA-neg',
                                                'SAO': 'SA-noft2',
                                                'SSGLRRw2010':helpfunc.obtain_mapping_dict()['SSGLRRw2010'],
                                                'wilcox+SST':helpfunc.obtain_mapping_dict()['wilcox+SST'],
                                                'komegaMenterBSL':helpfunc.obtain_mapping_dict()['komegaMenterBSL'],
                                                'wilcox+SST':helpfunc.obtain_mapping_dict()['wilcox+SST'],
                                                'komegaWilcox':helpfunc.obtain_mapping_dict()['komegaWilcox'],
                                                } 
                                        }  
                        },                  
                      ##---------EARSM / RSM only plots--------------------------#
                    # 'cadence':{ 'mesh':'meshXX',
                    #             'turb_model_list': ['SSCEARSM_Prt086Lemmon_LDFSS'],
                    #             'naming_dict': {'mesh':
                    #                                 {'meshXX': 'Fidelity Flow DBS \n'},
                    #                             'turb':
                    #                                 {'SSCEARSM_Prt086Lemmon': 'SSC-EARSM',
                    #                                 'SSCEARSM_Prt086Lemmon_LDFSS': 'SSC-EARSM',
                    #                                 'SSTa10355': 'k-$\\omega$ SST $a_1$=0.355' 
                    #                                 } 
                    #                         }  
                    #             },
                        # 'tau':{ 'mesh':'meshXX',
                        #     'turb_model_list': ['SSGLRRw2010', 'EARSMWJ3DTNT',
                        #                             'EARSMWJHellsten','WilcoxRSM2010'],
                        #     'naming_dict': {'mesh':
                        #                         # {'meshXX': 'TAU \n'},
                        #                          {'meshXX': ''},
                        #                     'turb':
                        #                         {'SST2003': 'k-$\\omega$ SST',
                        #                         'SAneg': 'SA-neg',
                        #                         'SSGLRRw2010':helpfunc.obtain_mapping_dict()['SSGLRRw2010'],
                        #                         'EARSMWJ3DTNT':helpfunc.obtain_mapping_dict()['EARSMWJ3DTNT'],
                        #                         'EARSMWJHellsten':helpfunc.obtain_mapping_dict()['EARSMWJHellsten'],
                        #                         'WilcoxRSM2010':helpfunc.obtain_mapping_dict()['WilcoxRSM2010'],                                                
                        #                     } 
                        #                 }  
                        # },  
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
                #                 'turb_model_list': 
                #                         # ['SSTa1coeff031','SST2Ta1coeff031'],
                #                         ['SSTa1coeff031','SSTa1coeff0355'],
                #             'naming_dict': {'mesh':
                #                                 {'mesh03': 'Ansys Fluent (Aselsan) \n'},
                #                             'turb':
                #                                 {
                #                             'SSTa1coeff031': 'k-$\\omega$ SST \n a1 = 0.31',
                #                             'SSTa1coeff0355': 'k-$\\omega$ SST \n a1 = 0.355',
                #                             # 'SST2Ta1coeff031': 'SST2T',
                #                             # 'SSTa1coeff031': 'SST1T'
                #                             } 
                #                         }
                #             },
                # 'SU2':{ 'mesh':'meshXX',
                #         'naming_dict': {'mesh':
                #                             {'meshXX': 'SU2',
                #                             'mesh05':'SU2' },
                #                         'turb':
                #                             {'SST': 'k-$\\omega$ SST'} 
                #                     }
                #         }

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
        # 'SU2':{ 'mesh':'meshXX',
        #         'naming_dict': {'mesh':
        #                             {'meshXX': 'SU2'},
        #                         'turb':
        #                             {'SST': 'k-$\\omega$ SST'} 
        #                     }
        #         }
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
        # 'SU2':{ 'mesh':'meshXX',
        #         'naming_dict': {'mesh':
        #                             {'meshXX': 'SU2',
        #                             'mesh05': 'SU2'},
        #                         'turb':
        #                             {'SST': 'k-$\\omega$ SST'} 
        #                     }
        #         },
        # 'h3amr':{ 'mesh':'meshXX',
        #         'naming_dict': {'mesh':
        #                             {'meshXX': 'H3AMR'},
        #                         # 'turb':
        #                         #     {'SA': 'k-$\\omega$ SST'} 
        #                     }
        #         }
            # run 14
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
            # 'SU2':{ 'mesh':'meshXX',
            #             'naming_dict': {'mesh':
            #                                 {'meshXX': 'SU2',
            #                                 'mesh05': 'SU2'},
            #                             'turb':
            #                                 {'SST': 'k-$\\omega$ SST'} 
            #                         }
            #             }

        # # # # run 41, 37
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
        # 'SU2':{ 'mesh':'meshXX',
        #             'naming_dict': {'mesh':
        #                                 {'meshXX': 'SU2',
        #                                 'mesh05': 'SU2'},
        #                             'turb':
        #                                 {'SST': 'k-$\\omega$ SST',
        #                                 } 
        #                         }
        #             }  

}


if zoom_flag:
    try:
        del parameter_matrix['gaspex']
    except KeyError:
        pass

ref_pressure_file = '_'.join((run_nb,"pressure.csv"))
ref_heatflux_file = '_'.join((run_nb,"heatFlux.csv"))


res_folder = "_".join(("comparison",run_nb))
if zoom_flag:
    res_folder = res_folder.replace('comparison','comparison_nose')
work_dir = os.getcwd()

if extra_folder_name is not None:
    res_folder = res_folder + '_' + extra_folder_name
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
    labelplot = 'ref'
    if (zoom_flag) and (run_nb in ['run4', 'run6']):
        labelplot = '_ref'
    # plt.plot(ref_pressure_data[:,0], ref_pressure_data[:,1], linestyle = 'none', marker = 'o')
    plt.errorbar(ref_pressure_data[:,0],
                    ref_pressure_data[:,1]*scale_fac_dict[key_select],
                    fmt='o', linestyle = 'none',
                    yerr = ref_pressure_data[:,1]*3/100*scale_fac_dict[key_select],
                    elinewidth=3,
                    label=labelplot,
                    color= 'k')
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
                            user_color = solver_specific_color,
                            scale_fac = scale_fac_dict[key_select]
                            )


# ---could be used to plot the geomtry if desired, use boxplot ref but I don't think
#       needed at this point
# geom_info = helpfunc.get_geometry_information()
# # Get current axis
# ax = plt.gca()

# # Create twin axis
# ax2 = ax.twinx()
# tmp_geom = geom_info[geom_nb]
# cone_flare_x = [0,tmp_geom['cone'], tmp_geom['total']]
# cone_flare_y = [0,
#                 tmp_geom['cone']*np.sin(np.deg2rad(tmp_geom['angle_cone'])),
#                 tmp_geom['cone']*np.sin(np.deg2rad(tmp_geom['angle_cone'])) \
#                 + tmp_geom['flare']*np.sin(np.deg2rad(tmp_geom['angle_flare']))
#                 ]
# ax2.plot(cone_flare_x, cone_flare_y, linestyle = '--', color = 'lightgrey')
# ax2.set_ylabel('y (m)')
# # plt.yscale('log')

# apply pre-defined, run and geometry dependent x-axis limit
helpfunc.apply_axes_limits(run_nb, geom_nb)
# plt.xlim([2.4,2.88])

if geom_nb == 'geom2':
    plt.xlim(right=2.51)
    plt.xlim(left=2.25)

if run_nb == 'run33':
    plt.xlim(left=2.2)

if zoom_flag:
    plt.xlim([0,2])
    plt.ylim(top = ylim_up_dict[run_nb][key_select])
    plt.ylim(bottom = ylim_low_dict[run_nb][key_select])
    if run_nb in ['run4', 'run6']:
        plt.xlim([0,2.6])

plt.ylabel('Pressure (kPa)')
# plt.ylabel('Pressure (kPa)',fontsize=14)
# plt.xlabel('x (m)',fontsize=14)
plt.tight_layout()
plt.legend(fontsize = legend_fontsize,loc = 'upper left', frameon=with_frame_legend)
plt.savefig('wall_pressure.png', dpi = 600)
plt.show()
plt.close()




#-------------------------------------------------------#
#--------------------------------------------------------------------#
#------Plot heatflux data for single mesh of interest----------------#
key_select = 'wallHeatFlux'


#------------------------------------------------------------#
if ref_heatflux_data is not None:
    labelplot = 'ref'
    # if (zoom_flag) and (run_nb in ['run4', 'run6']):
    #     labelplot = '_ref'

    plt.errorbar(ref_heatflux_data[:,0],
                ref_heatflux_data[:,1]*scale_fac_dict[key_select],
                        fmt='o', linestyle = 'none',
                        yerr=ref_heatflux_data[:,1]*5/100*scale_fac_dict[key_select],
                        elinewidth=3,
                label=labelplot,
                color= 'k')

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
                            user_color = solver_specific_color,
                            scale_fac = scale_fac_dict[key_select])


# plt.yscale('log')

# apply pre-defined, run and geometry dependent x-axis limit
helpfunc.apply_axes_limits(run_nb, geom_nb)
if run_nb == 'run14':
    plt.ylim(top = 1e6*scale_fac_dict[key_select])
if run_nb == 'run4':
    plt.ylim(top = 5e6*scale_fac_dict[key_select])
    plt.ylim(bottom = -1e3*scale_fac_dict[key_select])
if run_nb == 'run45':
    plt.ylim(top = 6.5e6*scale_fac_dict[key_select])
    plt.ylim(bottom = -1e3*scale_fac_dict[key_select])

else:
    plt.ylim(top=ylim_up_dict[run_nb][key_select]*scale_fac_dict[key_select])
    plt.ylim(bottom=0)

if geom_nb == 'geom2':
    plt.xlim(right=2.51)
    plt.xlim(left=2.25)
if run_nb == 'run33':
    plt.xlim(left=2.2)

if zoom_flag:
    key_select = 'noseHeatFlux'
    plt.xlim([0,2])
    plt.ylim(top = ylim_up_dict[run_nb][key_select]*scale_fac_dict[key_select])
    plt.ylim(bottom = 0e6*scale_fac_dict[key_select])
    if run_nb in ['run4', 'run6']:
        plt.xlim([0,2.5])

plt.ylabel('Heat Flux (MW / $m^2$)')

plt.tight_layout()
# plt.grid(True)
legend = plt.legend(fontsize = legend_fontsize,loc = 'upper left',
        frameon=with_frame_legend)
# legend.get_frame().set_facecolor('white')  # Set the background color (opaque)
# legend.get_frame().set_edgecolor('none')  # Remove the border

if zoom_flag:
    plt.legend(fontsize = legend_fontsize,loc = 'upper right')
    if run_nb == 'run45':
        plt.legend(fontsize = legend_fontsize,loc = 'lower right', ncol = 2)
        
plt.savefig('wall_heatflux.png', dpi = 600)
plt.show()
plt.close()




#-- go back to orginal directory---#
os.chdir(work_dir)




