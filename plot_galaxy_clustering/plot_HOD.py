import numpy as np
import matplotlib.pyplot as plt

plt.rc('text',usetex=True)
plt.rc('font',size=15,family='serif')

#===================
# Files
#===================
File_HR_Base     = 'Catalogs/highres-galaxy_hod.txt'
File_HR_As	     = 'Catalogs/highres-galaxy_hod_assembly.txt'
File_LR_As 	     = 'Catalogs/lowres-galaxy_hod_assembly.txt'
File_LR_As_Cr    = 'Catalogs/lowres-galaxy_hod_assembly_correct.txt'
File_HR_As_Rv    = 'Catalogs/highres-galaxy_hod_assembly_reverse.txt'
File_LR_As_Cr_Rv = 'Catalogs/lowres-galaxy_hod_assembly_correct_reverse.txt'
#===================

#===================
# Read
#===================
logM,Nh_HR_Base    ,Nc_HR_Base    ,Ns_HR_Base     = np.loadtxt(File_HR_Base    ,unpack=True)
_   ,Nh_HR_As      ,Nc_HR_As      ,Ns_HR_As       = np.loadtxt(File_HR_As      ,unpack=True)
_   ,Nh_LR_As      ,Nc_LR_As      ,Ns_LR_As       = np.loadtxt(File_LR_As      ,unpack=True)
_   ,Nh_LR_As_Cr   ,Nc_LR_As_Cr   ,Ns_LR_As_Cr    = np.loadtxt(File_LR_As_Cr   ,unpack=True)
_   ,Nh_HR_As_Rv   ,Nc_HR_As_Rv   ,Ns_HR_As_Rv    = np.loadtxt(File_HR_As_Rv   ,unpack=True)
_   ,Nh_LR_As_Cr_Rv,Nc_LR_As_Cr_Rv,Ns_LR_As_Cr_Rv = np.loadtxt(File_LR_As_Cr_Rv,unpack=True)
#===================

#===================
# Ratios
#===================
Nc_HR_Base     = Nc_HR_Base    /Nh_HR_Base
Nc_HR_As       = Nc_HR_As      /Nh_HR_As
Nc_LR_As       = Nc_LR_As      /Nh_LR_As
Nc_LR_As_Cr    = Nc_LR_As_Cr   /Nh_LR_As_Cr
Nc_HR_As_Rv    = Nc_HR_As_Rv   /Nh_HR_As_Rv
Nc_LR_As_Cr_Rv = Nc_LR_As_Cr_Rv/Nh_LR_As_Cr_Rv

Ns_HR_Base     = Ns_HR_Base    /Nh_HR_Base
Ns_HR_As       = Ns_HR_As      /Nh_HR_As
Ns_LR_As       = Ns_LR_As      /Nh_LR_As
Ns_LR_As_Cr    = Ns_LR_As_Cr   /Nh_LR_As_Cr
Ns_HR_As_Rv    = Ns_HR_As_Rv   /Nh_HR_As_Rv
Ns_LR_As_Cr_Rv = Ns_LR_As_Cr_Rv/Nh_LR_As_Cr_Rv
#===================
print (Nc_HR_As )
#===================
# Plot
#===================
fig,ax = plt.subplots(2,2,figsize=(14,8),sharex=True)
L,B,R,T=0.08,0.12,0.95,0.85
plt.subplots_adjust(L,B,R,T,0.2,0)

ax[0,0].plot(logM,Nc_HR_Base    , 'k'  ,lw=2,label='Base')
ax[0,0].plot(logM,Nc_HR_As      , 'r'  ,lw=2,label='Assembly, HR')
ax[0,0].plot(logM,Nc_LR_As      , 'b'  ,lw=2,label='Assembly, LR')
ax[0,0].plot(logM,Nc_HR_As_Rv   , 'g--',lw=2,label='Assembly+Reverse, HR')
ax[0,0].plot(logM,Nc_LR_As_Cr   , 'm--',lw=2,label='Assembly+Correct, LR')
ax[0,0].plot(logM,Nc_LR_As_Cr_Rv, 'y--',lw=2,label='Assembly+Correct+Reverse, LR')

ax[1,0].plot(logM,Nc_HR_As      /Nc_HR_Base, 'r'  ,lw=2)
ax[1,0].plot(logM,Nc_LR_As      /Nc_HR_Base, 'b'  ,lw=2)
ax[1,0].plot(logM,Nc_HR_As_Rv   /Nc_HR_Base, 'g--',lw=2)
ax[1,0].plot(logM,Nc_LR_As_Cr   /Nc_HR_Base, 'm--',lw=2)
ax[1,0].plot(logM,Nc_LR_As_Cr_Rv/Nc_HR_Base, 'y--',lw=2)

ax[0,1].semilogy(logM,Ns_HR_Base    , 'k'  ,lw=2,label='Base')
ax[0,1].semilogy(logM,Ns_HR_As      , 'r'  ,lw=2,label='Assembly, HR')
ax[0,1].semilogy(logM,Ns_LR_As      , 'b'  ,lw=2,label='Assembly, LR')
ax[0,1].semilogy(logM,Ns_HR_As_Rv   , 'g--',lw=2,label='Assembly+Reverse, HR')
ax[0,1].semilogy(logM,Ns_LR_As_Cr   , 'm--',lw=2,label='Assembly+Correct, LR')
ax[0,1].semilogy(logM,Ns_LR_As_Cr_Rv, 'y--',lw=2,label='Assembly+Correct+Reverse, LR')

ax[1,1].plot(logM,Ns_HR_As      /Ns_HR_Base, 'r'  ,lw=2)
ax[1,1].plot(logM,Ns_LR_As      /Ns_HR_Base, 'b'  ,lw=2)
ax[1,1].plot(logM,Ns_HR_As_Rv   /Ns_HR_Base, 'g--',lw=2)
ax[1,1].plot(logM,Ns_LR_As_Cr   /Ns_HR_Base, 'm--',lw=2)
ax[1,1].plot(logM,Ns_LR_As_Cr_Rv/Ns_HR_Base, 'y--',lw=2)

ax[0,0].legend(loc='lower center',
               bbox_to_anchor = (0.5*(L+R),T+0.01),
               bbox_transform = fig.transFigure,
               ncol=2,fontsize=12)

ax[-1,0].set_xlabel('$\log(M_\mathrm h) \ [ h^{-1} \ M_\odot]$')
ax[-1,1].set_xlabel('$\log(M_\mathrm h) \ [ h^{-1} \ M_\odot]$')
ax[0,0].set_ylabel('$\langle N_\mathrm{cen}(M_\mathrm h) \\rangle$')
ax[1,0].set_ylabel('ratio w.r.t. Base')
ax[0,1].set_ylabel('$\langle N_\mathrm{sat}(M_\mathrm h) \\rangle$')
ax[1,1].set_ylabel('ratio w.r.t. Base')

plt.show()
#===================
