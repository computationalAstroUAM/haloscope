import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sys
import matplotlib.gridspec as gridspec
sys.path.append('../')
from hod import HOD

plt.rc('text',usetex=True)
plt.rc('font',size=20,family='serif')

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
File_LR_As_Rv   = 'Catalogs/lowres-galaxy_pk_assembly_reverse%s.txt' %(str_cen)
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

#===================
# Read
#===================
k_HR_Base    ,Pk_HR_Base    ,PknoSN_HR_Base    ,Nmodes_HR_Base     = np.loadtxt(File_HR_Base    ,unpack=True)
k_HR_As      ,Pk_HR_As      ,PknoSN_HR_As      ,Nmodes_HR_As       = np.loadtxt(File_HR_As      ,unpack=True)
k_LR_As      ,Pk_LR_As      ,PknoSN_LR_As      ,Nmodes_LR_As       = np.loadtxt(File_LR_As      ,unpack=True)
k_LR_As_Cr   ,Pk_LR_As_Cr   ,PknoSN_LR_As_Cr   ,Nmodes_LR_As_Cr    = np.loadtxt(File_LR_As_Cr   ,unpack=True)
k_LR_As_Rv   ,Pk_LR_As_Rv   ,PknoSN_LR_As_Rv   ,Nmodes_LR_As_Rv    = np.loadtxt(File_LR_As_Rv   ,unpack=True)
k_HR_As_Rv   ,Pk_HR_As_Rv   ,PknoSN_HR_As_Rv   ,Nmodes_HR_As_Rv    = np.loadtxt(File_HR_As_Rv   ,unpack=True)
k_LR_As_Cr_Rv,Pk_LR_As_Cr_Rv,PknoSN_LR_As_Cr_Rv,Nmodes_LR_As_Cr_Rv = np.loadtxt(File_LR_As_Cr_Rv,unpack=True)
#===================
 
 
dk = np.mean(k_LR_As_Rv[1:]-k_LR_As_Rv [0:-1] )
print (dk*4*np.pi*k_LR_As_Rv**2*(1000)**3/(2*np.pi)**3)

def errorbarpk(Nmode,Pk):
	return np.sqrt(2/Nmode)*Pk
#===================
# Plot
#===================
fig = plt.figure(figsize=(6,6))
gs = gridspec.GridSpec(1, 1)

ax = fig.add_subplot(gs[0,0])
ax.plot(10**(logM),Nc_HR_As      , 'blue'  ,linestyle='solid',lw=3,label='- ve assembly bias i.e.,\n'+r'$(A_{\rm cen}=B_{\rm cen}=C_{\rm cen}=D_{\rm cen}=-1)$')
ax.plot(10**(logM),Nc_HR_As_Rv      , 'red'  ,linestyle='solid',lw=3,label='+ ve assembly bias i.e.,\n'+r'$(A_{\rm cen}=B_{\rm cen}=C_{\rm cen}=D_{\rm cen}=+1)$')
ax.set_ylabel('$\langle N_\mathrm{cen} \\rangle$',fontsize=18)
ax.set_xlabel('$M_{200b}  [ h^{-1} \ M_\odot]$',fontsize=18)
ax.tick_params(axis='both', labelsize=18)
# ~ ax.legend(loc='lower right',fontsize=18,title='High Resolution Simulation \n (Reference)',title_fontsize=30)
ax.legend(loc='lower right',fontsize=15)

ax.set_xscale('log')
#ax.plot(logM,Nc_LR_As      , 'b'  ,lw=2,label='Assembly, LR')
#ax.plot(logM,Nc_HR_As_Rv   , 'g--',lw=2,label='Assembly+Reverse, HR')
#ax.plot(logM,Nc_LR_As_Cr   , 'm--',lw=2,label='Assembly+Correct, LR')
#ax.plot(logM,Nc_LR_As_Cr_Rv, 'y--',lw=2,label='Assembly+Correct+Reverse, LR')
plt.savefig('HOD.pdf',bbox_inches='tight')
plt.show()
fig = plt.figure(figsize=(12,10))
gs = gridspec.GridSpec(2,1,height_ratios=[1.5,1])


def errorbandplot(x,y,error,color,lw,linestyle='solid',label=None):
	ax.plot(x,y,color=color,lw=lw,linestyle=linestyle,label=label)
	ax.fill_between(x,y-error,y+error,color=color,alpha=0.08)

#fig,ax = plt.subplots(3,1,)
L,B,R,T=0.12,0.12,0.95,0.95
plt.subplots_adjust(L,B,R,T,0.2,0.02)
ax = fig.add_subplot(gs[0, 0])

errorbandplot(k_HR_As      ,PknoSN_HR_As ,	0   , color='blue'  ,lw=2,label='-ve AB parameters')
errorbandplot(k_LR_As      ,PknoSN_LR_As      , 0,color = 'tab:blue'  ,lw=2)
errorbandplot(k_LR_As_Cr   ,PknoSN_LR_As_Cr   , 0,color = 'tab:blue',lw=2,linestyle='dashed')

