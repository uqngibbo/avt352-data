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
cfd_sep = helpfunc.get_cfd_separation_values()

geom_names_dict = {'geom1': '6/42 cone-flare' , 'geom2': '7/40 cone-flare'}

geom_select = 'geom2'

vertical_boxplot = False

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

# Plot a point on the first boxplot (Category A)
for ind, run_nb in enumerate(labels):
    label = ''
    if ind == 0:
        label = 'experimental \n separation onset'
    if vertical_boxplot:
        ax.scatter(ind+1, exp_sep[run_nb], color='red', label = label)  # (x=1, y=7)
    else:
        ax.scatter(exp_sep[run_nb], ind+1,color='red', label = label)  # (x=1, y=7)


# Create a secondary axis that shares the same x-axis
ax2 = ax.twinx()

tmp_geom = geom_info[geom_select]
cone_flare_x = [0,tmp_geom['cone'], tmp_geom['total']]
cone_flare_y = [0,
                tmp_geom['cone']*np.sin(np.deg2rad(tmp_geom['angle_cone'])),
                tmp_geom['cone']*np.sin(np.deg2rad(tmp_geom['angle_cone'])) \
                + tmp_geom['flare']*np.sin(np.deg2rad(tmp_geom['angle_flare']))
                ]
ax2.plot(cone_flare_x, cone_flare_y, linestyle = '--', label = 'cone-flare \n geometry')
ax2.set_ylabel('y (m)')


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
    ax.set_xticklabels(labels)

else:
    ax.set_yticklabels(labels)
    ax.set_xlabel('axial separation onset location (m)')
    ax.set_ylabel('runs')

# Set title and labels
# ax.set_title('Box plot for '  + geom_names_dict[geom_select])


if geom_select == 'geom1':
    plt.xlim(left = 2.4)
    plt.xlim(right = 2.75)
else:
    plt.xlim(left = 2.2)
    plt.xlim(right = 2.45)


cone_ymin = (limits_dict[geom_select]['xlim']['min']) *np.sin(np.deg2rad(tmp_geom['angle_cone']))
# cone_ymax = cone_ymin + (limits_dict[geom_select]['xlim']['max']-limits_dict[geom_select]['xlim']['min']) *np.sin(np.deg2rad(tmp_geom['angle_flare']))
cone_ymax = cone_ymin + (limits_dict[geom_select]['xlim']['max']-tmp_geom['cone']) *np.sin(np.deg2rad(tmp_geom['angle_flare']))
ax2.set_ylim(cone_ymin, cone_ymax)


plt.legend()
plt.tight_layout()
plt.savefig('boxplot_'+geom_select+'.png', dpi = 300)
# Display the plot
plt.show()


#-- go back to orginal directory---#
os.chdir(work_dir)




