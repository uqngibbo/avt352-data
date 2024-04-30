"""
Plot the final wall heat transfer in a nice kind of way.

@author: Nick Gibbons
"""

from sys import argv
from wlib import *

cfdkey = 'q_total (W/cm2)'
expkey = 'Q (W/cm2)'
ylabel ='WHT (W/cm2)' 
filename = 'wht.svg'
errpercent = 5.0/100.0

if __name__=='__main__':
    exps, datas, title = parse_arguments(argv[1:])

    
    cfd = read_loads_file(argv[1])
    exp = read_expdata(argv[2])
    title = argv[3]
    zoom = False
    if len(argv)==5:
        filename = 'zwht.svg'
        zoom = True

    cfd['name'] = "{}: Heat Transfer".format(title)
    datas = [cfd]
    exps = [exp]

    for data in datas: data['q_total (W/cm2)'] = data['q_total']/1e4
    for exp in exps:   exp['Q (W/cm2)']        = exp['Q (W/m2)']/1e4

    WallPlot(exps, datas, title, cfdkey, expkey, ylabel, filename, errpercent, zoom, 'red')
