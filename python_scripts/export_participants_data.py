""" Exporting data
"""

import os
import glob
import copy
import shutil
import numpy as np
import matplotlib.pyplot as plt
import helper_functions as helpfunc


#-----------end helper functions------------------------------------------#
#-------------------------------------------------------------------------#

#-------------------------------------------------------------------------------#
#---------User selection zone-------------------------------#
ref_folder = "../refdata"
# geom_nb = "geom1"
solver_color = False
zoom_flag = False # If true, focus on nose cone region
with_frame_legend = False
random_data = False

# Defines the solvers selected, the grid and turbulence models
#   might look cumbersome at first but it's an elegant and simple solution to
#   work with all the existing code structure
parameter_matrix = {
    # for run4
            'run4': {
            ##---------SU2 bluntness study isolated----------------#
            'SU2':{ 'mesh':'meshYY',
                    'turb_model_list': ['Blunt01','Blunt05', 'Blunt12','Blunt26'],
                    'bounds': {'wallP': 
                                    {'Blunt01': {'xmin':2.35, 'xmax':2.9},
                                    'Blunt05': {'xmin':2.35, 'xmax':2.9},
                                    'Blunt12': {'xmin':2.35, 'xmax':2.9},
                                    'Blunt26': {'xmin':2.35, 'xmax':2.9},
                                    },
                            'wallHeatFlux': 
                                    {'Blunt01': {'xmin':0, 'xmax':1},
                                    'Blunt12': {'xmin':0, 'xmax':1},
                                    'Blunt26': {'xmin':0, 'xmax':1},
                                    }
                        },
                    'naming_dict': {'mesh':
                                        {'meshXX': 'SU2',
                                        'mesh05': 'SU2',
                                        'mesh04': 'SU2',
                                        'meshYY': ''},

                                        'turb':
                                            {'SST': 'k-$\\omega$ SST',
                                            'Blunt01': 'SST01mm',
                                            'Blunt05': 'SST05mm',
                                            'Blunt12': 'SST125mm',
                                            'Blunt26': 'SST260mm',
                                            }

                                    }  
                        },
            'starccm':{ 'mesh':'mesh08',
                        'bounds': {'wallP': 
                                    {'SST': {'xmin':2.35, 'xmax':2.9},
                                    },
                        },
                        'naming_dict': {'mesh':
                                            {'mesh08': 'STAR-CCM+'},
                                        'turb':
                                            {}
                                            # {'SST': 'k-$\\omega$ SST'} 
                                    }
                        },
            'eilmer':{ 'mesh':'mesh1',
                        'bounds': {'wallP': 
                                    {'komega': {'xmin':2.35, 'xmax':2.9},
                                    },
                        },
                        'naming_dict': {'mesh':
                                            {'mesh1': 'Eilmer'},
                                        'turb':
                                            {'komega': 'wilcox2006-klimV'} 
                                    }  
                        },
            'ansys_aselsan':{ 'mesh':'meshXX',
                            'turb_model_list': ['SST1T','SA1T', 'SST2T','SA2T'],
                            'bounds': {'wallP': 
                                        {'SST1T': {'xmin':2.35, 'xmax':2.9},
                                        'SA1T': {'xmin':2.35, 'xmax':2.9},
                                        'SST2T': {'xmin':2.35, 'xmax':2.9},
                                        'SA2T': {'xmin':2.35, 'xmax':2.9},
                                        },
                                'wallHeatFlux': 
                                        {'SST1T': {'xmin':0, 'xmax':2.9},
                                        'SA1T': {'xmin':0, 'xmax':2.9},
                                        'SST2T': {'xmin':2.35, 'xmax':2.9},
                                        'SA2T': {'xmin':2.35, 'xmax':2.9},
                                        }
                        },
                        'naming_dict': {'mesh':
                                            {'meshXX': 'Ansys Fluent (Aselsan)\n'},
                                            # {'meshXX': ''},
                                        'turb': {}
                                            # {'SST1T': 'k-$\\omega$ SST',
                                            # 'SA1T': 'SA',
                                            # 'SST2T': 'k-$\\omega$ SST 2-T',
                                            # 'SA2T': 'SA 2-T'
                                            # } 
                                    }
                         },
            'overflow':{ 'mesh':'mesh3',
                        'turb_model_list': ['SST'],
                        'bounds': {'wallP': 
                                    {'SST': {'xmin':2.35, 'xmax':2.9},
                                    },
                        },
                        'naming_dict': {'mesh':
                                            {'mesh2': 'OVERFLOW',
                                            'mesh3': 'OVERFLOW'},
                                        'turb': {}
                                            # {'SST': 'k-$\\omega$ SST'}
                                    } 
                        },
            'vulcan':{ 'mesh':'meshXX',
                        'turb_model_list': ['SST','SSTKL', 'SSTV', 'SSTVnorhok',
                                                'SA', 'SAQCRV'],
                        'bounds': {'wallP': 
                                            {'SST': {'xmin':2.35, 'xmax':2.9},
                                            'SSTKL': {'xmin':2.35, 'xmax':2.9},
                                            'SSTV': {'xmin':2.35, 'xmax':2.9},
                                            'SSTVnorhok': {'xmin':2.35, 'xmax':2.9},
                                            'SA':   {'xmin':2.35, 'xmax':2.9},
                                            'SAQCRV': {'xmin':2.35, 'xmax':2.9},
                                            },
                                    'wallHeatFlux': 
                                            {'SST': {'xmin':2.35, 'xmax':2.9},
                                            'SSTKL': {'xmin':2.35, 'xmax':2.9},
                                            'SSTV': {'xmin':0, 'xmax':2.9},
                                            'SSTVnorhok': {'xmin':2.35, 'xmax':2.9},
                                            'SA':   {'xmin':0, 'xmax':2.9},
                                            'SAQCRV': {'xmin':2.35, 'xmax':2.9},
                                            }
                                },
                        'naming_dict': {'mesh':
                                            {'meshXX': 'VULCAN'},
                                        'turb':
                                            {'SST': 'SST',
                                            # 'SAQCRV': 'SA 2013 QCR-V',
                                            'SSTKL':'SST-KL',
                                            'SSTV':'SST-V',
                                            'SSTVnorhok':'SST-Vm',
                                            'SA':'SA-noft2',
                                            'SAQCRV': 'SA-noft2-QCR-V',
                                            } 
                                    }  
                        },
            'cadence':{ 'mesh':'meshXX',
                        # 'turb_model_list': ['SSCEARSM_Prt086Lemmon'],
                        'bounds': {'wallP': 
                                    {'SSCEARSM_Prt086Lemmon_LDFSS': {'xmin':2.35, 'xmax':2.9},
                                    'SSTa10355_Prt086Lemmon_LDFSS':{'xmin':2.35, 'xmax':2.9}
                                    },
                        },
                        'naming_dict': {'mesh':
                                            {'meshXX': 'Fidelity Flow DBS\n'},
                                        'turb':
                                            {'SSCEARSM_Prt086Lemmon_LDFSS': 'SSC-EARSM',
                                            'SSTa10355_Prt086Lemmon': 'k-$\\omega$ SST',
                                            'SSTa10355_Prt086Lemmon_LDFSS':'SST-a10355'} 
                                    }  
                        },
            },
    # for run6
    'run6': {
            'eilmer':{ 'mesh':'mesh1',
                        'bounds': {'wallP': 
                                    {'komega': {'xmin':2.2, 'xmax':2.9},
                                    },
                        },
                        'naming_dict': {'mesh':
                                            {'mesh1': 'Eilmer'},
                                        'turb':
                                            {'komega': 'wilcox2006-klimV'} 
                                    }  
                        },
            'ansys_aselsan':{ 'mesh':'mesh4',
                            'bounds': {'wallP': 
                                        {'SST': {'xmin':2.2, 'xmax':2.9},
                                        },
                        },
                        'naming_dict': {'mesh':
                                            {'meshXX': 'Ansys Fluent (Aselsan)\n'},
                                            # {'meshXX': ''},
                                        'turb': {}
                                    }
                        },
            'cadence':{ 'mesh':'meshXX',
                        'bounds': {'wallP': 
                                    {'SSCEARSM_Prt086Lemmon_LDFSS': {'xmin':2.2, 'xmax':2.9},
                                    'SSTa10355_Prt086Lemmon_LDFSS':{'xmin':2.2, 'xmax':2.9}
                                    },
                        },
                        'naming_dict': {'mesh':
                                            {'meshXX': 'Fidelity Flow DBS\n'},
                                        'turb':
                                            {'SSCEARSM_Prt086Lemmon_LDFSS': 'SSC-EARSM',
                                            'SSTa10355_Prt086Lemmon': 'k-$\\omega$ SST',
                                            'SSTa10355_Prt086Lemmon_LDFSS':'SST-a10355'} 
                                    }  
                        },
        },
        # for run 45
        'run45': {            
                'vulcan':{ 'mesh':'meshXX',
                        'turb_model_list': ['SST','SSTKL', 'SSTV', 'SSTVnorhok',
                                                'SA', 'SAQCRV'],
                        'bounds': {'wallP': 
                                            {'SST': {'xmin':2.25, 'xmax':2.9},
                                            'SSTKL': {'xmin':2.25, 'xmax':2.9},
                                            'SSTV': {'xmin':2.25, 'xmax':2.9},
                                            'SSTVnorhok': {'xmin':2.25, 'xmax':2.9},
                                            'SA':   {'xmin':2.25, 'xmax':2.9},
                                            'SAQCRV': {'xmin':2.25, 'xmax':2.9},
                                            },
                                    'wallHeatFlux': 
                                            {'SST': {'xmin':0, 'xmax':2.9},
                                            'SSTKL': {'xmin':2.25, 'xmax':2.9},
                                            'SSTV': {'xmin':2.25, 'xmax':2.9},
                                            'SSTVnorhok': {'xmin':2.25, 'xmax':2.9},
                                            'SA':   {'xmin':2.25, 'xmax':2.9},
                                            'SAQCRV': {'xmin':0, 'xmax':2.9},
                                            }
                                },
                        'naming_dict': {'mesh':
                                            {'meshXX': 'VULCAN'},
                                        'turb':
                                            {'SST': 'SST',
                                            'SSTKL':'SST-KL',
                                            'SSTV':'SST-V',
                                            'SSTVnorhok':'SST-Vm',
                                            'SA':'SA-noft2',
                                            'SAQCRV': 'SA-noft2-QCR-V',
                                            } 
                                    }           
                    }, # end VULCAN
                    'starccm':{ 'mesh':'mesh09',
                                'bounds': {'wallP': 
                                            {'SST': {'xmin':2.25, 'xmax':2.9},
                                            },
                                      },
                                'naming_dict': {'mesh':
                                                    {'mesh09': 'STAR-CCM+'},
                                                'turb':
                                                    {}
                                            }
                            },
                    'eilmer':{ 'mesh':'mesh1',
                                'bounds': {'wallP': 
                                            {'komega': {'xmin':2.25, 'xmax':2.9},
                                            },
                                },
                                'naming_dict': {'mesh':
                                                    {'mesh1': 'Eilmer'},
                                                'turb':
                                                    {'komega': 'wilcox2006-klimV'} 
                                            }  
                            },
                    'ansys_aselsan':{ 'mesh':'mesh2',
                                    'bounds': {'wallP': 
                                                {'SST': {'xmin':2.25, 'xmax':2.9},
                                                },
                                    },
                                    'naming_dict': {'mesh':
                                                        {'meshXX': 'Ansys Fluent (Aselsan)\n'},
                                                        # {'meshXX': ''},
                                                    'turb': {}
                                                }
                                },
                    'cadence':{ 'mesh':'meshXX',
                                'bounds': {'wallP': 
                                        {'SSCEARSM_Prt086Lemmon_LDFSS': {'xmin':2.25, 'xmax':2.9},
                                        'SSTa10355_Prt086Lemmon_LDFSS':{'xmin':2.25, 'xmax':2.9}
                                        },
                                    },
                                    'naming_dict': {'mesh':
                                                        {'meshXX': 'Fidelity Flow DBS\n'},
                                                    'turb':
                                                        {'SSCEARSM_Prt086Lemmon_LDFSS': 'SSC-EARSM',
                                                        'SSTa10355_Prt086Lemmon': 'k-$\\omega$ SST',
                                                        'SSTa10355_Prt086Lemmon_LDFSS':'SST-a10355'} 
                                    }
                                },
                    'SU2':{ 'mesh':'meshXX',
                            'bounds': {'wallP': 
                                        {'SST': {'xmin':2.25, 'xmax':2.9},
                                        },
                                },
                            'naming_dict': {
                                        'turb':{}
                                    }  
                        },
                    'overflow':{ 'mesh':'meshXX',
                                'turb_model_list': ['SST'],
                                'bounds': {'wallP': 
                                            {'SST': {'xmin':2.25, 'xmax':2.9},
                                            },
                                },
                                'naming_dict': {'mesh':
                                                    {'mesh2': 'OVERFLOW',
                                                    'mesh3': 'OVERFLOW'},
                                                'turb': {}
                                                    # {'SST': 'k-$\\omega$ SST'}
                                            } 
                                },
                    'tau':{ 'mesh':'meshXX',
                            'turb_model_list': ['SST2003', 'SAneg','SSGLRRw2010',
                                                'SAO', 'wilcox+SST','komegaMenterBSL',
                                                'komegaWilcox',
                                                 'EARSMWJ3DTNT',
                                                    'EARSMWJHellsten','WilcoxRSM2010'],
                            'bounds': {'wallP': 
                                            {'SST2003': {'xmin':2.25, 'xmax':2.9},
                                            'SAneg': {'xmin':2.25, 'xmax':2.9},
                                            'SSGLRRw2010': {'xmin':2.25, 'xmax':2.9},
                                            'SAO':  {'xmin':2.25, 'xmax':2.9},
                                            'wilcox+SST':  {'xmin':2.25, 'xmax':2.9},
                                            'komegaMenterBSL':  {'xmin':2.25, 'xmax':2.9},
                                            'komegaWilcox':  {'xmin':2.25, 'xmax':2.9},
                                            'EARSMWJ3DTNT':  {'xmin':2.25, 'xmax':2.9},
                                            'EARSMWJHellsten':  {'xmin':2.25, 'xmax':2.9},
                                            'WilcoxRSM2010':  {'xmin':2.25, 'xmax':2.9},
                                            },
                                        'wallHeatFlux':
                                            {'SST2003': {'xmin':0, 'xmax':2.9},
                                            'SAneg': {'xmin':0, 'xmax':2.9},
                                            'SSGLRRw2010': {'xmin':0, 'xmax':2.9},
                                            'SAO':  {'xmin':2.25, 'xmax':2.9},
                                            'wilcox+SST':  {'xmin':2.25, 'xmax':2.9},
                                            'komegaMenterBSL':  {'xmin':2.25, 'xmax':2.9},
                                            'komegaWilcox':  {'xmin':2.25, 'xmax':2.9},
                                            'EARSMWJ3DTNT':  {'xmin':2.25, 'xmax':2.9},
                                            'EARSMWJHellsten':  {'xmin':2.25, 'xmax':2.9},
                                            'WilcoxRSM2010':  {'xmin':2.25, 'xmax':2.9},
                                            }
                                },
                            'naming_dict': {
                                                'turb':{'wilcox+SST':'wilcoxSST'}
                                            }  
                        },# end TAU
                    'coda':{ 'mesh':'meshXX',
                            'bounds': {'wallP': 
                                            {'SAneg': {'xmin':2.25, 'xmax':2.9},
                                        },
                                    },
                            'naming_dict': {
                                            'turb':
                                                {} 
                                        }  
                        }, # end CODA
                    'ansys_inc':{ 'mesh':'meshXX',
                                'bounds': {'wallP': 
                                          {'GEKO': {'xmin':2.25, 'xmax':2.9},
                                        },
                                    },
                                'naming_dict': {
                                                'turb': {} 
                                            }  
                        }, # end ANSYS INC

            # # # #         # # ##--------second plot------------------------#
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
            # # # #         # # # ##--------------------------------------------#
            #         'ansys_inc':{ 'mesh':'meshXX',
            #                     'naming_dict': {'mesh':
            #                                         {'meshXX': 'Ansys Fluent (Ansys Inc.)\n'},
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
                        # 'tau':{ 'mesh':'meshXX',
                        #     'turb_model_list': ['wilcox+SST', 'SAO', 'SST2003', 
                        #                     'komegaMenterBSL', 'SAneg', 'komegaWilcox'],
                        #     'naming_dict': {'mesh':
                        #                         {'meshXX': ''},
                        #                     'turb':
                        #                         {'SST2003': 'k-$\\omega$ SST',
                        #                         'SAneg': 'SA-neg',
                        #                         'SAO': 'SA-noft2',
                        #                         'SSGLRRw2010':helpfunc.obtain_mapping_dict()['SSGLRRw2010'],
                        #                         'wilcox+SST':helpfunc.obtain_mapping_dict()['wilcox+SST'],
                        #                         'komegaMenterBSL':helpfunc.obtain_mapping_dict()['komegaMenterBSL'],
                        #                         'wilcox+SST':helpfunc.obtain_mapping_dict()['wilcox+SST'],
                        #                         'komegaWilcox':helpfunc.obtain_mapping_dict()['komegaWilcox'],
                        #                         } 
                        #                 }  
                        # },                  
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
        }, # end run45 
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
                #                             'SSTa1coeff031': 'k-$\\omega$ SST  a1 = 0.31',
                #                             'SSTa1coeff0355': 'k-$\\omega$ SST a1 = 0.355',
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
        #                             {'meshXX': 'Ansys Fluent (Ansys Inc.)\n'},
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
            #                                 {'meshXX': 'Ansys Fluent (Ansys Inc.)\n'},
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


# ref_pressure_file = '_'.join((run_nb,"pressure.csv"))
# ref_heatflux_file = '_'.join((run_nb,"heatFlux.csv"))


res_folder = "export_data"

work_dir = os.getcwd()


#-------------------------------------------------------------------------------#
#-------------------------------------------------------------------------------#

# ref_pressure_data, ref_heatflux_data = helpfunc.load_experimental_data(ref_folder,
#                                                 ref_pressure_file,
#                                                 ref_heatflux_file
#                                             )


# Load all the data based on parameter_matrix dict into 
run_global_dict_all = {}
for run_nb, run_dict in parameter_matrix.items():
    global_data_dict = {}
    geom_nb = 'geom2'
    if run_nb in ['run4','run6']:
        geom_nb = 'geom1'
    for ind, key in enumerate(run_dict.keys()):
        cfd_folder = os.path.join("..","cfddata", key, geom_nb,run_nb)
        cfd_data_filenames = helpfunc.filter_cfd_data_filenames(glob.glob(cfd_folder+"/*"))
        cfd_data_dict = helpfunc.create_cfddatadict_for_solver(key, cfd_data_filenames)
        helpfunc.sort_data_dict_based_on_column(cfd_data_dict,0)
        global_data_dict[key] = cfd_data_dict
    run_global_dict_all[run_nb] = global_data_dict

#-------------------------------------------------------------------------------#


def create_random_array(num_rows):
    # Generate a random array with shape (num_rows, 2)
    random_array = np.random.random((num_rows, 2))
    return random_array


params_allowed = ['wallHeatFlux', 'wallP']
reduced_dict = copy.deepcopy(run_global_dict_all)
for run_nb, run_dict in run_global_dict_all.items():
    for cfdcode, code_dict in run_dict.items():
        for param, param_dict in code_dict.items():
            if param not in params_allowed:
                continue
            reduced_dict[run_nb][cfdcode][param] = {} # re-init the dict
            mesh_select = parameter_matrix[run_nb][cfdcode]['mesh']
            tmp_turb_dict = param_dict[mesh_select]
            turb_models_select = tmp_turb_dict.keys()
            if 'turb_model_list' in parameter_matrix[run_nb][cfdcode].keys():
                turb_models_select = parameter_matrix[run_nb][cfdcode]['turb_model_list']
            for turb_model in turb_models_select:
                # TODO add turb model renaming
                turb_model_name = turb_model
                if turb_model_name in parameter_matrix[run_nb][cfdcode]['naming_dict']['turb'].keys():
                    turb_model_name = parameter_matrix[run_nb][cfdcode]['naming_dict']['turb'][turb_model]
                tmp_data_dict = tmp_turb_dict[turb_model]
                if 'bounds' in parameter_matrix[run_nb][cfdcode].keys():
                    if param in parameter_matrix[run_nb][cfdcode]['bounds'].keys():
                        if turb_model in parameter_matrix[run_nb][cfdcode]['bounds'][param].keys():
                            print(f"Selecting indices for solver {cfdcode} and turb model {turb_model} for parameter {param}")
                            ind_select =  helpfunc.find_indices_between_vals(
                                            tmp_data_dict[:,0], 
                                            parameter_matrix[run_nb][cfdcode]['bounds'][param][turb_model]['xmin'],
                                            parameter_matrix[run_nb][cfdcode]['bounds'][param][turb_model]['xmax'])
                            tmp_data_dict = tmp_data_dict[ind_select]
                if random_data:
                    print('generating random data')
                    tmp_data_dict = create_random_array(100)
                reduced_dict[run_nb][cfdcode][param][turb_model_name] =  tmp_data_dict
            # for mesh, mesh_dict in  param_dict.items():
            #     print(mesh)

# parameter_matrix[cfdcode]['mesh']



if not os.path.isdir(res_folder):
    os.mkdir(res_folder)
os.chdir(res_folder)


res_folder_dir = os.getcwd()
param_units = {'wallP':'Pa', 'wallHeatFlux': 'W/m2'}
for run_nb, run_dict in reduced_dict.items():
    if os.path.isdir(run_nb):
        print(f'Removing previous content for {run_nb}')
        shutil.rmtree(run_nb)
    os.mkdir(run_nb)
    os.chdir(run_nb)
    run_nb_dir = os.getcwd()
    for cfdcode, code_dict in run_dict.items():
        os.mkdir(cfdcode)
        os.chdir(cfdcode)
        for param, param_dict in code_dict.items():
            if param not in params_allowed:
                continue
            units = param_units[param]
            for turb_model, data in param_dict.items():
                np.savetxt(f'{run_nb}_{cfdcode}_{param}_{turb_model}.csv', data, 
                            header = f'x(m),{param}({units})', comments = '', delimiter=',')
        os.chdir(run_nb_dir)
    os.chdir(res_folder_dir)

#--------------------------------------------------------------------#
#------Plot pressure data for single mesh of interest----------------#
#       By default this mesh is the latest one
#User define zone
key_select = 'wallP'

#--------------------------------#

# if ref_pressure_data is not None:
#     labelplot = 'ref'
#     if (zoom_flag) and (run_nb in ['run4', 'run6']):
#         labelplot = '_ref'
#     # plt.plot(ref_pressure_data[:,0], ref_pressure_data[:,1], linestyle = 'none', marker = 'o')
#     plt.errorbar(ref_pressure_data[:,0],
#                     ref_pressure_data[:,1]*scale_fac_dict[key_select],
#                     fmt='o', linestyle = 'none',
#                     yerr = ref_pressure_data[:,1]*3/100*scale_fac_dict[key_select],
#                     elinewidth=3,
#                     label=labelplot,
#                     color= 'k')
#     # plt.errorbar(x, y, yerr=dy, fmt='o', color='black',
#     #              ecolor='lightgray', elinewidth=3, capsize=0);


# for ind, cfdcode in enumerate(parameter_matrix.keys()):

#     tgt_turb_list = None
#     try:
#         tgt_turb_list = parameter_matrix[cfdcode]['turb_model_list']
#     except KeyError:
#         pass

#     naming_dict = {}
#     try:
#         naming_dict = parameter_matrix[cfdcode]['naming_dict']
#     except KeyError:
#         pass

#     # NOTE: currently assumes single mesh for results, if different mesh for different
#     #           turbulence model we'll need to handle -> loop through grids then! in list
#     solver_specific_color = solver_color_dict[cfdcode]
#     if not solver_color:
#         solver_specific_color = None
#     helpfunc.plot_loop_turbulence_models(global_data_dict[cfdcode][key_select],
#                             parameter_matrix[cfdcode]['mesh'],
#                             tgt_turb_list = tgt_turb_list,
#                             naming_dict = naming_dict,
#                             user_color = solver_specific_color,
#                             scale_fac = scale_fac_dict[key_select]
#                             )




#-- go back to orginal directory---#
os.chdir(work_dir)




