import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sys
import matplotlib.gridspec as gridspec
sys.path.append('../')
from hod import HOD

plt.rc('text',usetex=True)
plt.rc('font',size=15,family='serif')

from matplotlib import rc
rc('font', **{'family': 'serif', 'serif': ['Computer Modern']})
#rc('text', usetex=True)

do_centrals = True
if do_centrals: str_cen = '_centrals'
else:		    str_cen = ''

#===================
# Simulation settings
#===================
Redshift  = 0.
#===================

#===================
# Files
#===================
File_HR_Base     = 'Catalogs/highres-galaxy_pk%s.txt' %(str_cen)
File_HR_As	     = 'Catalogs/highres-galaxy_pk_assembly%s.txt' %(str_cen)
File_LR_As 	     = 'Catalogs/lowres-galaxy_pk_assembly%s.txt' %(str_cen)
File_LR_As_Cr    = 'Catalogs/lowres-galaxy_pk_assembly_correct%s.txt' %(str_cen)
File_HR_As_Rv    = 'Catalogs/highres-galaxy_pk_assembly_reverse%s.txt' %(str_cen)
File_LR_As_Cr_Rv = 'Catalogs/lowres-galaxy_pk_assembly_correct_reverse%s.txt' %(str_cen)
#===================

## Catalogs 
File_HR_As_Nc	     = 'Catalogs/highres-galaxy_hod_assembly.txt'
File_HR_As_Rv_Nc   = 'Catalogs/highres-galaxy_hod_assembly_reverse.txt'


#logM,Nh_HR_Base    ,Nc_HR_Base    ,Ns_HR_Base     = np.loadtxt(File_HR_Base    ,unpack=True)
logM   ,Nh_HR_As      ,Nc_HR_As      ,Ns_HR_As       = np.loadtxt(File_HR_As_Nc      ,unpack=True)
_   ,Nh_HR_As_Rv   ,Nc_HR_As_Rv   ,Ns_HR_As_Rv    = np.loadtxt(File_HR_As_Rv_Nc   ,unpack=True)

Nc_HR_As       = Nc_HR_As      /Nh_HR_As
Nc_HR_As_Rv    = Nc_HR_As_Rv   /Nh_HR_As_Rv

print (Nc_HR_As ,logM)
#===================
# Read
#===================
k_HR_Base    ,Pk_HR_Base    ,PknoSN_HR_Base    ,Nmodes_HR_Base     = np.loadtxt(File_HR_Base    ,unpack=True)
k_HR_As      ,Pk_HR_As      ,PknoSN_HR_As      ,Nmodes_HR_As       = np.loadtxt(File_HR_As      ,unpack=True)
k_LR_As      ,Pk_LR_As      ,PknoSN_LR_As      ,Nmodes_LR_As       = np.loadtxt(File_LR_As      ,unpack=True)
k_LR_As_Cr   ,Pk_LR_As_Cr   ,PknoSN_LR_As_Cr   ,Nmodes_LR_As_Cr    = np.loadtxt(File_LR_As_Cr   ,unpack=True)
k_HR_As_Rv   ,Pk_HR_As_Rv   ,PknoSN_HR_As_Rv   ,Nmodes_HR_As_Rv    = np.loadtxt(File_HR_As_Rv   ,unpack=True)
k_LR_As_Cr_Rv,Pk_LR_As_Cr_Rv,PknoSN_LR_As_Cr_Rv,Nmodes_LR_As_Cr_Rv = np.loadtxt(File_LR_As_Cr_Rv,unpack=True)
#===================

#===================
# Plot
#===================
fig = plt.figure(figsize=(30,10),sharex=True)
gs = gridspec.GridSpec(3, 2,width_ratios=[1,2],height_ratios=[1,0.5,0.5])

ax = fig.add_subplot(gs[1:, 0])
print (Nc_HR_As.shape)
ax.plot(10**(logM),Nc_HR_As      , 'green'  ,lw=3,label='Assembly bias A_{\rm cen}=B_{\rm cen}=C_{\rm cen}=D_{\rm cen}=-1')
ax.plot(10**(logM),Nc_HR_As_Rv      , 'k'  ,linestyle='dashed',lw=3,label='Assembly, HR')
ax.set_ylabel('$\langle N_\mathrm{cen}(M_\mathrm h) \\rangle$',fontsize=30)
ax.set_xlabel('$M_{200b}  [ h^{-1} \ M_\odot]$',fontsize=30)

ax.set_xscale('log')
#ax.plot(logM,Nc_LR_As      , 'b'  ,lw=2,label='Assembly, LR')
#ax.plot(logM,Nc_HR_As_Rv   , 'g--',lw=2,label='Assembly+Reverse, HR')
#ax.plot(logM,Nc_LR_As_Cr   , 'm--',lw=2,label='Assembly+Correct, LR')
#ax.plot(logM,Nc_LR_As_Cr_Rv, 'y--',lw=2,label='Assembly+Correct+Reverse, LR')


#fig,ax = plt.subplots(3,1,)
L,B,R,T=0.12,0.12,0.95,0.95
plt.subplots_adjust(L,B,R,T,0.2,0)
ax = fig.add_subplot(gs[0, 1])

ax.loglog(k_HR_As      ,PknoSN_HR_As      , 'r'  ,lw=2,label='Assembly, HR')
ax.loglog(k_LR_As      ,PknoSN_LR_As      , 'b'  ,lw=2,label='Assembly, LR')
ax.loglog(k_HR_As_Rv   ,PknoSN_HR_As_Rv   , 'g--',lw=2,label='Assembly+Reverse, HR')
ax.loglog(k_LR_As_Cr   ,PknoSN_LR_As_Cr   , 'm--',lw=2,label='Assembly+Correct, LR')
ax.loglog(k_LR_As_Cr_Rv,PknoSN_LR_As_Cr_Rv, 'y--',lw=2,label='Assembly+Correct+Reverse, LR')
ax.set_ylabel('$P_{gg}(k) \ [(h^{-1} \ \mathrm{Mpc})^3]$',fontsize=30)
ax.legend(bbox_to_anchor=(-0.15, 0.85),fontsize=30)


ax = fig.add_subplot(gs[1, 1])
ax.semilogx(k_HR_Base,PknoSN_HR_As      /PknoSN_HR_As   ,'r'  ,lw=3)
ax.semilogx(k_HR_Base,PknoSN_LR_As      /PknoSN_HR_As   ,'b'  ,lw=3)
ax.semilogx(k_HR_Base,PknoSN_HR_As_Rv   /PknoSN_HR_As   ,'g--',lw=3)
ax.semilogx(k_HR_Base,PknoSN_LR_As_Cr   /PknoSN_HR_As   ,'m--',lw=3)
ax.semilogx(k_HR_Base,PknoSN_LR_As_Cr_Rv/PknoSN_HR_As_Rv,'y--',lw=3)
ax.axhline(1.,c='k',ls=':')

ax.set_ylabel('$P_{gg}/P_{gg}^{\mathrm{HR}}$',fontsize=30)


ax = fig.add_subplot(gs[2, 1])
ax.set_ylabel('$P_{gg}/P_{gg}^{\mathrm{HR}}$',fontsize=30)
ax.set_xlabel('$k \ [ h \ \mathrm{Mpc}^{-1}]$',fontsize=30)
plt.savefig('GalaxyPS.pdf',bbox_inches='tight')
plt.show()
#===================
