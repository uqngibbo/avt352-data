#!/bin/bash
python3 wht.py geom1/run4/run4_data_mesh1-komega.txt geom1/run4/run4_heatFlux_si.csv "Run 04" zoom
python3 wp.py geom1/run4/run4_data_mesh1-komega.txt geom1/run4/run4_pressure_si.csv "Run 04" zoom
