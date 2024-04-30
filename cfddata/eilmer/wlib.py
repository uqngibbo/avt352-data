"""
Plot the final wall heat transfer in a nice kind of way.

@author: Nick Gibbons
"""

from numpy import zeros, array, mean, concatenate, argsort, stack
from glob import glob
from os.path import isdir
import matplotlib.pyplot as plt

def number(thing):
    try:
        outnumber = int(thing)
    except(ValueError):
        try:
            outnumber = float(thing)
        except(ValueError):
            outnumber = complex(thing.replace('i','j')).real
    return outnumber

def read_loads_file(filename):
    header = None
    body = []
    with open(filename) as fp:
        for line in fp:
            line = line.strip().split()
            if line[0].startswith('#'):
                header = line[1:]
            else:
                body.append(list(map(number,line)))
            
    assert header!=None
    header = [i.split(':')[-1] if ':' in i else i for i in header]
    cols = [array(col) for col in zip(*body)]
    data = dict(zip(header,cols))
    return data

def collate_datafiles(datafiles, sortkey='pos.x'):
    keys = list(datafiles[0].keys())

    data = {}
    for k in keys:
        values = [f[k] for f in datafiles]
        data[k] = concatenate(values)

    print(len(datafiles))
    if not sortkey is None:
        idxs = argsort(data[sortkey])
        for k,v in data.items():
            data[k] = v[idxs].copy()

    return data

def read_expdata(filename):
    with open(filename) as fp:
        lines = [line for line in fp]

    print(lines[0])
    header = [item.strip() for item in lines[0].split(',')]
    print(header)
    body = [list(map(float, items.split(','))) for items in lines[1:]]
    cols = [array(col) for col in zip(*body)]
    data = dict(zip(header, cols))
    return data

def read_simdata(path):
    print("Reading name: ", path)
    jobname = glob(path+'/config/*.config')[0].split('/')[-1].split('.config')[0]
    metadata = read_loads_file(path+'/loads/{}-loads.times'.format(jobname))
    index = metadata['loads_index'][-1]
    print("index: ", index)

    time_string = str(index).zfill(4)
    datafilenames = sorted(glob(path+'/loads/t{}/*.wall.dat'.format(time_string)))
    print("len(datafilenames): ", len(datafilenames))
    datafiles = [read_loads_file(filename) for filename in datafilenames]
    print("len(datafiles): ", len(datafiles))
    data = collate_datafiles(datafiles, sortkey='pos.x')
    print("Mean yplus ", mean(data['y+']))
    return data

def parse_arguments(args, title='Axisymmetric Cone-Flare'):
    exps = []
    datas = []

    for argument in args:
        if argument.endswith('.csv'):
            exp = read_expdata(argument)
            exps.append(exp)
        elif isdir(argument):
            data = read_simdata(argument)
            data['name'] = argument
            datas.append(data)
        else:
            title = argument
    return exps, datas, title

def WallPlot(exps, datas, title, cfdkey, expkey, ylabel, filename, errpercent, zoom=False, override_colour=None):
    plt.rcParams.update({'font.size': 12})
    plt.rcParams['svg.fonttype'] = 'none'

    lines = ['-','--','-.',':','-']
    colours = ['blue', 'red', 'black', 'green', 'cyan', 'magenta']


    if zoom:
        fig = plt.figure(figsize=(7,6))
    else:
        fig = plt.figure(figsize=(18,7))
    ax, ax1 = fig.subplots(2,1, gridspec_kw={'height_ratios': [3,1]}) 

    for j, data in enumerate(datas):
        linestyle = '-'
        linewidth = 2.0
        if override_colour:
            colour = override_colour
        else:
            colour = colours[j]
        ax.plot(data['pos.x'], data[cfdkey], color=colour, linewidth=linewidth, linestyle=linestyle, label=data['name'])
        ax1.plot(data['pos.x'], data['pos.y'], 'k-', linewidth=2.0)

    for j, exp in enumerate(exps):
        #ax.plot(exp['x (mm)']/1000.0, exp[expkey], linestyle="None", color='black', marker='o', label='exp')
        ax.errorbar(exp['x (mm)']/1000.0, exp[expkey], yerr=exp[expkey]*errpercent, fmt='ko', capsize=2, elinewidth=2, markeredgewidth=2)


    ax.set_ylabel(ylabel)
    ax.set_xticklabels([])
    ax1.set_xlabel('x (m)')
    #ax.set_title(title)

    ax.legend(framealpha=1.0, loc='upper left')
    ax.grid()
    if zoom:
        xmin, xmax = ax.get_xlim()
        xstart = 0.82*(xmax-xmin) + xmin
        xend   = 0.96*(xmax-xmin) + xmin
        ax.set_xlim(xstart, xend)
        ax1.set_xlim(xstart, xend)
    plt.tight_layout()
    #plt.savefig(filename)
    #plt.close()
    plt.show()

