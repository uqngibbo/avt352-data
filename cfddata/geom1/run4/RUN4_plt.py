import numpy as np
import matplotlib.pyplot as plt
import pdb


# CONVERSION DATA
psiToPa=6894.7573
butTokWm=11356.538527 
InchesToMeters=0.0254


HF_coarse=np.loadtxt("./RUN4_SU2_gridConv_coarse_heatFlux.dat",unpack=True)
P_coarse=np.loadtxt("./RUN4_SU2_gridConv_coarse_pressure.dat",unpack=True)
HF_med=np.loadtxt("./RUN4_SU2_gridConv_medium_heatFlux.dat",unpack=True)
P_med=np.loadtxt("./RUN4_SU2_gridConv_medium_pressure.dat",unpack=True)
HF_fin=np.loadtxt("./RUN4_SU2_gridConv_fine_heatFlux.dat",unpack=True)
P_fin=np.loadtxt("./RUN4_SU2_gridConv_fine_pressure.dat",unpack=True)
HF_fin1=np.loadtxt("./RUN4_SU2_gridConv_vfine_heatFlux.dat",unpack=True)
P_fin1=np.loadtxt("./RUN4_SU2_gridConv_vfine_pressure.dat",unpack=True)
HF_fin2=np.loadtxt("./RUN4_SU2_gridConv_sfine_heatFlux.dat",unpack=True)
P_fin2=np.loadtxt("./RUN4_SU2_gridConv_sfine_pressure.dat",unpack=True)
HF_hwr=np.loadtxt("./RUN4_SU2_gridConv_hwr_heatFlux.dat",unpack=True)
P_hwr=np.loadtxt("./RUN4_SU2_gridConv_hwr_pressure.dat",unpack=True)


HF_1st=np.loadtxt("./RUN4_SU2_schemeOrder_1st_heatFlux.dat",unpack=True)
P_1st=np.loadtxt("./RUN4_SU2_schemeOrder_1st_pressure.dat",unpack=True)
HF_2nd=np.loadtxt("./RUN4_SU2_schemeOrder_2nd_heatFlux.dat",unpack=True)
P_2nd=np.loadtxt("./RUN4_SU2_schemeOrder_2nd_pressure.dat",unpack=True)

run4_hf=np.loadtxt("../../../../refdata/run4_heatFlux.csv",unpack=True,delimiter=",",skiprows=1)
run4_p=np.loadtxt("../../../../refdata/run4_pressure.csv",unpack=True,delimiter=",",skiprows=1)



plt.set_cmap('jet')

# RUN 4: Pressure - scheme order
plt.figure()
norm=1000.0

plt.plot(P_1st[0,:],P_1st[1,:]/norm,label="First-order")
plt.plot(P_2nd[0,:],P_2nd[1,:]/norm,label="Second-order")

plt.scatter(run4_p[0,:]*InchesToMeters,run4_p[1,:]*psiToPa/norm, facecolors='none', edgecolors='k', label="Experiment")
plt.legend()
plt.xlim([2.5,2.86])
plt.xlabel(r'$x$ (m)')
plt.ylabel('Wall static pressure (kPa)')
plt.tight_layout()
plt.savefig("RUN4_pressure_schemeOrder.pdf")


# RUN 4: Heat Flux -scheme order
plt.figure()
norm=1000.0

plt.plot(HF_1st[0,:],HF_1st[1,:],label="First-order")
plt.plot(HF_2nd[0,:],HF_2nd[1,:],label="Second-order")

plt.scatter(run4_hf[0,:]*InchesToMeters,run4_hf[1,:]*butTokWm, facecolors='none', edgecolors='k', label="Experiment")
plt.legend()

plt.xlim([2.5,2.86])
plt.xlabel(r'$x$ (m)')
plt.ylabel('Heat flux (W/m^2))')
plt.tight_layout()
plt.savefig("RUN4_heatFlux_schemeOrder.pdf")
plt.show()





# RUN 4: Pressure - Grid Convergence
plt.figure()
norm=1000.0

plt.plot(P_coarse[0,:],P_coarse[1,:]/norm,label="coarse")
plt.plot(P_med[0,:],P_med[1,:]/norm,label="medium")
plt.plot(P_fin[0,:],P_fin[1,:]/norm,label="fine")
plt.plot(P_fin1[0,:],P_fin1[1,:]/norm,label="fine1")
plt.plot(P_fin2[0,:],P_fin2[1,:]/norm,label="fine2")
plt.plot(P_hwr[0,:],P_hwr[1,:]/norm,label="very fine")
plt.scatter(run4_p[0,:]*InchesToMeters,run4_p[1,:]*psiToPa/norm, facecolors='none', edgecolors='k', label="Experiment")
plt.legend()
plt.xlim([2.5,2.86])
plt.xlabel(r'$x$ (m)')
plt.ylabel('Wall static pressure (kPa)')
plt.tight_layout()
plt.savefig("RUN4_pressure_gridConvergence.pdf")


# RUN 4: Heat Flux - Grid Convergence
plt.figure()
norm=1000.0

plt.plot(HF_coarse[0,:],HF_coarse[1,:],label="coarse")
plt.plot(HF_med[0,:],HF_med[1,:],label="medium")
plt.plot(HF_fin[0,:],HF_fin[1,:],label="fine")
plt.plot(HF_fin1[0,:],HF_fin1[1,:],label="fine1")
plt.plot(HF_fin2[0,:],HF_fin2[1,:],label="fine2")
plt.plot(HF_hwr[0,:],HF_hwr[1,:],label="very fine")
plt.scatter(run4_hf[0,:]*InchesToMeters,run4_hf[1,:]*butTokWm, facecolors='none', edgecolors='k', label="Experiment")
plt.legend()

plt.xlim([2.5,2.86])
plt.xlabel(r'$x$ (m)')
plt.ylabel('Heat flux (W/m^2))')
plt.tight_layout()
plt.savefig("RUN4_heatFlux_gridConvergence.pdf")
plt.show()




