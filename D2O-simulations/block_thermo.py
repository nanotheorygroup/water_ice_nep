from ase.io import read
import numpy as np

#constants and conversions
amu = 1.66054e-24
eV = 1.60218e-19
cubicm = 1.e-30
pascal = 1.e9 # turn GPa into Pa
kboltz = 1.380649e-23
extpress=1.013e-4 # GPa

### 

system = read('model.xyz')
natms = np.prod(system.get_atomic_numbers().shape)
weights = system.get_masses()
total_mass = np.sum(weights)
nmolecules = natms/3
D2O_mass = 20.0276
H2O_mass = total_mass/nmolecules

# here I want to use D2O mass!
total_mass = total_mass * D2O_mass/H2O_mass
#total_mass = 1.66054e-24 * D2O_mass  * nmolecules  # in grams

thermo=np.loadtxt("thermo.out")

#print ("Atoms:",natms)
temperature = np.average(thermo[:,0])
#print ("temperature (K):", temperature)

ekin = np.average(thermo[:,1])
epot = np.average(thermo[:,2])
etot_variance = np.var(thermo[:,1]+thermo[:,2]) 

pressx = np.average(thermo[:,3])
pressy = np.average(thermo[:,4])
pressz = np.average(thermo[:,5])

pressure = (pressx+pressy+pressz)/3
#print("Pressure (GPa):", pressure)

lx = np.average(thermo[:,9])
ly = np.average(thermo[:,10])
lz = np.average(thermo[:,11])

volume = np.average(thermo[:,9]*thermo[:,10]*thermo[:,11])
var_volume = np.var(thermo[:,9]*thermo[:,10]*thermo[:,11])
std_volume = np.std(thermo[:,9]*thermo[:,10]*thermo[:,11])
density = total_mass*1.66054/volume
std_density = density*std_volume/volume

pv = extpress*volume* cubicm*pascal/eV
enthalpy = (ekin+epot) + pv
var_enthalpy = np.var( thermo[:,1]+thermo[:,2] + extpress*pascal/eV * cubicm * thermo[:,9]**3    )
norm = 1./kboltz/temperature**2 * eV**2 / total_mass / amu * D2O_mass
Cp = var_enthalpy * norm #/kboltz/temperature**2 * eV**2 / total_mass / amu * D2O_mass # if you multiply by mass it's the molar Cp (in j/mol-K)
isocomp = var_volume /volume /(temperature*kboltz)*cubicm *1e11

# error analysis on Cp
nblocks = 5 
enth_i = np.zeros_like(thermo[:,0]) 
Cp_b = np.zeros(nblocks)
pv_pre = extpress*pascal/eV * cubicm
enth_i = thermo[:,1] + thermo[:,2] + pv_pre * thermo[:,9]*thermo[:,10]*thermo[:,11] 
enth_b = np.split(enth_i,nblocks)
for i in range(nblocks):
    Cp_b[i] = np.var( enth_b[i] ) * norm  

Cp_error = np.std(Cp_b) #/nblocks**0.5
#print("Cp (j/mol-K) =", Cp, Cp_error)

# error analysis on kappaT
vol_i = np.zeros_like(thermo[:,0])
vol_i = thermo[:,9]*thermo[:,10]*thermo[:,11]
vol_b = np.split(enth_i,nblocks)
kappa_b = np.zeros(nblocks)
norm = 1.0e11/ (temperature*kboltz)*cubicm 
for i in range(nblocks):
    kappa_b[i] = np.var(vol_b[i]) / np.average(vol_b[i]) * norm
    print(kappa_b[i])

isocomp_err = np.std(kappa_b)

#print ("enthalpy (eV):", enthalpy, "U:", ekin+epot, "PV:", pv )
print (f"{temperature:.2f}", f"{density:.4f}", f"{std_density:.4f}",
        f"{enthalpy/nmolecules:.8f}", f"{isocomp:.4f}", f"{isocomp_err:.4f}", 
        f"{Cp:.4f}",f"{Cp_error:.4f}" )


