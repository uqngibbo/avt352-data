"""
Plot the final wall heat transfer in a nice kind of way.

@author: Nick Gibbons
"""

from sys import argv
from wlib import *

cfdkey = 'p (kPa)'
expkey = 'P (kPa)'
ylabel ='Pressure (kPa)' 
filename = 'wp.svg'
errpercent = 3.0/100.0

if __name__=='__main__':
    exps, datas, title = parse_arguments(argv[1:])

    
    cfd = read_loads_file(argv[1])
    exp = read_expdata(argv[2])
    title = argv[3]
    zoom = False
    if len(argv)==5:
        filename = 'zwht.svg'
        zoom = True

    cfd['name'] = "{}: Pressure".format(title)
    datas = [cfd]
    exps = [exp]

    for data in datas: data['p (kPa)'] = data['p']/1e3
    for exp in exps:   exp['P (kPa)']  = exp['P (Pa)']/1e3

    WallPlot(exps, datas, title, cfdkey, expkey, ylabel, filename, errpercent, zoom, 'blue')
