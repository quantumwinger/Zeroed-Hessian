# -*- coding: utf-8 -*-
"""
@author: SASWATA DASGUPTA
"""
import numpy as np
import os
import sys


def read_lines(filename):
    """
    Read file line by line using a generator expression
    """
    with open(filename, "r") as f:
        yield from f.readlines()


if __name__ == "__main__":
    # Handle command-line arguments
    try:
        infile = sys.argv[1]
    except IndexError:
        print("Usage: python script.py <input_file> <opt/ts>")
        sys.exit(1)

    # Read harmonic configuration
    harm_conf = list(read_lines("harmonic.txt"))
    conf_atoms = harm_conf[1].strip()
    At = np.array(list(map(int, conf_atoms.split())))

    # Extract coordinates for constrained atoms
    coords = np.loadtxt(infile, usecols=(1, 2, 3))
    coords1 = np.empty((At.shape[0], 4))
    coords1 = coords[At - 1, :]
    At = np.expand_dims(At, axis=1)
    coords1 = np.hstack((At, coords1))
    np.savetxt("coords.txt", coords1, fmt=("%d", "%6f", "%6f", "%6f"))


mol_label_opt='''
$molecule
0 1
'''

rem_opt='''
$end

$rem
method b3lyp
basis  6-31G(d,p)
jobtype opt
GEOM_OPT_COORDS 0
GEOM_OPT_MAX_CYCLES 1500
DFT_D D3_BJ
SYMMETRY             false
SYM_IGNORE           true
NO_REORIENT          true
HARM_OPT 1 ! turns on the harmonic confiner
HOATOMS {} ! No. of constrained atoms
MEM_TOTAL 60000
HARM_FORCE 450 !force constant
$end
'''.format(At.shape[0])

block_freq='''
@@@@

$molecule
read
$end

$rem
method b3lyp
basis  6-31G(d,p)
jobtype freq
DFT_D D3_BJ
SYMMETRY             false
SYM_IGNORE           true
NO_REORIENT          true
HARM_OPT 1 ! turns on the harmonic confiner
HOATOMS {} ! No. of constrained atoms
MEM_TOTAL 60000
HARM_FORCE 450 !force constant
$end
'''.format(At.shape[0])

ts_freq='''
$end

$rem
method b3lyp
basis  6-31G(d,p)
jobtype freq
DFT_D D3_BJ
SYMMETRY             false
SYM_IGNORE           true
NO_REORIENT          true
HARM_OPT 1 ! turns on the harmonic confiner
HOATOMS {} ! No. of constrained atoms
MEM_TOTAL 60000
HARM_FORCE 450 !force constant
$end
'''.format(At.shape[0])

ts_opt='''
@@@

$molecule
read
$end

$rem
method b3lyp
basis  6-31G(d,p)
jobtype ts
SCF_GUESS            read
GEOM_OPT_DMAX        100
GEOM_OPT_MAX_CYCLES 1500
DFT_D D3_BJ
GEOM_OPT_COORDS  0
SYMMETRY             false
GEOM_OPT_HESSIAN     read
SYM_IGNORE           true
NO_REORIENT          true
HARM_OPT 1 ! turns on the harmonic confiner
HOATOMS {} ! No. of constrained atoms
MEM_TOTAL 60000
HARM_FORCE 450 !force constant
$end
'''.format(At.shape[0])

if sys.argv[2] == "opt":
    with open(infile[:-4]+".inp", 'w') as f:
        f.write(mol_label_opt)
        with open(infile, 'r') as fp:
            lines = fp.readlines()
            for i in lines:
                f.write(i)
        f.write(rem_opt)
        f.write("\n")
        for j in harm_conf:
           f.write(j)
        f.write("\n")
        f.write("$coords\n")
        with open("coords.txt", 'r') as fc:
            lines_coord = fc.readlines()
            for k in lines_coord:
                f.write(k)
        f.write("$end\n\n")
        f.write(block_freq)
        f.write("\n")
        for j in harm_conf:
            f.write(j)
        f.write("\n")
        f.write("$coords\n")
        with open("coords.txt", 'r') as fc:
            lines_coord = fc.readlines()
            for k in lines_coord:
                f.write(k)
        f.write("$end\n\n")    
        f.close()


if sys.argv[2] == "ts":
    with open(infile[:-4] + ".inp", 'w') as f:
        f.write(mol_label_opt)
        with open(infile, 'r') as fp:
            lines = fp.readlines()
            for i in lines:
                f.write(i)
        f.write(ts_freq)
        f.write("\n")
        for j in harm_conf:
            f.write(j)
        f.write("\n")
        f.write("$coords\n")
        with open("coords.txt", 'r') as fc:
            lines_coord = fc.readlines()
            for k in lines_coord:
                f.write(k)
        f.write("$end\n\n")
        f.write(ts_opt)
        f.write("\n")
        for j in harm_conf:
            f.write(j)
        f.write("\n")
        f.write("$coords\n")
        with open("coords.txt", 'r') as fc:
            lines_coord = fc.readlines()
            for k in lines_coord:
                f.write(k)
        f.write("$end\n\n")
        f.write(block_freq)
        f.write("\n")
        for j in harm_conf:
            f.write(j)
        f.write("\n")
        f.write("$coords\n")
        with open("coords.txt", 'r') as fc:
            lines_coord = fc.readlines()
            for k in lines_coord:
                f.write(k)
        f.write("$end\n\n")
        f.close()


os.remove("coords.txt")
