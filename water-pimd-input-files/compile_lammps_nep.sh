#!/bin/sh

# Fetch lammps
git clone https://github.com/lammps/lammps.git

# Fetch NEP_CPU
git clone https://github.com/brucefan1983/NEP_CPU.git

NEP_CPU_PATH=NEP_CPU
LAMMPS_PATH=lammps
curdir=$(pwd)
cp $NEP_CPU_PATH/src/nep.*  $NEP_CPU_PATH/interface/lammps/USER-NEP/
cp -r $NEP_CPU_PATH/interface/lammps/USER-NEP/ $LAMMPS_PATH/src
cd $LAMMPS_PATH/src
make clean-mpi
make no-user-nep
make yes-MISC
make yes-extra-compute
make yes-extra-dump
make yes-user-nep
make mpi -j 8
mv lmp_mpi $curdir