errorbandplot(k_HR_As_Rv   ,PknoSN_HR_As_Rv   , 0,color = 'red',lw=2,label='+ve AB parameters')
errorbandplot(k_LR_As      ,PknoSN_LR_As_Rv    ,0  , color = 'tab:brown', lw=2)
errorbandplot(k_LR_As_Cr_Rv,PknoSN_LR_As_Cr_Rv, 0,color = 'tab:brown', lw=2,linestyle='dashed')
ax.set_xlim([0.009,2])
ax.legend(loc='upper right',fontsize=20,title='High-Resolution Simulation \n (Reference)',title_fontsize=20)
# ~ ax.set_ylabel('$P_{gg}(k) \ [h^{-1} \ \mathrm{Mpc}]^3$',fontsize=20)
ax.set_ylabel('$P_{gg}(k) \ [h^{-1} \ \mathrm{Mpc}]^3$',fontsize=30)
ax.set_xscale('log')
ax.set_yscale('log')
plt.xticks([])
ax = fig.add_subplot(gs[1, 0])
# ~ ax.semilogx(k_HR_Base,PknoSN_HR_As      /PknoSN_HR_As   ,'r'  ,lw=3)

def errorquadrature_div(delA,delB,A,B):
	return A/B *np.sqrt((delA/A)**2+(delB/B)**2)
	
delA = errorbarpk(Nmodes_LR_As,Pk_LR_As)
delB = errorbarpk(Nmodes_HR_As,Pk_HR_As)
delA  = 0  ### dont propagate errors
delB = 0
A = PknoSN_LR_As
B = PknoSN_HR_As

errorbandplot(k_HR_Base,PknoSN_LR_As      /PknoSN_HR_As ,errorquadrature_div(delA,delB,A,B),color='tab:blue'  ,lw=2,label='- ve AB parameters')
#ax.errorbar(k_HR_Base,PknoSN_LR_As      /PknoSN_HR_As   ,errorquadrature_div(delA,delB,A,B),color='tab:blue'  ,lw=3)
# ~ ax.semilogx(k_HR_Base,PknoSN_HR_As_Rv   /PknoSN_HR_As   ,'g--',lw=3)
delA = errorbarpk(Nmodes_LR_As_Cr,Pk_LR_As_Cr)
delB = errorbarpk(Nmodes_HR_As,Pk_HR_As)
delA  = 0  ### dont propagate errors
delB = 0
A = PknoSN_LR_As_Cr
B = PknoSN_HR_As
errorbandplot(k_HR_Base,PknoSN_LR_As_Cr   /PknoSN_HR_As ,errorquadrature_div(delA,delB,A,B),color='tab:blue'  ,lw=2,linestyle='dashed',label='- ve AB parameters, \n (corrected)')


delA = errorbarpk(Nmodes_LR_As_Rv,Pk_LR_As_Rv)
delB = errorbarpk(Nmodes_HR_As_Rv,Pk_HR_As_Rv)
delA  = 0  ### dont propagate errors
delB = 0
A = PknoSN_LR_As_Rv
B = PknoSN_HR_As_Rv
errorbandplot(k_HR_Base,PknoSN_LR_As_Rv   /PknoSN_HR_As_Rv,errorquadrature_div(delA,delB,A,B),color='tab:brown',lw=2,label='+ve AB parameters')

delA = errorbarpk(Nmodes_LR_As_Cr_Rv,PknoSN_LR_As_Cr_Rv)
delB = errorbarpk(Nmodes_HR_As_Rv,PknoSN_HR_As_Rv)
delA  = 0  ### dont propagate errors
delB = 0
A = PknoSN_LR_As_Cr_Rv
B = PknoSN_HR_As_Rv
errorbandplot(k_HR_Base,PknoSN_LR_As_Cr_Rv/PknoSN_HR_As_Rv,errorquadrature_div(delA,delB,A,B),linestyle='dashed',color='tab:brown',lw=2,label='+ve AB parameters, \n (corrected)')
#ax.semilogx(k_HR_Base,PknoSN_LR_As_Cr_Rv/PknoSN_HR_As_Rv,'y--',lw=3)

ax.legend(bbox_to_anchor=(0.75, 1.6),fontsize=20,title='Low-Resolution Simulation',title_fontsize=20,ncols=2)


ax.set_xscale('log')
ax.axhline(1.,c='k',ls=':',alpha=0.2)
ax.axhline(1.05,c='k',ls='--',alpha=0.2)
ax.axhline(0.95,c='k',ls='--',alpha=0.2)
ax.axhline(1.15,c='k',ls='-.',alpha=0.2)
ax.axhline(0.85,c='k',ls='-.',alpha=0.2)

ax.set_ylabel('$P_{gg}/P_{gg}^{\mathrm{HR}}$',fontsize=30)
ax.set_xlim([0.009,2])
ax.set_ylim([0.7,1.3])

ax.axhline(1.,c='k',ls=':',alpha=0.2)
#ax.semilogx(k_HR_Base,PknoSN_HR_As_Rv   /PknoSN_HR_As   ,'g--',lw=3)

ax.set_ylabel('$P_{gg}^{\mathrm{LR}}/P_{gg}^{\mathrm{HR}}$',fontsize=30)
ax.set_xlabel('$k \ [ h \ \mathrm{Mpc}^{-1}]$',fontsize=30)
plt.savefig('GalaxyPS.pdf',bbox_inches='tight')
#===================
plt.show()
