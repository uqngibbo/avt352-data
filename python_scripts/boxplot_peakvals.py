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

limits_dict = {'geom1':{'xlim': {'min':2.4, 'max':2.75}},
                'geom2':{'xlim': {'min':2.2, 'max':2.45}
                }
            }


work_dir = os.getcwd()

#-------------------------------------------------------------------------------#
#-------------------------------------------------------------------------------#

exp_sep = helpfunc.get_experimental_separation()
geom_info = helpfunc.get_geometry_information()

geom_names_dict = {'geom1': '6/42 cone-flare' , 'geom2': '7/40 cone-flare'}

geom_select = 'geom2'
variable_of_interest = 'pressure'
font_size = 14
vertical_boxplot = True



cfd_sep = helpfunc.get_cfd_peak_vals_and_locs_values(variable_of_interest, 'peak')


data = []
labels = []
for keys in cfd_sep[geom_select].keys():
    labels.append(keys)
    data.append(cfd_sep[geom_select][keys])

# Sample data
# data = [
#     [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],  # Data for Category A
#     [2, 3, 4, 5, 6, 7, 8, 9, 10, 11],  # Data for Category B
#     [1, 1, 2, 2, 3, 3, 4, 4, 5, 5]   # Data for Category C
# ]




# Create a figure and axis
fig, ax = plt.subplots()

# Create boxplots
ax.boxplot(data, vert = vertical_boxplot)

# # Plot a point on the first boxplot (Category A)
# for ind, run_nb in enumerate(labels):
#     label = ''
#     if ind == 0:
#         label = 'experimental \n separation onset'
#     if vertical_boxplot:
#         ax.scatter(ind+1, exp_sep[run_nb], color='red', label = label)  # (x=1, y=7)
#     else:
#         ax.scatter(exp_sep[run_nb], ind+1,color='red', label = label)  # (x=1, y=7)


# Create a secondary axis that shares the same x-axis
# ax2 = ax.twinx()

# tmp_geom = geom_info[geom_select]
# cone_flare_x = [0,tmp_geom['cone'], tmp_geom['total']]
# cone_flare_y = [0,
#                 tmp_geom['cone']*np.sin(np.deg2rad(tmp_geom['angle_cone'])),
#                 tmp_geom['cone']*np.sin(np.deg2rad(tmp_geom['angle_cone'])) \
#                 + tmp_geom['flare']*np.sin(np.deg2rad(tmp_geom['angle_flare']))
#                 ]
# ax2.plot(cone_flare_x, cone_flare_y, linestyle = '--', linewidth=  2, label = 'cone-flare \n geometry')
# ax2.set_ylabel('y (m)', fontsize=font_size)

# increase tick width
ax.tick_params(width=2)
# ax2.tick_params(width=2)

# if geom_select == 'geom1':
#     plt.plot([1, geom_info[geom_select]['cone']], [0, len(labels) -0.5], linestyle = '--',
#                     color = 'b')
#     plt.plot([geom_info[geom_select]['cone'], geom_info[geom_select]['total']],
#                 [len(labels) -0.5, len(labels)+1], linestyle = '--', color = 'b',
#                 label = 'cone-flare representation')
# else:
#     plt.plot([1, geom_info[geom_select]['cone']], [0, len(labels)/2], linestyle = '--',
#                     color = 'b')
#     plt.plot([geom_info[geom_select]['cone'], geom_info[geom_select]['total']],
#                 [len(labels)/2, len(labels)+1], linestyle = '--', color = 'b',
#                 label = 'cone-flare \n representation')

# showmeans=True, meanline=True, meanprops={'color': 'red', 'linewidth': 2}

# # Given parameters
# start_x = 0
# start_y = 1
# angle_degrees = 6
# length = 

# # Convert angle to radians
# angle_radians = np.radians(angle_degrees)

# # Calculate the change in x and y
# delta_x = length * np.cos(angle_radians)
# delta_y = length * np.sin(angle_radians)


# Set custom xtick labels
if vertical_boxplot:
    ax.set_xticklabels(labels, fontsize=font_size)
    

    ax.set_ylabel('peak pressure (kPa)', fontsize=font_size)
    if variable_of_interest == 'heatflux':
        ax.set_ylabel('peak heat flux (MW)', fontsize=font_size)

    ax.set_xlabel('runs', fontsize=font_size)

else:
    ax.set_yticklabels(labels)
    ax.set_xlabel('axial location (m)', fontsize=font_size)
    ax.set_ylabel('runs', fontsize=font_size)

# Set title and labels
# ax.set_title('Box plot for '  + geom_names_dict[geom_select])


# if geom_select == 'geom1':
#     plt.xlim(left = 2.5)
#     plt.xlim(right = 2.85)
# else:
#     plt.xlim(left = 2.3)
#     plt.xlim(right = 2.6)

# change the fontsize
ax.tick_params(axis='x', labelsize=font_size)
ax.tick_params(axis='y', labelsize=font_size)
# ax2.tick_params(axis='x', labelsize=font_size)
# ax2.tick_params(axis='y', labelsize=font_size)

# cone_ymin = (limits_dict[geom_select]['xlim']['min']) *np.sin(np.deg2rad(tmp_geom['angle_cone']))
# # cone_ymax = cone_ymin + (limits_dict[geom_select]['xlim']['max']-limits_dict[geom_select]['xlim']['min']) *np.sin(np.deg2rad(tmp_geom['angle_flare']))
# cone_ymax = cone_ymin + (limits_dict[geom_select]['xlim']['max']-tmp_geom['cone']) *np.sin(np.deg2rad(tmp_geom['angle_flare']))
# ax2.set_ylim(cone_ymin, cone_ymax)



# Get handles and labels from both axes
lines, labels = ax.get_legend_handles_labels()
# lines2, labels2 = ax2.get_legend_handles_labels()

# # Combine legends from both axes
# if geom_select == 'geom1':
#     ax.legend(lines + lines2, labels + labels2, loc='center left')
# else:
#     ax.legend(lines + lines2, labels + labels2, loc='best')

# plt.legend()
plt.tight_layout()
plt.savefig('boxplot_peakvals_'+geom_select+'_'+ variable_of_interest+'.png', dpi = 300)
# Display the plot
plt.show()


#-- go back to orginal directory---#
os.chdir(work_dir)




